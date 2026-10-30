"""Small, inspectable retrieval workflow. All document content is untrusted."""
from dataclasses import dataclass, asdict
from typing import Callable
from .core import Store


@dataclass
class Step:
    name: str
    status: str
    detail: str = ""


def run_retrieval(question: str, top_k: int = 5, store: Store | None = None):
    """Validate input, retrieve evidence and return structured execution trace."""
    steps = [Step("validate", "completed")]
    if not question.strip():
        raise ValueError("question must not be empty")
    if not 1 <= top_k <= 20:
        raise ValueError("top_k must be in [1, 20]")
    results = (store or Store()).retrieve(question, top_k)
    steps.append(Step("retrieve", "completed", f"{len(results)} passages"))
    sources = [
        {"id": i, "source": p["source"], "text": p["text"], "score": p["score"]}
        for i, p in enumerate(results, 1)
    ]
    if sources:
        answer = "\n\n".join(f"[{p['id']}] {p['text']}" for p in sources)
        steps.append(Step("extract", "completed", "Evidence returned without a model"))
    else:
        answer = "No relevant passages found."
        steps.append(Step("extract", "skipped", "No evidence"))
    return {"question": question, "answer": answer, "sources": sources,
            "trace": [asdict(step) for step in steps]}


def source_context(sources: list[dict]) -> str:
    """Produce a numbered evidence block, not instructions."""
    return "\n\n".join(
        f"[{item['id']}] SOURCE: {item['source']}\n{item['text']}" for item in sources
    )
