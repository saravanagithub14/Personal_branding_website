"""Pixel-art icon system for the site (Pixelarticons, MIT, by Gerrit Halfmann).

One icons map (assets/icons/icons.json) and one helper, icon(name), which returns the
inline SVG every page uses. Icons are inlined into the static HTML at edit time, so
nothing is loaded at runtime and no third-party API is called.

Usage (from the repo root):

    python tools/icons.py render
        Expand every <i class="ico ico-NAME"></i> placeholder in the site's pages into the
        inline SVG, and re-sync every existing <svg class="ico ico-NAME ..."> from the map.
        Extra classes after ico-NAME are kept. Safe to run any time.

    python tools/icons.py test-page
        Write tools/icon-test.html: every icon at 24px and 48px on light and dark.

    python tools/icons.py build-map path/to/@iconify-json/pixelarticons/icons.json
        Rebuild assets/icons/icons.json from the npm package
        @iconify-json/pixelarticons (version 1.2.9 to match the portfolio site).

Rules (from the portfolio site's icon spec): 24x24 grid of filled 2-unit squares,
fill="currentColor", shape-rendering="crispEdges", aria-hidden. Show at 24px or a whole
multiple (48, 72...). No emoji anywhere; icons replace them.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAP_FILE = ROOT / "assets" / "icons" / "icons.json"
FALLBACK = "circle-dot"

# Site icon name -> Pixelarticons icon. Same names as the portfolio site, so both mean the same thing.
SOURCES = {
    "arrow-right": "arrow-right", "arrow-up-right": "external-link", "award": "trophy",
    "book-open": "book-open", "bot": "robot", "briefcase": "briefcase", "camera": "camera",
    "chart-column": "chart-bar", "circle-dot": "circle", "clapperboard": "movie",
    "code-xml": "code", "cpu": "cpu", "eye": "eye", "file-text": "file-text",
    "flask-conical": "potion", "github": "github", "globe": "globe", "handshake": "users",
    "hard-hat": "ai-scan", "heart": "heart", "hospital": "plus-box", "id-card": "card-id",
    "image": "image", "instagram": "instagram", "landmark": "building", "laptop": "laptop",
    "layers": "card-stack", "leaf": "leaf", "library": "library", "lightbulb": "lightbulb",
    "linkedin": "linkedin", "mail": "mail", "map-pin": "map-pin", "medal": "trophy",
    "medium": "article", "menu": "menu", "message-circle": "message", "mic": "mic",
    "network": "git-branch", "notebook-pen": "notebook", "orcid": "card-id", "pen-line": "pencil",
    "presentation": "teach", "researchgate": "article", "rocket": "trending-up", "scan": "ai-scan",
    "scan-eye": "ai-view", "scan-search": "zoom-in", "scroll-text": "article", "search": "search",
    "settings": "settings-cog", "star": "star", "swords": "sword", "target": "bullseye",
    "terminal": "terminal", "users": "users", "video": "video", "workflow": "git-merge",
    "wrench": "tools",
    # Extras this site needs (closest Pixelarticons icon, not in the portfolio list)
    "arrow-down": "arrow-down", "chevron-down": "chevron-down", "x": "close",
    "whatsapp": "whatsapp",
}

# Pixelarticons has no equivalent for these; exact paths from the portfolio site.
CUSTOM = {
    "brain": '<path fill="currentColor" d="M6 2h4v2h-4zM14 2h4v2h-4zM4 4h2v2h-2zM10 4h4v2h-4zM18 4h2v2h-2zM2 6h2v2h-2zM12 6h2v2h-2zM20 6h2v2h-2zM2 8h2v2h-2zM6 8h4v2h-4zM12 8h2v2h-2zM16 8h2v2h-2zM20 8h2v2h-2zM0 10h2v2h-2zM10 10h2v2h-2zM14 10h2v2h-2zM20 10h2v2h-2zM0 12h2v2h-2zM4 12h2v2h-2zM10 12h2v2h-2zM16 12h4v2h-4zM22 12h2v2h-2zM2 14h2v2h-2zM6 14h4v2h-4zM12 14h2v2h-2zM22 14h2v2h-2zM2 16h2v2h-2zM12 16h2v2h-2zM16 16h4v2h-4zM22 16h2v2h-2zM4 18h4v2h-4zM12 18h2v2h-2zM20 18h2v2h-2zM8 20h4v2h-4zM14 20h6v2h-6z"/>',
    "dna": '<path fill="currentColor" d="M4 0h2v2h-2zM18 0h2v2h-2zM4 2h16v2h-16zM6 4h2v2h-2zM16 4h2v2h-2zM8 6h2v2h-2zM14 6h2v2h-2zM10 8h4v2h-4zM8 10h2v2h-2zM14 10h2v2h-2zM6 12h2v2h-2zM16 12h2v2h-2zM4 14h16v2h-16zM4 16h2v2h-2zM18 16h2v2h-2zM6 18h2v2h-2zM16 18h2v2h-2zM8 20h2v2h-2zM14 20h2v2h-2zM10 22h4v2h-4z"/>',
    "graduation-cap": '<path fill="currentColor" d="M8 4h8v2h-8zM4 6h4v2h-4zM16 6h4v2h-4zM0 8h4v2h-4zM20 8h4v2h-4zM4 10h4v2h-4zM16 10h4v2h-4zM22 10h2v2h-2zM4 12h2v2h-2zM8 12h8v2h-8zM18 12h2v2h-2zM22 12h2v2h-2zM4 14h2v2h-2zM18 14h2v2h-2zM22 14h2v2h-2zM4 16h2v2h-2zM18 16h2v2h-2zM22 16h2v2h-2zM6 18h12v2h-12z"/>',
    "microscope": '<path fill="currentColor" d="M8 0h4v2h-4zM6 2h8v2h-8zM8 4h4v2h-4zM8 6h4v2h-4zM16 6h4v2h-4zM8 8h4v2h-4zM18 8h2v2h-2zM6 10h8v2h-8zM18 10h2v2h-2zM8 12h4v2h-4zM18 12h2v2h-2zM16 14h2v2h-2zM4 16h12v2h-12zM2 20h20v2h-20z"/>',
}

_cache: dict | None = None


def icons() -> dict[str, str]:
    global _cache
    if _cache is None:
        _cache = json.loads(MAP_FILE.read_text(encoding="utf-8"))["icons"]
    return _cache


def icon(name: str, extra_class: str = "") -> str:
    """Inline SVG for a site icon name. Unknown names get the circle-dot fallback but keep
    their own ico-NAME class, so adding the icon to the map later fixes them on re-render."""
    body = icons().get(name) or icons()[FALLBACK]
    cls = f"ico ico-{name}" + (f" {extra_class.strip()}" if extra_class.strip() else "")
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="currentColor" shape-rendering="crispEdges" '
            f'aria-hidden="true" focusable="false">{body}</svg>')


# ---------------------------------------------------------------- commands

def build_map(package_icons_json: str) -> None:
    data = json.loads(Path(package_icons_json).read_text(encoding="utf-8"))
    pack = data["icons"]
    out, missing = {}, []
    for name, source in sorted(SOURCES.items()):
        entry = pack.get(source)
        if not entry or entry.get("width", 24) != 24 or entry.get("height", 24) != 24:
            missing.append(source)
            continue
        out[name] = entry["body"]
    out.update(CUSTOM)
    if missing:
        raise SystemExit(f"Not found (or not 24x24) in the package: {missing}")
    MAP_FILE.parent.mkdir(parents=True, exist_ok=True)
    MAP_FILE.write_text(json.dumps({
        "about": "Site icon name -> SVG body on a 24x24 grid. Generated by tools/icons.py build-map.",
        "source": "Pixelarticons by Gerrit Halfmann (MIT), via @iconify-json/pixelarticons 1.2.9; "
                  "brain, dna, graduation-cap and microscope are custom icons from the portfolio site.",
        "icons": dict(sorted(out.items())),
    }, indent=1), encoding="utf-8", newline="\n")
    print(f"wrote {MAP_FILE.relative_to(ROOT)}: {len(out)} icons")


def site_pages() -> list[Path]:
    pages = sorted(ROOT.glob("*.html"))
    for d in sorted(p for p in ROOT.iterdir() if p.is_dir() and not p.name.startswith(".")):
        if d.name in {"mcp_server", "tools", "assets", "node_modules"}:
            continue
        if (d / "index.html").is_file():
            pages.append(d / "index.html")
    return pages


_PLACEHOLDER = re.compile(r'<i class="ico ico-([a-z0-9-]+)((?: [^"]*)?)"></i>')
_RENDERED = re.compile(r'<svg class="ico ico-([a-z0-9-]+)((?: [^"]*)?)"[^>]*>.*?</svg>', re.S)


_COMMENT = re.compile(r"(<!--.*?-->)", re.S)


def render_text(html: str) -> str:
    """Render icons everywhere except inside HTML comments (which may hold copy-me templates)."""
    parts = _COMMENT.split(html)
    for i in range(0, len(parts), 2):        # even indexes are outside comments
        part = _PLACEHOLDER.sub(lambda m: icon(m.group(1), m.group(2)), parts[i])
        parts[i] = _RENDERED.sub(lambda m: icon(m.group(1), m.group(2)), part)
    return "".join(parts)


def render() -> None:
    unknown = set()
    for page in site_pages():
        with open(page, encoding="utf-8", newline="") as f:
            html = f.read()
        visible = _COMMENT.sub("", html)
        for m in list(_PLACEHOLDER.finditer(visible)) + list(_RENDERED.finditer(visible)):
            if m.group(1) not in icons():
                unknown.add(m.group(1))
        new = render_text(html)
        if new != html:
            with open(page, "w", encoding="utf-8", newline="") as f:
                f.write(new)
            print("rendered", page.relative_to(ROOT))
    if unknown:
        print("WARNING: unknown icon names (showing the circle-dot fallback):", sorted(unknown))


def test_page() -> None:
    names = sorted(icons())
    cells = "\n".join(
        f'      <figure><div class="row">{icon(n)}{icon(n, "ico-48")}</div><figcaption>{n}</figcaption></figure>'
        for n in names)
    unknown_demo = icon("not-a-real-icon")
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow">
  <title>Pixel icon test</title>
  <style>
    :root {{ --ivory:#FAF6EC; --slate:#3F4650; --ink:#1E2F57; }}
    body {{ margin:0; font:16px/1.4 "Times New Roman", serif; background:var(--ivory); color:var(--slate); }}
    header {{ padding:24px 16px 8px; max-width:1200px; margin:0 auto; }}
    h1 {{ margin:0 0 4px; color:var(--ink); }}
    section {{ padding:24px 16px; }}
    section > div {{ max-width:1200px; margin:0 auto; }}
    .dark {{ background:var(--slate); color:var(--ivory); }}
    .ink {{ background:var(--ink); color:var(--ivory); }}
    h2 {{ margin:0 0 16px; font-size:18px; }}
    .grid {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(120px, 1fr)); gap:8px; }}
    figure {{ margin:0; padding:12px; border:1px solid currentColor; border-color:rgba(127,127,127,.35); }}
    .row {{ display:flex; align-items:center; gap:16px; height:48px; }}
    figcaption {{ margin-top:8px; font-size:13px; font-family:monospace; }}
    /* Base CSS from the spec */
    .ico {{ display:block; width:1em; height:1em; flex-shrink:0; }}
    svg.ico {{ font-size:24px; }}
    svg.ico.ico-48 {{ font-size:48px; }}
  </style>
</head>
<body>
  <header>
    <h1>Pixel icon test</h1>
    <p>{len(names)} icons, each at 24px and 48px. Unknown name fallback: {unknown_demo}</p>
  </header>
  <section><div><h2>Light: slate on ivory</h2><div class="grid">
{cells}
  </div></div></section>
  <section class="dark"><div><h2>Dark: ivory on slate</h2><div class="grid">
{cells}
  </div></div></section>
  <section class="ink"><div><h2>Dark: ivory on ink blue</h2><div class="grid">
{cells}
  </div></div></section>
</body>
</html>
"""
    out = ROOT / "tools" / "icon-test.html"
    out.write_text(html, encoding="utf-8", newline="\n")
    print(f"wrote {out.relative_to(ROOT)} ({len(names)} icons)")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "render":
        render()
    elif cmd == "test-page":
        test_page()
    elif cmd == "build-map" and len(sys.argv) > 2:
        build_map(sys.argv[2])
    else:
        print(__doc__)
        sys.exit(1)
