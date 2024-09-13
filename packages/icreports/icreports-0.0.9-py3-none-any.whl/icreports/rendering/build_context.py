from pathlib import Path
from typing import NamedTuple


class BuildContext(NamedTuple):

    source_dir: Path
    build_dir: Path
    formats: list[str] = ["html", "pdf"]
    tags: list[str] = []
    rebuild: bool = True
