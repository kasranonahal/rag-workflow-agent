"""Ingest text, Markdown or PDF files from the command line."""
import argparse
from pathlib import Path
from app.core import Store
from app.loaders import load_document


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--db", default=None, help="SQLite database path")
    args = parser.parse_args()
    store = Store(args.db)
    for file in args.files:
        count = store.ingest(str(file), load_document(file))
        print(f"{file}: indexed {count} chunks")


if __name__ == "__main__":
    main()
