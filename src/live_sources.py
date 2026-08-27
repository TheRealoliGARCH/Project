"""Controlled live acquisition boundary for official source artifacts.

Network retrieval is injected for testability. Acquisition preserves raw artifacts
before parsing and deliberately leaves document-specific row extraction explicit.
"""
from pathlib import Path
from urllib.request import urlopen

from .acquisition import capture_text


def fetch_official_text(url: str, timeout: float = 30.0) -> str:
    """Retrieve a UTF-8 official text artifact without parsing it."""
    with urlopen(url, timeout=timeout) as response:
        return response.read().decode("utf-8")


def acquire_official_text(source_name: str, source_url: str, destination: str,
                          fetcher=fetch_official_text) -> dict:
    """Fetch once, persist verbatim, and return checksum-backed provenance."""
    text = fetcher(source_url)
    if not isinstance(text, str) or not text.strip():
        raise ValueError("official source returned no usable text")
    return capture_text(source_name, source_url, text, destination)


def extract_pipe_row(text: str, row_prefix: str) -> list[str]:
    """Extract exactly one pipe-delimited row selected by a documented prefix.

    This deliberately performs no date inference, maturity interpolation, or
    missing-value repair. Ambiguous or absent matches are rejected.
    """
    matches = [line.strip() for line in text.splitlines()
               if line.strip().startswith(row_prefix)]
    if len(matches) != 1:
        raise ValueError("source must contain exactly one matching documented row")
    cells = [cell.strip() for cell in matches[0].split("|")]
    if len(cells) < 2:
        raise ValueError("matching source row is malformed")
    return cells
