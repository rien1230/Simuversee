# writes each tick message into a file like a diary.

from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional
import json

# Ensures the logs gets written ti the right place.
def _find_repo_root(start_file: Path) -> Path:
# Looks for folder name
    for parent in start_file.resolve().parents:
        if parent.name == "backend":
            return parent.parent
    # Fallback: assume 3 levels up from /backend/app/services/
    return start_file.resolve().parents[3]


# Auto-generates __init__ and __repr__
@dataclass
class EventLogger:
    # Writes replay logs in JSONL format:
    # - one JSON object per line
    # - stored at: data/replays/<run_id>.jsonl

    run_id: str
    base_dir: Optional[Path] = None

    def __post_init__(self) -> None:
        repo_root = _find_repo_root(Path(__file__))
        replays_dir = self.base_dir or (repo_root / "data" / "replays")
        replays_dir.mkdir(parents=True, exist_ok=True)

        self.path: Path = replays_dir / f"{self.run_id}.jsonl"

    def log(self, diff: Dict[str, Any]) -> None:

        # Append a single diff as one JSON line.
        line = json.dumps(diff, ensure_ascii=False, separators=(",", ":"))
        with self.path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
