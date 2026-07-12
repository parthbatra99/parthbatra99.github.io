import os
import re
import sys
import subprocess
import tempfile
from pathlib import Path

def get_rsvg_command():
    # Check if 'rsvg-convert' is in PATH
    try:
        result = subprocess.run(['rsvg-convert', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            return 'rsvg-convert'
    except FileNotFoundError:
        pass

    # Check common brew/system paths
    for path in ['/opt/homebrew/bin/rsvg-convert', '/usr/local/bin/rsvg-convert', '/usr/bin/rsvg-convert']:
        if os.path.exists(path):
            return path
    return None

def parse_viewbox(svg_tag: str):
    # Extract viewBox
    match = re.search(r'viewBox\s*=\s*["\']([^"\'\n]+)["\']', svg_tag, re.IGNORECASE)
    if match:
        try:
            parts = [float(x) for x in re.split(r'[\s,]+', match.group(1).strip())]
            if len(parts) == 4:
                return tuple(parts)
        except ValueError:
            pass
    
    # Fallback to width/height if viewBox is missing
    w_match = re.search(r'width\s*=\s*["\']([^"\'\n]+)["\']', svg_tag, re.IGNORECASE)
    h_match = re.search(r'height\s*=\s*["\']([^"\'\n]+)["\']', svg_tag, re.IGNORECASE)
    if w_match and h_match:
        try:
            w_str = re.sub(r'[^\d\.]', '', w_match.group(1))
            h_str = re.sub(r'[^\d\.]', '', h_match.group(1))
            return (0, 0, float(w_str), float(h_str))
        except ValueError:
            pass
            
    # Default fallback
    return (0, 0, 380, 150)

def generate_og_svg(inner_svg: str):
    start_match = re.match(r'^\s*<svg\b[^>]*>', inner_svg, re.IGNORECASE)
    if not start_match:
        return None
    
    start_tag = start_match.group(0)
    # Get the viewBox values
    x, y, w, h = parse_viewbox(start_tag)
    
    if w <= 0 or h <= 0:
        w, h = 380, 150
        
    # Get inner content (everything inside <svg>...</svg>)
    inner_content = inner_svg[start_match.end():]
    # Remove closing </svg>
    inner_content = re.sub(r'</svg>\s*$', '', inner_content, flags=re.IGNORECASE).strip()
    
    # Output canvas dimensions
    W_out = 1200
    H_out = 630
    
    # Bounding box dimensions (80% of outer dimensions)
    W_box = W_out * 0.8
    H_box = H_out * 0.8
    
    # Math for scaling and centering
    r_in = w / h
    r_box = W_box / H_box
    
    if r_in > r_box:
        # Width limited
        w_scaled = W_box
        h_scaled = W_box / r_in
    else:
        # Height limited
        h_scaled = H_box
        w_scaled = H_box * r_in
        
    scale = w_scaled / w
    
    # Center coordinates
    cx_out = W_out / 2.0
    cy_out = H_out / 2.0
    
    # Scaled center relative to viewBox offset
    cx_scaled = scale * (x + w / 2.0)
    cy_scaled = scale * (y + h / 2.0)
    
    # Translation offsets
    tx = cx_out - cx_scaled
    ty = cy_out - cy_scaled
    
    # Branded template
    parent_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W_out}" height="{H_out}" viewBox="0 0 {W_out} {H_out}">
  <defs>
    <filter id="sketch" x="-5%" y="-5%" width="110%" height="110%">
      <feTurbulence type="fractalNoise" baseFrequency="0.018" numOctaves="2" seed="7" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="2.2" xChannelSelector="R" yChannelSelector="G"/>
    </filter>
  </defs>
  <rect width="{W_out}" height="{H_out}" fill="#fafaf8"/>
  <g filter="url(#sketch)" style="color: #c1492b; fill: none; stroke: currentColor;" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
    <g transform="translate({tx:.4f}, {ty:.4f}) scale({scale:.6f})">
      {inner_content}
    </g>
  </g>
</svg>"""
    return parent_svg

def generate_default_og():
    W_out = 1200
    H_out = 630
    
    default_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W_out}" height="{H_out}" viewBox="0 0 {W_out} {H_out}">
  <defs>
    <filter id="sketch" x="-5%" y="-5%" width="110%" height="110%">
      <feTurbulence type="fractalNoise" baseFrequency="0.018" numOctaves="2" seed="7" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="2.2" xChannelSelector="R" yChannelSelector="G"/>
    </filter>
  </defs>
  <rect width="{W_out}" height="{H_out}" fill="#fafaf8"/>
  <rect x="40" y="40" width="1120" height="550" rx="15" fill="none" stroke="#c1492b" stroke-width="3" filter="url(#sketch)" opacity="0.3"/>
  <g filter="url(#sketch)">
    <text x="600" y="325" 
          font-family="Georgia, serif" 
          font-size="72" 
          font-style="italic" 
          font-weight="bold" 
          fill="#c1492b" 
          text-anchor="middle">fromparth.blog</text>
  </g>
</svg>"""
    return default_svg

def convert_svg_to_png(svg_content: str, output_path: Path, rsvg_cmd: str):
    # Create a temp file to hold the SVG
    with tempfile.NamedTemporaryFile(mode='w', suffix='.svg', delete=False) as temp_file:
        temp_file.write(svg_content)
        temp_path = temp_file.name

    try:
        # Run rsvg-convert
        cmd = [rsvg_cmd, '-o', str(output_path), temp_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error converting {output_path.name}: {result.stderr}")
            return False
        return True
    finally:
        # Ensure the temp file is deleted
        if os.path.exists(temp_path):
            os.remove(temp_path)

def process_posts():
    rsvg_cmd = get_rsvg_command()
    is_production = os.getenv('JEKYLL_ENV') == 'production'

    if not rsvg_cmd:
        msg = "Warning: rsvg-convert not found. Skipping SVG-to-PNG generation."
        if is_production:
            raise RuntimeError("Error: rsvg-convert is required in production environment but not found.")
        else:
            print(msg)
            return

    output_dir = Path('assets/images/generated')
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate default OG image first
    default_svg = generate_default_og()
    default_output = output_dir / 'default-og.png'
    if convert_svg_to_png(default_svg, default_output, rsvg_cmd):
        print(f"Generated default OG image: {default_output}")

    # Find all posts
    posts_dir = Path('_posts')
    if not posts_dir.exists():
        print("No _posts directory found.")
        return

    post_files = list(posts_dir.glob('*.md'))
    print(f"Found {len(post_files)} posts to scan.")

    # SVG matching regex
    svg_pattern = re.compile(r'<svg\b[^>]*>.*?</svg>', re.DOTALL | re.IGNORECASE)

    for post_path in post_files:
        try:
            with open(post_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {post_path}: {e}")
            continue

        # Find the first SVG in the post content
        match = svg_pattern.search(content)
        if match:
            inner_svg = match.group(0)
            slug = post_path.stem
            output_path = output_dir / f"{slug}.png"
            
            print(f"Processing post: {post_path.name}")
            wrapped_svg = generate_og_svg(inner_svg)
            if wrapped_svg:
                if convert_svg_to_png(wrapped_svg, output_path, rsvg_cmd):
                    print(f"  -> Generated: {output_path.name}")
                else:
                    print(f"  -> Failed to generate PNG for {slug}")
            else:
                print(f"  -> Failed to wrap SVG for {slug}")

if __name__ == '__main__':
    process_posts()
