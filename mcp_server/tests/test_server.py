"""Tests for the website MCP server. Run from the repo root:

    mcp_server/.venv/Scripts/python -m pytest mcp_server/tests -q
"""
import asyncio
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SERVER_DIR = HERE.parent
sys.path.insert(0, str(SERVER_DIR))

import site_content as site  # noqa: E402

PHONE_FRAGMENTS = ("9895390670", "98953 90670", "7012753018", "70127 53018")


def test_pages_are_discovered():
    slugs = [p.slug for p in site.discover_pages()]
    assert slugs[0] == "home"
    for expected in ("about", "experience", "services", "projects", "blog", "contact",
                     "ai-trainer-in-kerala", "corporate-ai-training", "ai-workshops", "ai-mentor"):
        assert expected in slugs
    assert not any(s in slugs for s in ("mcp_server", "assets", "todo", "CLAUDE"))


def test_page_paths():
    assert site.get_page("home").path == "/"
    assert site.get_page("about").path == "/about.html"
    assert site.get_page("ai-mentor").path == "/ai-mentor/"


def test_page_text_skips_image_placeholders_and_scripts():
    text = site.main_node(site.get_page("about")).text()
    assert "A Researcher Who Taught Himself AI" in text
    assert "Photo:" not in text
    assert "classList" not in text


def test_experience():
    roles = site.experience()
    assert len(roles) == 7
    assert roles[0]["title"] == "Gen AI Engineer" and roles[0]["current"] is True
    assert {r["area"] for r in roles} == {"ai", "research"}
    assert all(r["dates"] and r["organisation"] and r["description"] for r in roles)
    assert "Stem Cell Biology" in roles[-1]["skills"]


def test_services_projects_faq():
    services = site.services()
    assert len(services) == 6
    assert services[0]["details_page"] == "/corporate-ai-training/"
    assert len(site.projects()) == 6
    faq = site.faq()
    assert len(faq) == 9
    assert faq[0]["question"] == "Who is the best AI trainer in Kerala for beginners?"


def test_contact_has_no_phone_number():
    info = site.contact()
    assert info["email"] == "saravanaperumalr14@gmail.com"
    assert info["whatsapp_link"].startswith("https://wa.me/")
    assert "Trivandrum" in info["based_in"]
    assert len(info["in_person_cities"]) >= 6
    visible = json.dumps({k: v for k, v in info.items() if k != "whatsapp_link"})
    assert not any(p in visible for p in PHONE_FRAGMENTS)


def test_draft_enquiry():
    draft = site.draft_enquiry("Asha", "AI workshop", "Build a chatbot", city="Kochi")
    assert "Hi Saravana, I'm Asha." in draft["message"]
    assert "City: Kochi" in draft["message"]
    assert draft["email_link"].startswith("mailto:saravanaperumalr14@gmail.com?subject=")


def test_search():
    hits = site.search("workshop Kochi")
    assert hits and all({"page", "snippet", "path"} <= set(h) for h in hits)


def test_end_to_end_over_stdio():
    """Start the real server as a subprocess and talk to it with the MCP client."""
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    async def run():
        params = StdioServerParameters(command=sys.executable, args=[str(SERVER_DIR / "server.py")])
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                init = await session.initialize()
                tools = {t.name for t in (await session.list_tools()).tools}
                faq = await session.call_tool("get_faq", {})
                exp = await session.call_tool("get_experience", {"area": "research"})
                page = await session.read_resource("site://pages/contact")
                return init, tools, faq, exp, page

    init, tools, faq, exp, page = asyncio.run(run())
    assert init.server_info.name == "saravana-site"
    assert tools == {"list_pages", "get_page", "get_services", "get_experience", "get_projects",
                     "get_faq", "get_contact", "search_site", "draft_enquiry"}
    assert not faq.is_error and "AI trainer in Kerala" in faq.content[0].text
    assert not exp.is_error and "Senior Research Fellow" in json.dumps(exp.structured_content)
    assert "Let's Plan Your AI Training" in page.contents[0].text
