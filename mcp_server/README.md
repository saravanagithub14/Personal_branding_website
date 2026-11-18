# Website MCP server

An [MCP](https://modelcontextprotocol.io) server that gives AI assistants (Claude Desktop, Claude Code, or any MCP client) read-only access to this website's content.

It reads the HTML pages each time it's asked, so its answers always match the live site. It only reads the public pages. It never exposes `CLAUDE.md`, `todo.md` or anything outside the site, and it publishes no phone number.

## Tools

| Tool | What it returns |
| --- | --- |
| `list_pages` | Every page: slug, title, description, path |
| `get_page(slug)` | The visible text of one page |
| `get_services` | The six training and mentoring services, with links to detail pages |
| `get_experience(area)` | Roles with dates, organisation, description and skills (`all`, `ai` or `research`) |
| `get_projects` | AI project areas and the tools used |
| `get_faq` | The FAQ from the AI trainer in Kerala page |
| `get_contact` | Email, WhatsApp link, profiles, base city, cities covered, booking and fees policy |
| `search_site(query)` | Keyword search across all pages |
| `draft_enquiry(...)` | A ready-to-send enquiry with WhatsApp and email links. It never sends anything. |

Resources: `site://pages` (all pages as JSON) and `site://pages/{slug}` (one page as text).

## Setup

From the repo root:

```bash
python -m venv mcp_server/.venv
mcp_server/.venv/Scripts/python -m pip install -r mcp_server/requirements.txt   # Windows
# macOS/Linux: mcp_server/.venv/bin/python -m pip install -r mcp_server/requirements.txt
```

### Claude Code

The repo's `.mcp.json` registers the server for this project. Claude Code asks you to approve it the first time. On macOS or Linux, change `command` to `mcp_server/.venv/bin/python`.

### Claude Desktop

Add this to `claude_desktop_config.json` (on Windows: `%APPDATA%\Claude\claude_desktop_config.json`), using absolute paths:

```json
{
  "mcpServers": {
    "saravana-site": {
      "command": "D:\\Repositories\\personal_branding_website\\Personal_branding_website\\mcp_server\\.venv\\Scripts\\python.exe",
      "args": ["D:\\Repositories\\personal_branding_website\\Personal_branding_website\\mcp_server\\server.py"]
    }
  }
}
```

Restart Claude Desktop after saving.

## Settings (environment variables)

| Variable | Default | Use |
| --- | --- | --- |
| `SITE_BASE_URL` | unset | The live domain, e.g. `https://example.com`. Once set, results include full URLs. |
| `SITE_ROOT` | the repo root | Where the HTML pages live |

## Tests

```bash
mcp_server/.venv/Scripts/python -m pip install pytest
mcp_server/.venv/Scripts/python -m pytest mcp_server/tests -q
```

The tests check the parsed content (7 roles, 6 services, 6 projects, 9 FAQs, no phone numbers, no image placeholder text). They also run a full round trip: a real MCP client starts the server, lists its tools, calls them and reads a page.

## How it reads the site

The server relies on the page markup, so keep these class names if you restyle the pages:

| Content | Page | Markup |
| --- | --- | --- |
| Experience | `experience.html` | `.timeline-group`, `.timeline-when`, `.timeline-org`, `.timeline-desc`, `.tags` |
| Services and projects | `services.html`, `projects.html` | `li.service` cards |
| FAQ | `ai-trainer-in-kerala/index.html` | `[data-faq-item]` |
| Contact | `contact.html` | `mailto:` link, `wa.me` link, `.cities` list |

If any of these change, the tests will fail and show what broke.
