"""In-process MCP tests: exercise the real MCPServer object end to end.

Uses the mcp SDK's in-process API (list_tools / call_tool / read_resource) —
no subprocess, no network. The true stdio transport is additionally covered by
the demo client run (``python -m askhabib.demo_client``) in CI.
"""

import asyncio
import json

from askhabib import core
from askhabib.server import mcp as server


def run(coro):
    return asyncio.run(coro)


EXPECTED_TOOLS = {
    "list_publications",
    "get_publication",
    "search_publications",
    "get_profile",
    "get_links",
}


def test_server_lists_all_tools():
    tools = run(server.list_tools())
    assert {t.name for t in tools} == EXPECTED_TOOLS
    for t in tools:
        assert t.description, f"tool {t.name} has no description"


def _call_json(name, arguments):
    result = run(server.call_tool(name, arguments))
    assert not result.is_error, f"{name} unexpectedly errored: {result.content}"
    assert result.content, f"{name} returned no content"
    return json.loads(result.content[0].text)


def test_tool_list_publications():
    rows = _call_json("list_publications", {})
    assert len(rows) == 5
    assert rows[0] == {
        "id": "p1",
        "title": core.get_publication("p1")["title"],
        "venue": "Computational Biology and Chemistry",
        "year": 2025,
    }


def test_tool_get_publication_round_trip():
    paper = _call_json("get_publication", {"publication_id": "p2"})
    assert paper["venue"] == "The Journal of Supercomputing"
    assert paper["status"] == "accepted"
    assert paper["draft"] is True


def test_tool_get_publication_unknown_id_is_clean_error():
    result = run(server.call_tool("get_publication", {"publication_id": "p99"}))
    assert result.is_error
    text = result.content[0].text
    assert "p99" in text and "p1" in text


def test_tool_search_publications_deepfake():
    hits = _call_json("search_publications", {"query": "deepfake"})
    assert [h["id"] for h in hits] == ["p3"]


def test_tool_search_publications_federated():
    hits = _call_json("search_publications", {"query": "federated"})
    assert [h["id"] for h in hits] == ["p4"]


def test_tool_search_publications_empty_query_is_clean_error():
    result = run(server.call_tool("search_publications", {"query": "  "}))
    assert result.is_error
    assert "non-empty" in result.content[0].text


def test_tool_get_profile():
    profile = _call_json("get_profile", {})
    assert profile["name"] == "Habib Ur Rehman"
    assert "SANWA SYSTEM SERVICE CO. LTD" in profile["current_role"]


def test_tool_get_links():
    links = _call_json("get_links", {})
    assert links["github"] == "https://github.com/Habib-Rehmn"
    assert links["email"] == "habib.gcuf.edu@gmail.com"


def _resource_texts(contents):
    texts = []
    for c in contents:
        payload = getattr(c, "content", None)
        if isinstance(payload, str):
            texts.append(payload)
        elif payload is not None and hasattr(payload, "text"):
            texts.append(payload.text)
        elif hasattr(c, "text"):
            texts.append(c.text)
    return texts


def test_resource_cv_is_markdown_with_his_name():
    contents = run(server.read_resource(core.CV_RESOURCE_URI))
    texts = _resource_texts(contents)
    assert texts, "resource returned no text content"
    md = texts[0]
    assert md.startswith("# Habib Ur Rehman")
    assert "Multimodal-FNet" in md


def test_resource_uri_registered():
    resources = run(server.list_resources())
    uris = [str(r.uri) for r in resources]
    assert core.CV_RESOURCE_URI in uris
