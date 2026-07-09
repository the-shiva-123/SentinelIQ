from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from ingestion.service import IngestionService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Ingest documents into the processed store")
    parser.add_argument("paths", nargs="+", help="One or more files to ingest")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    service = IngestionService()
    documents = service.ingest_files([Path(path) for path in args.paths])
    print(f"Ingested {len(documents)} document(s)")
    return 0


if __name__ == "__main__":
    main()
