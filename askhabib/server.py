"""MCP server exposing Habib Ur Rehman's professional profile.

Transport: stdio (JSON-RPC 2.0 over stdin/stdout), the standard transport for
Claude Desktop and other local MCP clients.

Tools:
    list_publications   id/title/venue/year for all 5 publications
    get_publication     full record for one publication id (p1..p5)
    search_publications keyword search over titles + summaries + venues
    get_profile         CV summary (bio, role, education, skills, interests)
    get_links           contact links (GitHub, LinkedIn, website, email)

Resources:
    profile://habib/cv  the profile rendered as Markdown

Run with:  python -m askhabib.server   (or the ``ask-habib-server`` console script)
"""

import asyncio
import json

import mcp.types as types
from mcp.server.mcpserver import MCPServer

from . import core

SERVER_NAME = "ask-habib"

mcp = MCPServer(
    SERVER_NAME,
    instructions=(
        "Answer questions about Habib Ur Rehman — ML/AI Engineer and "
        "healthcare-AI researcher — using only the tools and the profile "
        "resource. Paper summaries are drafts pending his verification: "
        "say so when you quote one."
    ),
)


@mcp.tool()
def list_publications() -> str:
    """List all publications as id/title/venue/year records (JSON)."""
    return json.dumps(core.list_publications(), indent=2)


@mcp.tool()
def get_publication(publication_id: str) -> str:
    """Return the full record (title, venue, year, summary) for one
    publication id such as 'p3' (JSON)."""
    try:
        return json.dumps(core.get_publication(publication_id), indent=2)
    except core.PublicationNotFoundError as exc:
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=str(exc))],
            isError=True,
        )


@mcp.tool()
def search_publications(query: str) -> str:
    """Keyword-search publications over titles, summaries and venues (JSON).
    Example queries: 'deepfake', 'federated', 'vision transformer'."""
    try:
        return json.dumps(core.search_publications(query), indent=2)
    except ValueError as exc:
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=str(exc))],
            isError=True,
        )


@mcp.tool()
def get_profile() -> str:
    """Return Habib Ur Rehman's CV summary: bio, current role, education,
    skills, research interests, and contact links (JSON)."""
    return json.dumps(core.get_profile(), indent=2)


@mcp.tool()
def get_links() -> str:
    """Return contact links: GitHub, LinkedIn, website, email (JSON)."""
    return json.dumps(core.get_links(), indent=2)


@mcp.resource(core.CV_RESOURCE_URI, mime_type="text/markdown")
def habib_cv() -> str:
    """Habib Ur Rehman's profile as a Markdown CV."""
    return core.cv_markdown()


def main() -> None:
    """Entry point: serve over stdio."""
    asyncio.run(mcp.run_stdio_async())


if __name__ == "__main__":
    main()
