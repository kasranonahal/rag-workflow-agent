from app.core import Store
from app.workflow import run_retrieval, source_context


def test_workflow_evidence(tmp_path):
    store = Store(str(tmp_path / "documents.sqlite3"))
    store.ingest("research.md", "A retrieval workflow finds relevant passages.")
    response = run_retrieval("retrieval", store=store)
    assert response["sources"][0]["source"] == "research.md"
    assert response["sources"][0]["id"] == 1
    assert response["trace"][-1]["status"] == "completed"
    assert "[1] SOURCE: research.md" in source_context(response["sources"])


def test_workflow_empty_database(tmp_path):
    response = run_retrieval("something", store=Store(str(tmp_path / "empty.db")))
    assert response["sources"] == []
    assert response["trace"][-1]["status"] == "skipped"
