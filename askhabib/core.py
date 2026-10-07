"""Pure query logic over the ask-habib corpus.

No MCP imports here — these functions are directly unit-testable and are
wrapped by :mod:`askhabib.server` as MCP tools.
"""

from copy import deepcopy
from typing import Any, Dict, List

from .data import LINKS, PROFILE, PUBLICATIONS

DRAFT_NOTE = (
    "Note: the paper summaries served here are DRAFTS written from titles and "
    "venue descriptions, pending verification by Habib Ur Rehman."
)

CV_RESOURCE_URI = "profile://habib/cv"


class PublicationNotFoundError(LookupError):
    """Raised when no publication matches a requested id."""


def _listing_record(paper: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": paper["id"],
        "title": paper["title"],
        "venue": paper["venue"],
        "year": paper["year"],
    }


def _full_record(paper: Dict[str, Any]) -> Dict[str, Any]:
    record = deepcopy(paper)
    record["summary_note"] = DRAFT_NOTE
    return record


def list_publications() -> List[Dict[str, Any]]:
    """Return id/title/venue/year for every publication."""
    return [_listing_record(p) for p in PUBLICATIONS]


def get_publication(publication_id: str) -> Dict[str, Any]:
    """Return the full record for one publication id (e.g. ``p3``).

    Raises:
        PublicationNotFoundError: if no publication has that id.
    """
    for paper in PUBLICATIONS:
        if paper["id"] == publication_id:
            return _full_record(paper)
    known = sorted(p["id"] for p in PUBLICATIONS)
    raise PublicationNotFoundError(
        f"Unknown publication id {publication_id!r}. Known ids: {', '.join(known)}."
    )


def search_publications(query: str) -> List[Dict[str, Any]]:
    """Keyword search over publication titles, summaries and venues.

    Case-insensitive substring match; every whitespace-separated token in the
    query must appear somewhere in the paper's searchable text (AND semantics).
    """
    if not query or not query.strip():
        raise ValueError("Search query must be a non-empty string.")
    tokens = query.lower().split()
    hits = []
    for paper in PUBLICATIONS:
        haystack = " ".join(
            [paper["title"], paper["summary"], paper["venue"]]
        ).lower()
        if all(tok in haystack for tok in tokens):
            hits.append(_full_record(paper))
    return hits


def get_profile() -> Dict[str, Any]:
    """Return the CV-summary profile dict."""
    profile = deepcopy(PROFILE)
    profile["contact"] = deepcopy(LINKS)
    return profile


def get_links() -> Dict[str, str]:
    """Return contact links (GitHub, LinkedIn, website, email)."""
    return deepcopy(LINKS)


def cv_markdown() -> str:
    """Render the profile as a Markdown CV document."""
    lines = [
        f"# {PROFILE['name']}",
        "",
        f"**{PROFILE['title']}** — {PROFILE['current_role']} ({PROFILE['current_role_since']})",
        "",
        PROFILE["bio"],
        "",
        "## Education",
        "",
    ]
    for edu in PROFILE["education"]:
        lines.append(
            f"- **{edu['degree']}**, {edu['institution']} ({edu['years']})"
        )
    lines += ["", "## Skills", ""]
    lines.append(", ".join(PROFILE["skills"]))
    lines += ["", "## Research Interests", ""]
    for interest in PROFILE["research_interests"]:
        lines.append(f"- {interest}")
    lines += ["", "## Contact", ""]
    for label, url in LINKS.items():
        lines.append(f"- {label.capitalize()}: {url}")
    lines += ["", "## Publications", ""]
    for paper in PUBLICATIONS:
        lines.append(
            f"### {paper['id']}: {paper['title']}"
        )
        lines.append(f"*{paper['venue']}, {paper['year']} ({paper['status']})*")
        lines.append("")
        lines.append(f"> {paper['summary']}")
        lines.append("")
        lines.append("_Summary is a draft pending his verification._")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
