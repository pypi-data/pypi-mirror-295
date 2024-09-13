from pathlib import Path
import logging

from .chapter import Chapter

logger = logging.getLogger(__name__)


class Part:

    def __init__(self) -> None:
        self.caption: str = ""
        self.chapters: list[Chapter] = []

    def load(self, root: Path):
        for chapter in self.chapters:
            chapter.load(root)

    def get_file_paths(self) -> list[Path]:
        paths = []
        for chapter in self.chapters:
            paths.extend(chapter.get_file_paths())
        return paths

    def has_tag_chapters(self, tag: str):
        for chapter in self.chapters:
            if chapter.has_tag_sections(tag):
                return True
        return False

    def get_tag_version(self, tag: str):
        tag_part = Part()
        tag_part.caption = self.caption

        for chapter in self.chapters:
            if chapter.has_tag_sections(tag):
                tag_part.chapters.append(chapter.get_tag_version(tag))
        return tag_part

    def deserialize(self, data: dict):
        if "caption" in data:
            self.caption = data["caption"]

        if "chapters" in data:
            for entry in data["chapters"]:
                chapter = Chapter()
                chapter.deserialize(entry)
                self.chapters.append(chapter)

    def serialize(self):
        ret = {}
        if self.caption:
            ret["caption"] = self.caption

        if self.chapters:
            ret["chapters"] = []
            for chapter in self.chapters:
                ret["chapters"].append(chapter.serialize())
        return ret
