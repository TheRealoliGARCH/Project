"""Reproducible acquisition primitives for official sovereign yield sources."""
from dataclasses import asdict
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json


def sha256_text(text: str) -> str:
    return sha256(text.encode("utf-8")).hexdigest()


def capture_text(source_name: str, source_url: str, text: str, destination: str) -> dict:
    """Persist a raw text artifact and a provenance sidecar without parsing it."""
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    metadata = {
        "source_name": source_name,
        "source_url": source_url,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "sha256": sha256_text(text),
        "artifact": str(path),
    }
    sidecar = path.with_suffix(path.suffix + ".metadata.json")
    sidecar.write_text(json.dumps(metadata, indent=2, sort_keys=True), encoding="utf-8")
    return metadata


def load_captured_text(destination: str) -> tuple[str, dict]:
    path = Path(destination)
    text = path.read_text(encoding="utf-8")
    sidecar = path.with_suffix(path.suffix + ".metadata.json")
    metadata = json.loads(sidecar.read_text(encoding="utf-8"))
    if metadata.get("sha256") != sha256_text(text):
        raise ValueError("captured artifact checksum mismatch")
    return text, metadata
