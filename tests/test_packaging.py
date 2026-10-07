"""Packaging tests: the project installs and exposes working entry points."""

from importlib import metadata


def test_distribution_installed_with_matching_version():
    import askhabib

    dist = metadata.distribution("askhabib")
    assert dist.version == askhabib.__version__


def test_runtime_dependency_is_mcp_only():
    dist = metadata.distribution("askhabib")
    requires = [r.split(";")[0].strip().lower() for r in dist.requires or []]
    assert requires == ["mcp"], f"unexpected runtime deps: {requires}"


def test_console_script_entry_points_load():
    eps = metadata.entry_points(group="console_scripts")
    by_name = {ep.name: ep for ep in eps}
    server_ep = by_name["ask-habib-server"]
    demo_ep = by_name["ask-habib-demo"]
    assert server_ep.value == "askhabib.server:main"
    assert demo_ep.value == "askhabib.demo_client:main"
    assert callable(server_ep.load())
    assert callable(demo_ep.load())


def test_python_requires_allows_310():
    dist = metadata.distribution("askhabib")
    assert "3.10" in str(dist.metadata["Requires-Python"])
