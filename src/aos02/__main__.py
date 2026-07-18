"""Python module entrypoint for the AOS-02 command-line interface."""

from .loader import load_records
from .interfaces.cli import main

__all__ = ["load_records", "main"]


if __name__ == "__main__":
    raise SystemExit(main())
