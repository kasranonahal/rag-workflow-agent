from app.core import Store, chunks


def test_empty_chunks():
    assert chunks("  ") == []


def test_chunk_overlap():
    assert chunks("abcdefghij", 6, 2) == ["abcdef", "efghij"]


def test_ingest_and_retrieve(tmp_path):
    store = Store(str(tmp_path / "test.db"))
    assert store.ingest("guide.md", "retrieval augmented generation combines search and models") == 1
    assert store.retrieve("retrieval")[0]["source"] == "guide.md"
    store.ingest("guide.md", "replacement document")
    assert store.retrieve("retrieval") == []
