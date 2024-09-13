from pathlib import Path
import yaml
import logging

from iccore.serialization import read_yaml

from .part import Part
from .chapter import Section

logger = logging.getLogger(__name__)


class TableOfContents:

    def __init__(self) -> None:
        self.jb_format: str = "jb-book"
        self.root: Section | None = None
        self.parts: list[Part] = []

    def read(self, path: Path):
        self.deserialize(read_yaml(path))

    def load_content(self, root: Path):
        if self.root:
            self.root.load(root)

        for part in self.parts:
            part.load(root)

    def serialize(self):
        ret = {}
        ret["format"] = self.jb_format
        if self.root:
            ret["root"] = str(self.root.get_path())

        if self.parts:
            ret["parts"] = []
            for part in self.parts:
                ret["parts"].append(part.serialize())
        return ret

    def get_file_paths(self) -> list[Path]:
        paths = []
        if self.root:
            paths.append(self.root.get_path_with_extension())
        for part in self.parts:
            paths.extend(part.get_file_paths())
        return paths

    def get_tag_version(self, tag: str):
        tag_toc = TableOfContents()
        tag_toc.root = self.root
        tag_toc.jb_format = self.jb_format

        for part in self.parts:
            if part.has_tag_chapters(tag):
                tag_toc.parts.append(part.get_tag_version(tag))
        return tag_toc

    def deserialize(self, content: dict):

        if "format" in content:
            self.jb_format = content["format"]

        if "root" in content:
            self.root = Section(content["root"])

        if "parts" in content:
            for entry in content["parts"]:
                part = Part()
                part.deserialize(entry)
                self.parts.append(part)

    def write(self, path: Path):
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(self.serialize(), f)
