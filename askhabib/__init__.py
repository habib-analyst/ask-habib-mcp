"""ask-habib-mcp: an MCP server exposing Habib Ur Rehman's professional profile.

Gives MCP clients (Claude Desktop, chat-widget backends, agents) a grounded,
citable source for his publications and CV summary — no hallucinations.

Paper summaries below are DRAFTS pending his verification (each record carries
``draft: True``); titles, venues and years are ground truth.
"""

__version__ = "0.1.0"
__author__ = "Habib Ur Rehman"

from .core import (
    PublicationNotFoundError,
    cv_markdown,
    get_links,
    get_profile,
    get_publication,
    list_publications,
    search_publications,
)
from .data import LINKS, PROFILE, PUBLICATIONS

__all__ = [
    "__version__",
    "LINKS",
    "PROFILE",
    "PUBLICATIONS",
    "PublicationNotFoundError",
    "cv_markdown",
    "get_links",
    "get_profile",
    "get_publication",
    "list_publications",
    "search_publications",
]
