"""Direct tests of the pure query logic in askhabib.core (no MCP, no network)."""

import pytest

from askhabib import core
from askhabib.data import LINKS, PROFILE, PUBLICATIONS


def test_publication_ids_are_p1_through_p5():
    ids = [p["id"] for p in PUBLICATIONS]
    assert ids == ["p1", "p2", "p3", "p4", "p5"]


def test_all_summaries_flagged_draft():
    for paper in PUBLICATIONS:
        assert paper["draft"] is True, f"{paper['id']} missing draft flag"


def test_list_publications_schema():
    rows = core.list_publications()
    assert len(rows) == 5
    for row in rows:
        assert set(row.keys()) == {"id", "title", "venue", "year"}
    assert rows[0]["id"] == "p1"
    assert rows[2]["title"].startswith("Multimodal-FNet")


def test_get_publication_full_record():
    paper = core.get_publication("p3")
    assert paper["id"] == "p3"
    assert paper["title"] == (
        "Multimodal-FNet: Unparametrized Token Mixing for Multimodal "
        "Deepfake Detection"
    )
    assert paper["venue"] == "IEEE TPAMI"
    assert paper["year"] == 2025
    assert paper["status"] == "submitted"
    assert paper["draft"] is True
    assert "draft" in paper["summary_note"].lower() or "DRAFT" in paper["summary_note"]


def test_get_publication_ground_truth_titles():
    expected = {
        "p1": "Revolutionizing medical imaging",
        "p2": "AI-Driven Multi-Disease Classification",
        "p4": "A Unified Framework for Enhancing Federated Learning Security",
        "p5": "AI-Driven Risk Assessment and Mitigation Strategies",
    }
    for pid, prefix in expected.items():
        assert core.get_publication(pid)["title"].startswith(prefix)


def test_get_publication_unknown_id_raises_clean_error():
    with pytest.raises(core.PublicationNotFoundError) as excinfo:
        core.get_publication("p99")
    message = str(excinfo.value)
    assert "p99" in message
    for known in ("p1", "p2", "p3", "p4", "p5"):
        assert known in message


def test_search_deepfake_finds_multimodal_fnet():
    hits = core.search_publications("deepfake")
    assert [h["id"] for h in hits] == ["p3"]


def test_search_federated_finds_fl_security_paper():
    hits = core.search_publications("federated")
    assert [h["id"] for h in hits] == ["p4"]


def test_search_vision_transformer_finds_medical_imaging_papers():
    hits = core.search_publications("vision transformer")
    assert sorted(h["id"] for h in hits) == ["p1", "p2"]


def test_search_is_case_insensitive():
    assert [h["id"] for h in core.search_publications("DeepFake")] == ["p3"]
    assert [h["id"] for h in core.search_publications("FEDERATED")] == ["p4"]


def test_search_no_match_returns_empty_list():
    assert core.search_publications("quantum cryptography") == []


def test_search_empty_query_raises():
    with pytest.raises(ValueError):
        core.search_publications("")
    with pytest.raises(ValueError):
        core.search_publications("   ")


def test_get_profile_contents():
    profile = core.get_profile()
    assert profile["name"] == "Habib Ur Rehman"
    assert profile["title"] == "ML/AI Engineer"
    assert "SANWA SYSTEM SERVICE CO. LTD" in profile["current_role"]
    assert profile["current_role_since"] == "2025-07"
    edu = profile["education"][0]
    assert edu["degree"] == "BS Data Analytics"
    assert edu["institution"] == "Government College University Faisalabad"
    assert "MCP (Model Context Protocol)" in profile["skills"]
    assert profile["contact"]["email"] == "habib.gcuf.edu@gmail.com"


def test_get_links_exact_urls():
    links = core.get_links()
    assert links == {
        "github": "https://github.com/Habib-Rehmn",
        "linkedin": "https://www.linkedin.com/in/hur-dev",
        "website": "https://habib.top",
        "email": "habib.gcuf.edu@gmail.com",
    }
    # Ground-truth check against the data module
    assert links == LINKS
    assert PROFILE["name"] == "Habib Ur Rehman"


def test_cv_markdown_contains_name_and_papers():
    md = core.cv_markdown()
    assert md.splitlines()[0] == "# Habib Ur Rehman"
    assert "SANWA SYSTEM SERVICE CO. LTD" in md
    for paper in PUBLICATIONS:
        assert paper["title"] in md
    assert "draft" in md.lower()
    assert "https://habib.top" in md
