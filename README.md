# ask-habib-mcp

[![CI](https://github.com/habib-analyst/ask-habib-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/habib-analyst/ask-habib-mcp/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)

An [MCP (Model Context Protocol)](https://spec.modelcontextprotocol.io/) server
that exposes **Habib Ur Rehman**'s professional profile — five 2025 publications
and a CV summary — as tools and a resource that any MCP client (Claude Desktop,
a website chat-widget backend, an agent) can query.

## The problem

Recruiters and collaborators ask chatbots about Habib and get hallucinations:
invented papers, wrong venues, phantom affiliations. This server is a small,
grounded, citable source of truth. A chatbot with `ask-habib-mcp` connected
answers "what did Habib publish on deepfakes?" from the actual corpus instead
of making something up.

## Architecture

```
MCP client (Claude Desktop / chat-widget backend / agent)
        │   JSON-RPC 2.0
        ▼
   stdio transport
        │
        ▼
  askhabib.server  (MCPServer, package: askhabib)
   ├─ tools: list_publications, get_publication,
   │         search_publications, get_profile, get_links
   └─ resources: profile://habib/cv   (Markdown CV)
        │
        ▼
  askhabib.data   (ground-truth corpus — titles, venues, years;
                   summaries flagged draft: True)
        │
   no network calls, ever
```

The corpus lives in-process (`askhabib/data.py`); every tool call is a local
function call wrapped as an MCP tool. Nothing leaves the machine.

## Quickstart (< 5 minutes)

```bash
git clone https://github.com/habib-analyst/ask-habib-mcp
cd ask-habib-mcp
pip install -r requirements.txt
pip install .

# sanity check — runs a real stdio MCP session against the server
python -m askhabib.demo_client
```

### Claude Desktop

Add to your Claude Desktop config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "ask-habib": {
      "command": "ask-habib-server",
      "args": []
    }
  }
}
```

If you installed without the console script, use the fallback instead:

```json
{
  "mcpServers": {
    "ask-habib": {
      "command": "python",
      "args": ["-m", "askhabib.server"]
    }
  }
}
```

Restart Claude Desktop, then ask: *"What has Habib Ur Rehman published on
federated learning?"*

## Example session

Real transcript, captured from `python -m askhabib.demo_client` against the
stdio server:

```
>>> client: starting ask-habib MCP server over stdio
<<< server: hello — ask-habib (protocol 2025-11-25)
<<< server: tools available: list_publications, get_publication, search_publications, get_profile, get_links
>>> client: search_publications(query="deepfake")
<<< server: 1 match(es):
    - Multimodal-FNet: Unparametrized Token Mixing for Multimodal Deepfake Detection
    (summaries are drafts pending his verification)
>>> client: get_publication(publication_id="p1")
<<< server: Revolutionizing medical imaging: A cutting-edge AI framework with vision transformers and perceiver IO for multi-disease diagnosis
    Computational Biology and Chemistry, 2025 (published)
    summary: Hybrid framework combining Vision Transformers with Perceiver IO for multi-disease diagnosis across imaging domains including MRI, CT/X-ray, and dermoscopic images. Evaluated on Stroke, Alzheimer's, Tinea, Melanoma, Pneumonia, and Lung Cancer cases. Ships with
... [truncated]
>>> client: get_profile()
<<< server: Habib Ur Rehman — ML/AI Engineer
    ML/AI Engineer at SANWA SYSTEM SERVICE CO. LTD
    BS Data Analytics, Government College University Faisalabad (2021-2025)
    skills: Python, PyTorch, TensorFlow, Hugging Face, LangChain/LangGraph, ...
>>> client: read_resource('profile://habib/cv')
<<< server: Markdown CV (3890 chars), opens with: '# Habib Ur Rehman'
>>> client: session closed
```

## Honest note: draft summaries

Titles, venues, and years in this corpus are exact. The 2–3 sentence summary on
each paper is a **draft written from the title and venue description, pending
verification by Habib himself** — every record carries `"draft": true`, every
full-record response includes a `summary_note`, and the server instructs
connected clients to say so when quoting a summary. Treat summaries as a
starting point, not as his words.

## Tools & resources

| Name | Type | What it returns |
|---|---|---|
| `list_publications` | tool | id / title / venue / year for all 5 papers (JSON) |
| `get_publication` | tool | full record for one id (`p1`…`p5`); clean error for unknown ids (JSON) |
| `search_publications` | tool | keyword search over titles + summaries + venues (JSON) |
| `get_profile` | tool | CV summary: bio, role, education, skills, interests, contact (JSON) |
| `get_links` | tool | GitHub, LinkedIn, website, email (JSON) |
| `profile://habib/cv` | resource | the profile rendered as Markdown |

## Roadmap

- Replace draft summaries with Habib-verified text (`draft: false`)
- Add arXiv/DOI/publisher links per paper
- Wire into the [habib.top](https://habib.top) "Chat with Habib" widget backend
- Optional: publication/talk resources beyond the static corpus

## Spec

Built against the [Model Context Protocol specification](https://spec.modelcontextprotocol.io/)
using the official `mcp` Python SDK (stdio transport).

## License

MIT — see [LICENSE](LICENSE). © 2026 Habib Ur Rehman.
