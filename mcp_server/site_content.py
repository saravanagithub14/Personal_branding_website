"""Read the static website and turn its pages into plain data.

The HTML pages are the single source of truth: nothing here is hard-coded, so the
MCP server always answers with what the live site says. Only the standard library
is used. Pages are re-parsed when their file changes on disk.
"""
from __future__ import annotations

import os
import posixpath
import re
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote

# --------------------------------------------------------------------------- paths

SITE_ROOT = Path(os.environ.get("SITE_ROOT") or Path(__file__).resolve().parent.parent)

# Public base URL, e.g. "https://example.com". Unset until the domain is live.
SITE_BASE_URL = (os.environ.get("SITE_BASE_URL") or "").rstrip("/")

# Folders that are never part of the public site.
_EXCLUDED_DIRS = {"mcp_server", "assets", "node_modules", ".git", ".venv", "venv", "__pycache__"}


# --------------------------------------------------------------------------- tiny DOM

_VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
         "source", "track", "wbr"}
_SKIP = {"script", "style", "noscript", "svg", "template", "head"}
_BLOCK = {"address", "article", "aside", "blockquote", "br", "dd", "details", "div", "dl",
          "dt", "figcaption", "figure", "footer", "form", "h1", "h2", "h3", "h4", "h5",
          "h6", "header", "hr", "li", "main", "nav", "ol", "p", "section", "summary",
          "table", "tr", "ul"}


class Node:
    __slots__ = ("tag", "attrs", "children", "parent")

    def __init__(self, tag: str, attrs: dict[str, str], parent: "Node | None"):
        self.tag = tag
        self.attrs = attrs
        self.children: list[Node | str] = []
        self.parent = parent

    # -- queries
    @property
    def classes(self) -> list[str]:
        return (self.attrs.get("class") or "").split()

    def iter(self):
        yield self
        for child in self.children:
            if isinstance(child, Node):
                yield from child.iter()

    def find_all(self, tag: str | None = None, cls: str | None = None,
                 attr: str | None = None) -> list["Node"]:
        out = []
        for node in self.iter():
            if node is self:
                continue
            if tag and node.tag != tag:
                continue
            if cls and cls not in node.classes:
                continue
            if attr and attr not in node.attrs:
                continue
            out.append(node)
        return out

    def find(self, tag: str | None = None, cls: str | None = None,
             attr: str | None = None) -> "Node | None":
        found = self.find_all(tag, cls, attr)
        return found[0] if found else None

    # -- text
    def text(self) -> str:
        """Visible text. Skips scripts and anything marked aria-hidden (image
        placeholders, decorative skeletons), so only real content comes back."""
        parts: list[str] = []
        self._collect(parts)
        lines = [re.sub(r"[ \t\r\f\v]+", " ", line).strip() for line in "".join(parts).split("\n")]
        return "\n".join(line for line in lines if line)

    def inline_text(self) -> str:
        return " ".join(self.text().split())

    def _collect(self, parts: list[str]) -> None:
        if self.tag in _SKIP or self.attrs.get("aria-hidden") == "true":
            return
        block = self.tag in _BLOCK
        if block:
            parts.append("\n")
        for child in self.children:
            if isinstance(child, Node):
                child._collect(parts)
            else:
                parts.append(child)
        if block:
            parts.append("\n")


class _Builder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#document", {}, None)
        self.current = self.root

    def handle_starttag(self, tag, attrs):
        node = Node(tag, {k: (v or "") for k, v in attrs}, self.current)
        self.current.children.append(node)
        if tag not in _VOID:
            self.current = node

    def handle_startendtag(self, tag, attrs):
        self.current.children.append(Node(tag, {k: (v or "") for k, v in attrs}, self.current))

    def handle_endtag(self, tag):
        node = self.current
        while node is not None and node.tag != tag:
            node = node.parent
        if node is not None and node.parent is not None:
            self.current = node.parent

    def handle_data(self, data):
        self.current.children.append(data)


def parse_html(source: str) -> Node:
    builder = _Builder()
    builder.feed(source)
    builder.close()
    return builder.root


# --------------------------------------------------------------------------- pages

@dataclass(frozen=True)
class Page:
    slug: str          # "home", "about", "ai-trainer-in-kerala", ...
    file: str          # path relative to SITE_ROOT, posix style
    path: str          # public URL path, e.g. "/about.html", "/ai-mentor/"

    @property
    def url(self) -> str | None:
        return f"{SITE_BASE_URL}{self.path}" if SITE_BASE_URL else None


_cache: dict[str, tuple[float, Node]] = {}


def _file_to_path(rel: str) -> str:
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def _slug_for(rel: str) -> str:
    if rel == "index.html":
        return "home"
    if rel.endswith("/index.html"):
        return rel.split("/")[0]
    return rel[: -len(".html")]


def discover_pages() -> list[Page]:
    files: list[str] = []
    for item in sorted(SITE_ROOT.iterdir()):
        if item.is_file() and item.suffix == ".html":
            files.append(item.name)
        elif item.is_dir() and item.name not in _EXCLUDED_DIRS and not item.name.startswith("."):
            if (item / "index.html").is_file():
                files.append(f"{item.name}/index.html")
    pages = [Page(_slug_for(f), f, _file_to_path(f)) for f in files]
    # Home first, then top-level pages, then the service landing pages
    return sorted(pages, key=lambda p: (p.slug != "home", "/" in p.file, p.file))


def get_page(slug: str) -> Page:
    for page in discover_pages():
        if page.slug == slug:
            return page
    valid = ", ".join(p.slug for p in discover_pages())
    raise ValueError(f"Unknown page '{slug}'. Valid pages: {valid}")


def document(page: Page) -> Node:
    file = SITE_ROOT / page.file
    mtime = file.stat().st_mtime
    cached = _cache.get(page.file)
    if cached and cached[0] == mtime:
        return cached[1]
    dom = parse_html(file.read_text(encoding="utf-8"))
    _cache[page.file] = (mtime, dom)
    return dom


def main_node(page: Page) -> Node:
    dom = document(page)
    return dom.find("main") or dom.find("body") or dom


def page_title(page: Page) -> str:
    node = document(page).find("title")
    return node.inline_text() if node else page.slug


def page_description(page: Page) -> str:
    for meta in document(page).find_all("meta"):
        if meta.attrs.get("name") == "description":
            return meta.attrs.get("content", "")
    return ""


def resolve_link(page: Page, href: str) -> str:
    """Turn a relative href found on `page` into a public URL path (or keep absolute URLs)."""
    if re.match(r"^[a-z]+:", href):
        return href
    target, _, fragment = href.partition("#")
    base_dir = posixpath.dirname(page.file)
    rel = posixpath.normpath(posixpath.join(base_dir, target)) if target else page.file
    path = _file_to_path(rel)
    return path + (f"#{fragment}" if fragment else "")


# --------------------------------------------------------------------------- structured content

def services() -> list[dict]:
    page = get_page("services")
    grid = main_node(page).find("ul", cls="services-grid")
    out = []
    for card in grid.find_all("li", cls="service") if grid else []:
        link = card.find("a", cls="service-link")
        href = resolve_link(page, link.attrs["href"]) if link else None
        out.append({
            "name": card.find("h3").inline_text(),
            "description": card.find("p").inline_text(),
            "details_page": href if href and not href.startswith("/contact") else None,
        })
    return out


def experience() -> list[dict]:
    page = get_page("experience")
    out = []
    for group in main_node(page).find_all("div", cls="timeline-group"):
        if "timeline-group--education" in group.classes:
            continue  # degrees live in the same page; see education()
        title_node = group.find(cls="timeline-group-title")
        group_title = title_node.inline_text() if title_node else ""
        area = "research" if "research" in group_title.lower() else "ai"
        timeline = group.find("ol", cls="timeline")
        for item in timeline.children if timeline else []:
            if not isinstance(item, Node) or item.tag != "li":
                continue
            body = item.find(cls="timeline-body")
            heading = body.find("h3") or body.find("h4")
            org = body.find("p", cls="timeline-org")
            desc = body.find("p", cls="timeline-desc")
            tags = body.find("ul", cls="tags")
            out.append({
                "area": area,
                "area_label": group_title,
                "dates": item.find(cls="timeline-when").inline_text(),
                "title": heading.inline_text() if heading else "",
                "organisation": org.inline_text() if org else "",
                "description": desc.inline_text() if desc else "",
                "skills": [li.inline_text() for li in tags.find_all("li")] if tags else [],
                "current": "is-current" in item.classes,
            })
    return out


def education() -> dict:
    """Degrees and qualifications, from the Education section of the Experience page."""
    page = get_page("experience")
    section = next((n for n in main_node(page).find_all("section") if n.attrs.get("id") == "education"), None)
    if section is None:
        return {"degrees": [], "qualifications": []}
    degrees = []
    group = section.find("div", cls="timeline-group--education")
    timeline = group.find("ol", cls="timeline") if group else None
    for item in timeline.children if timeline else []:
        if not isinstance(item, Node) or item.tag != "li":
            continue
        body = item.find(cls="timeline-body")
        tags = body.find("ul", cls="tags")
        degrees.append({
            "dates": item.find(cls="timeline-when").inline_text(),
            "degree": (body.find("h4") or body.find("h3")).inline_text(),
            "institution": body.find("p", cls="timeline-org").inline_text(),
            "details": " ".join(p.inline_text() for p in body.find_all("p", cls="timeline-desc")),
            "subjects": [li.inline_text() for li in tags.find_all("li")] if tags else [],
        })
    qualifications = []
    for card in section.find_all("div", cls="qual-card"):
        head = card.find(cls="qual-head")
        name = head.inline_text() if head else ""
        text = card.inline_text()
        qualifications.append({"name": name, "details": text[len(name):].strip() if text.startswith(name) else text})
    return {"degrees": degrees, "qualifications": qualifications}


def skills() -> dict:
    """Focus areas and skill groups from the Skills page."""
    page = get_page("skills")
    main = main_node(page)
    focus = [{"area": c.find("h3").inline_text(), "note": c.find("p").inline_text()}
             for c in main.find_all("a", cls="focus-card")]
    groups = []
    for group in main.find_all("div", cls="skill-group"):
        head = group.find(cls="skill-group-head")
        groups.append({
            "id": group.attrs.get("id"),
            "group": head.find("h3").inline_text(),
            "summary": head.find("p").inline_text(),
            "skills": [{"name": t.find("strong").inline_text(), "note": t.find("span").inline_text()}
                       for t in group.find_all("li", cls="skill-tile")],
        })
    return {"focus_areas": focus, "groups": groups}


def publications() -> dict:
    """Stats and publications from the Publications page."""
    page = get_page("publications")
    main = main_node(page)
    stats_node = main.find("dl", cls="pubs-stats")
    stats = {}
    for item in stats_node.find_all("div") if stats_node else []:
        dt, dd = item.find("dt"), item.find("dd")
        if dt and dd:
            stats[dd.inline_text()] = dt.inline_text()
    items = []
    for card in main.find_all("article", cls="pubs-card"):
        title = card.find("h3", cls="pubs-title")
        link = title.find("a") if title else None
        tags = card.find("ul", cls="tags")
        items.append({
            "type": card.find("p", cls="pub-type").inline_text(),
            "title": title.inline_text() if title else "",
            "url": link.attrs.get("href") if link else None,
            "authors": (card.find("p", cls="pubs-authors") or Node("p", {}, None)).inline_text(),
            "venue": (card.find("p", cls="pubs-meta") or Node("p", {}, None)).inline_text(),
            "summary": (card.find("p", cls="pubs-summary") or Node("p", {}, None)).inline_text(),
            "topics": [li.inline_text() for li in tags.find_all("li")] if tags else [],
        })
    return {"stats": stats, "publications": items}


def projects() -> list[dict]:
    page = get_page("projects")
    out = []
    for card in main_node(page).find_all("li", cls="service"):
        tags = card.find("ul", cls="tags")
        link = card.find("a", cls="service-link")
        out.append({
            "name": card.find("h3").inline_text(),
            "description": card.find("p").inline_text(),
            "tools": [li.inline_text() for li in tags.find_all("li")] if tags else [],
            "link": link.attrs.get("href") if link else None,
        })
    return out


def faq() -> list[dict]:
    """The canonical FAQ, from the AI trainer in Kerala page (the one with FAQPage schema)."""
    page = get_page("ai-trainer-in-kerala")
    out = []
    for item in main_node(page).find_all("details", attr="data-faq-item"):
        q = item.find(attr="data-faq-q")
        a = item.find(attr="data-faq-a")
        if q and a:
            out.append({"question": q.inline_text(), "answer": a.inline_text()})
    return out


def contact() -> dict:
    page = get_page("contact")
    dom = document(page)
    main = main_node(page)
    links = [a.attrs.get("href", "") for a in dom.find_all("a")]

    email = next((h[len("mailto:"):].split("?")[0] for h in links if h.startswith("mailto:")), None)
    whatsapp = next((h.split("?")[0] for h in links if h.startswith("https://wa.me/")), None)
    profiles = {}
    for social in dom.find_all("ul", cls="footer-social"):
        for a in social.find_all("a"):
            profiles[a.inline_text()] = a.attrs.get("href")
    address = dom.find("address")
    cities = main.find("ul", cls="cities")
    answers = {item["question"]: item["answer"] for item in faq()}
    return {
        "email": email,
        "whatsapp_link": whatsapp,
        "profiles": profiles,
        "based_in": address.inline_text() if address else None,
        "in_person_cities": [li.inline_text() for li in cities.find_all("li")] if cities else [],
        "how_to_book": answers.get("How do I book you?"),
        "fees": answers.get("What are your fees for AI training?"),
        "contact_page": "/contact.html",
    }


def draft_enquiry(name: str, interest: str, goal: str, organisation: str = "",
                  city: str = "", group_size: str = "") -> dict:
    """Same message the contact form builds, with ready-to-open WhatsApp and email links."""
    lines = [f"Hi Saravana, I'm {name.strip()}."]
    for label, value in (("Interested in", interest), ("Organisation", organisation),
                         ("City", city), ("Group size", group_size), ("Goal", goal)):
        if value and value.strip():
            lines.append(f"{label}: {value.strip()}")
    message = "\n".join(lines)
    info = contact()
    subject = "AI training enquiry" + (f": {interest.strip()}" if interest.strip() else "")
    return {
        "message": message,
        "whatsapp_link": f"{info['whatsapp_link']}?text={quote(message)}" if info["whatsapp_link"] else None,
        "email_link": (f"mailto:{info['email']}?subject={quote(subject)}&body={quote(message)}"
                       if info["email"] else None),
    }


def search(query: str, limit: int = 8) -> list[dict]:
    terms = [t for t in re.findall(r"\w+", query.lower()) if len(t) > 1]
    if not terms:
        return []
    hits = []
    for page in discover_pages():
        title = page_title(page)
        for line in main_node(page).text().split("\n"):
            low = line.lower()
            score = sum(low.count(t) for t in terms)
            if score and len(line) > 3:
                matched = sum(1 for t in terms if t in low)
                hits.append((matched, score, page, title, line))
    hits.sort(key=lambda h: (-h[0], -h[1]))
    out, seen = [], set()
    for _, _, page, title, line in hits:
        key = (page.slug, line)
        if key in seen:
            continue
        seen.add(key)
        out.append({"page": page.slug, "title": title, "path": page.path, "url": page.url,
                    "snippet": line if len(line) <= 400 else line[:397] + "..."})
        if len(out) >= limit:
            break
    return out
