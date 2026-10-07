"""Demo: spin up the ask-habib MCP server over stdio and run example calls.

Shows a realistic MCP client session: initialize, discover tools, then three
example tool calls. The transcript this prints is the example session used in
the README (captured from a real run).

Run:  python -m askhabib.demo_client
"""

import asyncio
import json
import sys

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


def _short(text: str, limit: int = 900) -> str:
    return text if len(text) <= limit else text[:limit] + "\n... [truncated]"


async def run_demo() -> str:
    """Run the demo session; return the full transcript as a string."""
    lines = []
    log = lines.append

    server_params = StdioServerParameters(
        command=sys.executable, args=["-m", "askhabib.server"]
    )
    log(">>> client: starting ask-habib MCP server over stdio")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            init = await session.initialize()
            log(
                f"<<< server: hello — {init.server_info.name} "
                f"(protocol {init.protocol_version})"
            )

            tools = await session.list_tools()
            names = [t.name for t in tools.tools]
            log(f"<<< server: tools available: {', '.join(names)}")

            # --- Call 1: keyword search -----------------------------------
            log('>>> client: search_publications(query="deepfake")')
            res = await session.call_tool(
                "search_publications", {"query": "deepfake"}
            )
            payload = json.loads(res.content[0].text)
            titles = [p["title"] for p in payload]
            log(f"<<< server: {len(payload)} match(es):")
            for t in titles:
                log(f"    - {t}")
            if payload:
                log(
                    "    (summaries are drafts pending his verification)"
                )

            # --- Call 2: full publication record --------------------------
            log('>>> client: get_publication(publication_id="p1")')
            res = await session.call_tool(
                "get_publication", {"publication_id": "p1"}
            )
            paper = json.loads(res.content[0].text)
            log(
                f"<<< server: {paper['title']}\n"
                f"    {paper['venue']}, {paper['year']} "
                f"({paper['status']})"
            )
            log(f"    summary: {_short(paper['summary'], 260)}")

            # --- Call 3: CV summary ---------------------------------------
            log(">>> client: get_profile()")
            res = await session.call_tool("get_profile", {})
            profile = json.loads(res.content[0].text)
            log(
                f"<<< server: {profile['name']} — {profile['title']}\n"
                f"    {profile['current_role']}\n"
                f"    {profile['education'][0]['degree']}, "
                f"{profile['education'][0]['institution']} "
                f"({profile['education'][0]['years']})\n"
                f"    skills: {', '.join(profile['skills'][:5])}, ..."
            )

            # Bonus: read the Markdown CV resource (not counted as a tool call)
            log(">>> client: read_resource('profile://habib/cv')")
            result = await session.read_resource("profile://habib/cv")
            md = result.contents[0].text
            first = md.splitlines()[0]
            log(
                f"<<< server: Markdown CV ({len(md)} chars), "
                f"opens with: {first!r}"
            )

    log(">>> client: session closed")
    return "\n".join(lines)


def main() -> None:
    print(asyncio.run(run_demo()))


if __name__ == "__main__":
    main()
