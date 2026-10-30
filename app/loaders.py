"""Local document extraction helpers. PDF support is optional."""
from pathlib import Path


SUPPORTED = {".txt", ".md", ".pdf"}


def load_document(path: str | Path) -> str:
    file = Path(path)
    if not file.is_file():
        raise FileNotFoundError(file)
    suffix = file.suffix.lower()
    if suffix in {".txt", ".md"}:
        return file.read_text(encoding="utf-8")
    if suffix == ".pdf":
        try:
            import fitz
        except ImportError as exc:
            raise RuntimeError("Install pymupdf to read PDFs") from exc
        with fitz.open(file) as document:
            return "\n".join(page.get_text(sort=True) for page in document)
    raise ValueError(f"Unsupported document type: {suffix}")
