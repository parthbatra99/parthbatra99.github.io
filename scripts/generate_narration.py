#!/usr/bin/env python3
"""Generate Gemini TTS narration for a Jekyll blog post.

Usage:
    GEMINI_API_KEY=xxx python scripts/generate_narration.py _posts/2026-06-22-....md

Requires:
    pip install google-genai

Outputs:
    assets/audio/posts/<stem>.mp3
    Prints the front matter fields to add to the post.

Voice : Achernar (gemini-3.1-flash-tts-preview)
"""

import mimetypes
import os
import pathlib
import re
import struct
import subprocess
import sys
import tempfile
import time

GEMINI_MODEL = "gemini-3.1-flash-tts-preview"
VOICE_NAME = "Achernar"
CHUNK_CHARS = 1800

AUDIO_PROFILE = (
    "Warm storyteller, rich, honeyed female perfect for narration."
)
DIRECTOR_NOTE = (
    'Style: The "Vocal Smile": The soft palate is raised to keep the tone '
    "bright, sunny, and explicitly inviting. "
    "Pace: Natural conversational pace. Accent: Neutral."
)


# ── Text cleaning ─────────────────────────────────────────────────────────────

def clean_text(raw: str) -> str:
    raw = re.sub(r'<style[^>]*>.*?</style>', '', raw, flags=re.DOTALL)
    raw = re.sub(r'<script[^>]*>.*?</script>', '', raw, flags=re.DOTALL)
    raw = re.sub(r'<figure[^>]*>.*?</figure>', '', raw, flags=re.DOTALL)
    raw = re.sub(r'<video[^>]*>.*?</video>', '', raw, flags=re.DOTALL)
    raw = re.sub(r'<div[^>]*class="video-wrapper"[^>]*>.*?</div>', '', raw, flags=re.DOTALL)
    raw = re.sub(r'<[^>]+>', '', raw)
    raw = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', raw)
    raw = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', raw)
    raw = re.sub(r'\*{1,3}([^*\n]+)\*{1,3}', r'\1', raw)
    raw = re.sub(r'_{1,3}([^_\n]+)_{1,3}', r'\1', raw)
    raw = re.sub(r'^#{1,6}\s+', '', raw, flags=re.MULTILINE)
    raw = re.sub(r'^[-*_]{3,}\s*$', '', raw, flags=re.MULTILINE)
    raw = re.sub(r'```[\s\S]*?```', '', raw)
    raw = re.sub(r'`([^`]+)`', r'\1', raw)
    raw = raw.replace('—', ', ').replace('–', ', ').replace('…', '...')
    raw = re.sub(r'\n{3,}', '\n\n', raw)
    return raw.strip()


def split_chunks(text: str) -> list:
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    chunks, current = [], ''
    for para in paragraphs:
        if len(current) + len(para) + 2 <= CHUNK_CHARS:
            current = (current + '\n\n' + para).strip() if current else para
        else:
            if current:
                chunks.append(current)
            if len(para) > CHUNK_CHARS:
                sentences = re.split(r'(?<=[.!?])\s+', para)
                current = ''
                for sent in sentences:
                    if len(current) + len(sent) + 1 <= CHUNK_CHARS:
                        current = (current + ' ' + sent).strip() if current else sent
                    else:
                        if current:
                            chunks.append(current)
                        current = sent
            else:
                current = para
    if current:
        chunks.append(current)
    return chunks


# ── Gemini TTS ────────────────────────────────────────────────────────────────

def make_prompt(title: str, transcript: str) -> str:
    return (
        "Read the following transcript based on the audio profile and director's note.\n\n"
        f"# Audio Profile\n{AUDIO_PROFILE}\n\n"
        f"# Director's note\n{DIRECTOR_NOTE}\n\n"
        f"## Scene:\n{title}\n\n"
        f"## Transcript:\n{transcript}"
    )


def parse_audio_mime_type(mime_type: str) -> dict:
    bits_per_sample, rate = 16, 24000
    for param in mime_type.split(";"):
        param = param.strip()
        if param.lower().startswith("rate="):
            try:
                rate = int(param.split("=", 1)[1])
            except (ValueError, IndexError):
                pass
        elif param.startswith("audio/L"):
            try:
                bits_per_sample = int(param.split("L", 1)[1])
            except (ValueError, IndexError):
                pass
    return {"bits_per_sample": bits_per_sample, "rate": rate}


def pcm_to_wav(pcm_data: bytes, mime_type: str) -> bytes:
    p = parse_audio_mime_type(mime_type)
    bits, rate, ch = p["bits_per_sample"], p["rate"], 1
    data_size = len(pcm_data)
    block_align = ch * (bits // 8)
    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF", 36 + data_size, b"WAVE",
        b"fmt ", 16, 1, ch, rate,
        rate * block_align, block_align, bits,
        b"data", data_size,
    )
    return header + pcm_data


def generate_chunk_wav(client, title: str, chunk_text: str, max_retries: int = 5) -> bytes:
    """Call Gemini TTS for one text chunk; return WAV bytes. Retries on 429."""
    from google.genai import types
    from google.genai import errors as genai_errors

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=make_prompt(title, chunk_text))],
        )
    ]
    config = types.GenerateContentConfig(
        temperature=1,
        response_modalities=["audio"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name=VOICE_NAME
                )
            )
        ),
    )

    for attempt in range(1, max_retries + 1):
        try:
            audio_buf = bytearray()
            first_mime = None

            for chunk in client.models.generate_content_stream(
                model=GEMINI_MODEL,
                contents=contents,
                config=config,
            ):
                if chunk.parts is None:
                    continue
                part = chunk.parts[0]
                if part.inline_data and part.inline_data.data:
                    if first_mime is None:
                        first_mime = part.inline_data.mime_type
                    audio_buf.extend(part.inline_data.data)

            if not audio_buf:
                raise RuntimeError("Gemini returned no audio data for chunk")

            raw = bytes(audio_buf)
            if first_mime is None or mimetypes.guess_extension(first_mime) is None:
                return pcm_to_wav(raw, first_mime or "audio/L16;rate=24000")
            return raw

        except genai_errors.ClientError as e:
            if '429' in str(e) and attempt < max_retries:
                wait = 30 * attempt
                print(f"rate-limited, waiting {wait}s (attempt {attempt}/{max_retries}) ... ", end="", flush=True)
                time.sleep(wait)
            else:
                raise

    raise RuntimeError("Max retries exhausted")


# ── Audio assembly ────────────────────────────────────────────────────────────

def wav_files_to_mp3(wav_paths: list, out_path: pathlib.Path) -> None:
    tmp_wav = out_path.with_suffix(".tmp.wav")
    try:
        # Step 1: concatenate all WAV chunks into one WAV
        inputs = []
        for p in wav_paths:
            inputs += ["-i", str(p)]
        n = len(wav_paths)
        filter_str = "".join(f"[{i}:a]" for i in range(n)) + f"concat=n={n}:v=0:a=1[out]"
        subprocess.run(
            ["ffmpeg", "-y", *inputs,
             "-filter_complex", filter_str,
             "-map", "[out]",
             "-ar", "44100", "-ac", "1",
             str(tmp_wav)],
            check=True,
            capture_output=True,
        )
        # Step 2: encode WAV → MP3 with explicit libmp3lame (sets correct codec tag 0x0055)
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(tmp_wav),
             "-codec:a", "libmp3lame",
             "-b:a", "128k",
             "-id3v2_version", "3",
             str(out_path)],
            check=True,
            capture_output=True,
        )
    finally:
        tmp_wav.unlink(missing_ok=True)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: GEMINI_API_KEY=xxx python scripts/generate_narration.py <post.md>")
        sys.exit(1)

    try:
        from google import genai
    except ImportError:
        print("Error: google-genai not installed. Run: pip install google-genai")
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        sys.exit(1)

    post_path = pathlib.Path(sys.argv[1])
    if not post_path.exists():
        print(f"Error: file not found: {post_path}")
        sys.exit(1)

    raw = post_path.read_text(encoding="utf-8")
    if raw.startswith("---"):
        end = raw.index("---", 3)
        raw = raw[end + 3:].lstrip()

    clean = clean_text(raw)
    chunks = split_chunks(clean)

    # Extract title from front matter for the scene header
    fm_raw = post_path.read_text(encoding="utf-8")
    title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', fm_raw, re.MULTILINE)
    title = title_match.group(1) if title_match else post_path.stem

    print(f"Post    : {post_path.name}")
    print(f"Chars   : {len(clean):,}")
    print(f"Chunks  : {len(chunks)}")
    print()

    client = genai.Client(api_key=api_key)
    tmp_dir = pathlib.Path(tempfile.mkdtemp())
    wav_paths = []

    try:
        for i, chunk in enumerate(chunks, 1):
            print(f"  [{i}/{len(chunks)}] {len(chunk)} chars ... ", end="", flush=True)
            wav = generate_chunk_wav(client, title, chunk)
            p = tmp_dir / f"chunk_{i}.wav"
            p.write_bytes(wav)
            wav_paths.append(p)
            print(f"{len(wav) // 1024} KB")
            if i < len(chunks):
                time.sleep(2)

        repo_root = post_path.parent.parent
        out_dir = repo_root / "assets" / "audio" / "posts"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{post_path.stem}.mp3"

        print(f"\nConverting to MP3 ... ", end="", flush=True)
        wav_files_to_mp3(wav_paths, out_path)
        print("done")

        size_mb = out_path.stat().st_size / (1024 * 1024)
        narration_src = f"/assets/audio/posts/{post_path.stem}.mp3"

        print(f"\nSaved   : {out_path}")
        print(f"Size    : {size_mb:.1f} MB")
        print()
        print("Add to post front matter:")
        print(f"  narration: true")
        print(f"  narration_src: \"{narration_src}\"")

    finally:
        for p in wav_paths:
            p.unlink(missing_ok=True)
        try:
            tmp_dir.rmdir()
        except OSError:
            pass


if __name__ == "__main__":
    main()
