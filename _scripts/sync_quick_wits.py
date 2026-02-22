#!/usr/bin/env python3
"""Sync quick-wits.md from latest tweets using X/Twitter API v2.

Usage:
  TWITTER_BEARER_TOKEN=... python _scripts/sync_quick_wits.py \
    --username batra99 --limit 120 --output quick-wits.md
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from urllib.error import HTTPError
from dataclasses import dataclass
from typing import Any

API_BASE = "https://api.twitter.com/2"
CACHE_PATH = ".cache/quick_wits_user_ids.json"
DEFAULT_FRONT_MATTER = """---
layout: quick-wits
title: QuickWits
description: Remember those 'unfiltered thoughts' and 'hot takes' I mentioned? This is where they often land first, mostly streamed from my twitter feed. Raw, rapid-fire, and probably less polished than my SQL queries.
permalink: /quick-wits/
---
"""


@dataclass
class TweetBundle:
    tweets: list[dict[str, Any]]
    includes_tweets: dict[str, dict[str, Any]]
    includes_users: dict[str, dict[str, Any]]


class RateLimitError(RuntimeError):
    def __init__(self, message: str, reset_in_seconds: int | None = None):
        super().__init__(message)
        self.reset_in_seconds = reset_in_seconds


class TwitterClient:
    def __init__(self, bearer_token: str):
        self.bearer_token = bearer_token

    def _get(self, path: str, params: dict[str, Any]) -> dict[str, Any]:
        query = urllib.parse.urlencode(params)
        url = f"{API_BASE}{path}?{query}"
        req = urllib.request.Request(url)
        req.add_header("Authorization", f"Bearer {self.bearer_token}")
        req.add_header("User-Agent", "quick-wits-sync/1.0")

        try:
            with urllib.request.urlopen(req) as resp:
                payload = resp.read().decode("utf-8")
                return json.loads(payload)
        except HTTPError as exc:
            raw = exc.read().decode("utf-8", errors="replace")
            try:
                api_error = json.loads(raw)
                detail = api_error.get("detail") or api_error.get("title") or raw
            except json.JSONDecodeError:
                detail = raw or str(exc)

            if exc.code == 429:
                retry_after = exc.headers.get("retry-after")
                reset_epoch = exc.headers.get("x-rate-limit-reset")
                hint_parts = []
                wait_seconds = None
                if retry_after:
                    hint_parts.append(f"retry after ~{retry_after}s")
                if reset_epoch and reset_epoch.isdigit():
                    wait_seconds = max(0, int(reset_epoch) - int(time.time()))
                    hint_parts.append(f"rate window resets in ~{wait_seconds}s")
                hint = f" ({'; '.join(hint_parts)})" if hint_parts else ""
                raise RateLimitError(
                    f"HTTP 429 Too Many Requests{hint}. API says: {detail}",
                    reset_in_seconds=wait_seconds,
                ) from exc

            raise RuntimeError(f"HTTP {exc.code}. API says: {detail}") from exc

    def get_user(self, username: str) -> dict[str, Any]:
        data = self._get(
            f"/users/by/username/{urllib.parse.quote(username)}",
            {"user.fields": "name,username"},
        )
        return data["data"]

    def get_recent_tweets(
        self,
        user_id: str,
        limit: int,
        include_replies: bool,
    ) -> TweetBundle:
        tweets: list[dict[str, Any]] = []
        includes_tweets: dict[str, dict[str, Any]] = {}
        includes_users: dict[str, dict[str, Any]] = {}
        page_token: str | None = None

        while len(tweets) < limit:
            max_results = min(100, limit - len(tweets))
            excludes = ["retweets"]
            if not include_replies:
                excludes.append("replies")

            params: dict[str, Any] = {
                "max_results": max_results,
                "exclude": ",".join(excludes),
                "tweet.fields": "author_id,created_at,entities,referenced_tweets,text",
                "expansions": "author_id,referenced_tweets.id,referenced_tweets.id.author_id",
                "user.fields": "name,username",
            }
            if page_token:
                params["pagination_token"] = page_token

            try:
                payload = self._get(f"/users/{user_id}/tweets", params)
            except RateLimitError:
                if tweets:
                    break
                raise
            batch = payload.get("data", [])
            if not batch:
                break

            tweets.extend(batch)

            includes = payload.get("includes", {})
            for included_tweet in includes.get("tweets", []):
                includes_tweets[included_tweet["id"]] = included_tweet
            for included_user in includes.get("users", []):
                includes_users[included_user["id"]] = included_user

            page_token = payload.get("meta", {}).get("next_token")
            if not page_token:
                break

        return TweetBundle(
            tweets=tweets[:limit],
            includes_tweets=includes_tweets,
            includes_users=includes_users,
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch latest tweets and regenerate quick-wits markdown."
    )
    parser.add_argument("--username", required=True, help="Twitter/X username without @")
    parser.add_argument(
        "--user-id",
        help="Optional X user id to skip username lookup (useful for strict free-tier limits)",
    )
    parser.add_argument(
        "--display-name",
        help="Optional display name used in quick-wits cards when --user-id is set",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Maximum number of latest tweets to pull (default: 100)",
    )
    parser.add_argument(
        "--output",
        default="quick-wits.md",
        help="Output markdown path (default: quick-wits.md)",
    )
    parser.add_argument(
        "--include-replies",
        action="store_true",
        help="Include reply tweets (default: false)",
    )
    return parser.parse_args()


def load_user_id_cache() -> dict[str, str]:
    try:
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return {str(k): str(v) for k, v in data.items()}
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}
    return {}


def save_user_id_cache(cache: dict[str, str]) -> None:
    os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2, sort_keys=True)
        f.write("\n")


def extract_front_matter(content: str) -> tuple[str, str]:
    if not content.startswith("---\n"):
        return DEFAULT_FRONT_MATTER, content

    second = content.find("\n---\n", 4)
    if second == -1:
        return DEFAULT_FRONT_MATTER, content

    front_matter = content[: second + 5].strip() + "\n"
    body = content[second + 5 :]
    return front_matter, body


def escape_and_linkify(text: str, entities: dict[str, Any] | None) -> str:
    if not entities or "urls" not in entities:
        return html.escape(text).replace("\n", "<br>")

    urls = sorted(entities.get("urls", []), key=lambda u: u.get("start", 0))
    out: list[str] = []
    cursor = 0

    for url in urls:
        start = url.get("start")
        end = url.get("end")
        if start is None or end is None or start < cursor:
            continue

        out.append(html.escape(text[cursor:start]))

        expanded = url.get("expanded_url") or url.get("url") or ""
        display = url.get("display_url") or expanded
        safe_expanded = html.escape(expanded, quote=True)
        safe_display = html.escape(display)
        out.append(
            f'<a href="{safe_expanded}" target="_blank" rel="noopener">{safe_display}</a>'
        )
        cursor = end

    out.append(html.escape(text[cursor:]))
    return "".join(out).replace("\n", "<br>")


def tweet_month_key(created_at: str) -> str:
    parsed = dt.datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    return parsed.strftime("%B %Y")


def tweet_date_label(created_at: str) -> str:
    parsed = dt.datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    return parsed.strftime("%b %d")


def month_slug(month_label: str) -> str:
    return month_label.lower().replace(" ", "-")


def build_tweet_html(
    tweet: dict[str, Any],
    username: str,
    display_name: str,
    includes_tweets: dict[str, dict[str, Any]],
    includes_users: dict[str, dict[str, Any]],
) -> str:
    tweet_text = escape_and_linkify(tweet.get("text", ""), tweet.get("entities"))
    tweet_url = f"https://twitter.com/{username}/status/{tweet['id']}"
    quoted = None

    for ref in tweet.get("referenced_tweets", []):
        if ref.get("type") == "quoted":
            quoted = includes_tweets.get(ref.get("id", ""))
            break

    quote_html = ""
    if quoted:
        quote_text = escape_and_linkify(quoted.get("text", ""), quoted.get("entities"))
        quote_author_id = quoted.get("author_id")
        quote_author = includes_users.get(quote_author_id, {}) if quote_author_id else {}
        quote_handle = quote_author.get("username")
        quote_source = ""
        if quote_handle:
            quote_source = f" <em>(quoted @{html.escape(quote_handle)})</em>"
        quote_html = f"<br><em>Quoted:</em> {quote_text}{quote_source}"

    date_label = tweet_date_label(tweet["created_at"])
    safe_name = html.escape(display_name)
    safe_handle = html.escape(username)

    return "\n".join(
        [
            '<article class="tweet-entry">',
            '  <div class="tweet-header">',
            f'    <img src="/assets/images/profile.jpg" alt="{safe_name}" class="tweet-avatar">',
            '    <div class="tweet-user-info">',
            f'      <span class="tweet-name">{safe_name}</span>',
            f'      <span class="tweet-handle">@{safe_handle}</span>',
            '    </div>',
            f'    <span class="tweet-date">{date_label}</span>',
            '  </div>',
            '  <div class="tweet-content">',
            f'    {tweet_text}{quote_html}',
            '  </div>',
            '  <div class="tweet-footer">',
            f'    <a href="{html.escape(tweet_url, quote=True)}" target="_blank" class="tweet-action">🔗 View Tweet</a>',
            '  </div>',
            "</article>",
        ]
    )


def render_body(
    tweets: list[dict[str, Any]],
    username: str,
    display_name: str,
    includes_tweets: dict[str, dict[str, Any]],
    includes_users: dict[str, dict[str, Any]],
) -> str:
    if not tweets:
        return "No tweets found."

    lines: list[str] = []
    current_month = None
    current_month_index = 0

    for tweet in tweets:
        month = tweet_month_key(tweet["created_at"])
        if month != current_month:
            if current_month is not None:
                lines.append("  </div>")
                lines.append("</section>\n")

            month_id = f"qw-month-{month_slug(month)}-{current_month_index + 1}"
            is_latest_month = current_month_index == 0
            expanded = "true" if is_latest_month else "false"
            collapsed_class = "" if is_latest_month else " is-collapsed"
            lines.append(f'<section class="qw-month{collapsed_class}">')
            lines.append(
                f'  <button type="button" class="qw-month-toggle" aria-expanded="{expanded}" aria-controls="{month_id}">'
            )
            lines.append(f'    <span class="qw-month-label">{html.escape(month)}</span>')
            lines.append('    <span class="qw-month-caret" aria-hidden="true"></span>')
            lines.append("  </button>")
            lines.append(f'  <div class="qw-month-body" id="{month_id}">')
            current_month = month
            current_month_index += 1

        lines.append(
            build_tweet_html(
                tweet=tweet,
                username=username,
                display_name=display_name,
                includes_tweets=includes_tweets,
                includes_users=includes_users,
            )
        )
        lines.append("")

    if current_month is not None:
        lines.append("  </div>")
        lines.append("</section>")

    return "\n".join(lines).strip() + "\n"


def main() -> int:
    args = parse_args()

    token = os.environ.get("TWITTER_BEARER_TOKEN") or os.environ.get("X_BEARER_TOKEN")
    if not token:
        print(
            "Missing bearer token. Set TWITTER_BEARER_TOKEN (or X_BEARER_TOKEN).",
            file=sys.stderr,
        )
        return 1

    client = TwitterClient(token)
    cache = load_user_id_cache()
    resolved_user_id = args.user_id or cache.get(args.username.lower())
    resolved_username = args.username
    resolved_name = args.display_name or args.username

    try:
        if not resolved_user_id:
            user = client.get_user(args.username)
            resolved_user_id = user["id"]
            resolved_username = user["username"]
            resolved_name = user["name"]
            cache[resolved_username.lower()] = resolved_user_id
            cache[args.username.lower()] = resolved_user_id
            save_user_id_cache(cache)

        bundle = client.get_recent_tweets(
            user_id=resolved_user_id,
            limit=args.limit,
            include_replies=args.include_replies,
        )
        if bundle.includes_users:
            for u in bundle.includes_users.values():
                if u.get("id") == resolved_user_id:
                    resolved_username = u.get("username", resolved_username)
                    resolved_name = u.get("name", resolved_name)
                    break
    except Exception as exc:  # noqa: BLE001
        print(f"Failed to fetch tweets: {exc}", file=sys.stderr)
        return 1

    front_matter = DEFAULT_FRONT_MATTER
    if os.path.exists(args.output):
        with open(args.output, "r", encoding="utf-8") as f:
            existing = f.read()
        front_matter, _ = extract_front_matter(existing)

    body = render_body(
        tweets=bundle.tweets,
        username=resolved_username,
        display_name=resolved_name,
        includes_tweets=bundle.includes_tweets,
        includes_users=bundle.includes_users,
    )

    final = front_matter.rstrip() + "\n\n" + body
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(final)

    print(f"Updated {args.output} with {len(bundle.tweets)} tweets from @{resolved_username}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
