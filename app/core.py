import os
import re
import sqlite3


def chunks(text: str, size: int = 900, overlap: int = 120):
    if not (0 <= overlap < size):
        raise ValueError("overlap must be smaller than size")
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    result = []
    step = size - overlap
    for start in range(0, len(text), step):
        result.append(text[start:start + size])
        if start + size >= len(text):
            break
    return result


class Store:
    def __init__(self, path=None):
        self.path = path or os.environ.get("RAG_DB", "rag.sqlite3")
        self.initialize()

    def connect(self):
        return sqlite3.connect(self.path)

    def initialize(self):
        with self.connect() as con:
            con.execute("CREATE VIRTUAL TABLE IF NOT EXISTS passages USING fts5(source UNINDEXED, body)")

    def ingest(self, source, text):
        if not source.strip():
            raise ValueError("source is required")
        pieces = chunks(text)
        with self.connect() as con:
            con.execute("DELETE FROM passages WHERE source = ?", (source,))
            con.executemany("INSERT INTO passages(source, body) VALUES(?, ?)", [(source, p) for p in pieces])
        return len(pieces)

    def retrieve(self, question, limit=5):
        terms = re.findall(r"[a-zA-Z0-9_]+", question)
        if not terms:
            return []
        expression = " OR ".join('"' + t + '"' for t in terms[:12])
        with self.connect() as con:
            rows = con.execute(
                "SELECT source, body, bm25(passages) AS rank FROM passages WHERE passages MATCH ? ORDER BY rank LIMIT ?",
                (expression, limit),
            ).fetchall()
        return [{"source": source, "text": body, "score": rank} for source, body, rank in rows]
