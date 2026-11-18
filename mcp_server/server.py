"""MCP server for Saravana Perumal R's website.

Gives AI assistants (Claude Desktop, Claude Code, any MCP client) read-only access to
the site's content: pages, services, experience, projects, FAQ and contact options.
Everything is read from the HTML pages at request time, so answers match the live site.

Run (stdio):  python mcp_server/server.py
"""
from __future__ import annotations

import json
from typing import Literal

from mcp.server.mcpserver import MCPServer
from mcp.types import ToolAnnotations

import site_content as site

INSTRUCTIONS = """\
This server answers questions about Saravana Perumal R, an AI trainer and mentor based in
Trivandrum (Thiruvananthapuram), Kerala, India, and a Gen AI Engineer at Blackbox Learning.
All content comes from his website, so prefer these tools over guessing.

- Services, experience, projects and FAQ have their own tools; use search_site for anything else.
- Never quote prices. Fees depend on the audience, group size, days and format; people should ask for a quote.
- Do not share or invent phone numbers. Point people to WhatsApp (whatsapp_link), email or LinkedIn.
- To help someone get in touch, use draft_enquiry; it only prepares a message, it never sends one.
"""

mcp = MCPServer(
    name="saravana-site",
    title="Saravana Perumal R, AI trainer",
    description="Read-only access to the content of Saravana Perumal R's website.",
    instructions=INSTRUCTIONS,
    website_url=site.SITE_BASE_URL or None,
    version="1.0.0",
)

READ_ONLY = ToolAnnotations(read_only_hint=True, destructive_hint=False,
                            idempotent_hint=True, open_world_hint=False)


# --------------------------------------------------------------------------- tools

@mcp.tool(title="List website pages", annotations=READ_ONLY)
def list_pages() -> list[dict]:
    """List every page on the website with its slug, title, description and path.
    Use a slug with get_page to read that page."""
    return [
        {"slug": p.slug, "title": site.page_title(p), "description": site.page_description(p),
         "path": p.path, "url": p.url}
        for p in site.discover_pages()
    ]


@mcp.tool(title="Read a page", annotations=READ_ONLY)
def get_page(slug: str) -> dict:
    """Read the visible text of one page. `slug` comes from list_pages, for example
    "home", "about", "experience", "services", "projects", "blog", "contact",
    "ai-trainer-in-kerala", "corporate-ai-training", "ai-workshops" or "ai-mentor"."""
    page = site.get_page(slug)
    return {"slug": page.slug, "title": site.page_title(page), "path": page.path,
            "url": page.url, "text": site.main_node(page).text()}


@mcp.tool(title="Training services", annotations=READ_ONLY)
def get_services() -> list[dict]:
    """The six ways to work with Saravana: corporate AI training, AI workshops, generative AI
    training, agentic AI training, one-on-one AI mentoring and freelance training. Each has a
    description and, where one exists, the path of its detailed page."""
    return site.services()


@mcp.tool(title="Work experience", annotations=READ_ONLY)
def get_experience(area: Literal["all", "ai", "research"] = "all") -> list[dict]:
    """Saravana's roles with dates, organisation, description and skills, newest first.
    area="ai" returns AI and data science roles, area="research" returns life sciences
    research roles, area="all" returns both."""
    roles = site.experience()
    return roles if area == "all" else [r for r in roles if r["area"] == area]


@mcp.tool(title="Education and qualifications", annotations=READ_ONLY)
def get_education() -> dict:
    """Saravana's degrees (BSc, MSc, Diploma in Data Science) with dates, institution and
    details, plus qualifications: UGC-NET, publications and languages."""
    return site.education()


@mcp.tool(title="Skills and technologies", annotations=READ_ONLY)
def get_skills(group: str = "") -> dict:
    """Saravana's skills: four focus areas, then six groups of tools and methods (LLMs and
    agentic AI, data science and ML, deep learning, AI deployment, life sciences research,
    teaching and mentoring), each skill with a short note such as "Primary language".
    Pass `group` (e.g. "deep learning") to return only matching groups."""
    data = site.skills()
    if group.strip():
        needle = group.strip().lower()
        data["groups"] = [g for g in data["groups"]
                          if needle in g["group"].lower() or needle in (g["id"] or "")]
    return data


@mcp.tool(title="Publications", annotations=READ_ONLY)
def get_publications() -> dict:
    """Saravana's publication counts and the publications listed on the site (type, year,
    title, venue, summary, topics). Only publications with full details on the site are
    listed; the counts cover all of them."""
    return site.publications()


@mcp.tool(title="AI projects", annotations=READ_ONLY)
def get_projects() -> list[dict]:
    """The AI project areas Saravana has built and teaches from (RAG chatbots, agents,
    text to SQL, fine-tuning, AWS apps, computer vision), with the tools used."""
    return site.projects()


@mcp.tool(title="Frequently asked questions", annotations=READ_ONLY)
def get_faq() -> list[dict]:
    """The website's FAQ about AI training with Saravana: who it suits, coding background,
    corporate training, workshops, mentoring, booking and fees."""
    return site.faq()


@mcp.tool(title="Contact options", annotations=READ_ONLY)
def get_contact() -> dict:
    """How to reach Saravana: email, WhatsApp link, profiles, where he is based, the cities he
    covers in person, how booking works and how fees are set. No phone number is published."""
    return site.contact()


@mcp.tool(title="Search the website", annotations=READ_ONLY)
def search_site(query: str, limit: int = 8) -> list[dict]:
    """Keyword search across all pages. Returns matching lines with the page they come from.
    Use it for questions the other tools don't cover."""
    return site.search(query, max(1, min(limit, 25)))


@mcp.tool(title="Draft an enquiry", annotations=READ_ONLY)
def draft_enquiry(name: str, interest: str, goal: str, organisation: str = "",
                  city: str = "", group_size: str = "") -> dict:
    """Prepare an enquiry for Saravana, the same message the website's contact form builds.
    Returns the message text plus a WhatsApp link and an email link that open it ready to
    send. Nothing is sent: the person sends it themselves.
    interest: e.g. "Corporate AI training", "AI workshop", "One-on-one AI mentoring".
    goal: what they want their group (or themselves) to be able to do."""
    return site.draft_enquiry(name, interest, goal, organisation, city, group_size)


# --------------------------------------------------------------------------- resources

@mcp.resource("site://pages", name="pages", title="Website pages",
              description="Every page on the website, as JSON.", mime_type="application/json")
def pages_resource() -> str:
    return json.dumps(list_pages(), indent=2)


@mcp.resource("site://pages/{slug}", name="page", title="Website page",
              description="The visible text of one page, by slug.", mime_type="text/plain")
def page_resource(slug: str) -> str:
    page = site.get_page(slug)
    return f"# {site.page_title(page)}\n\n{site.main_node(page).text()}"


if __name__ == "__main__":
    mcp.run()
