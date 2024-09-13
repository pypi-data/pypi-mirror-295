from pathlib import Path
import logging

from icreports.content_file import ContentFile, MarkdownContentFile


logger = logging.getLogger(__name__)


class Section:

    def __init__(self, path: Path) -> None:
        self.content: ContentFile = MarkdownContentFile(path)

    def load(self, root: Path):
        self.content.load(root)

    def has_tag(self, tag: str):
        return self.content.has_tag(tag)

    def get_path(self):
        return self.content.path

    def get_path_with_extension(self):
        return Path(f"{self.content.path}.{self.content.extension}")


class Chapter:

    def __init__(self) -> None:
        self.base_section: Section | None = None
        self.sections: list[Section] = []

    def has_tag_sections(self, tag: str) -> bool:
        if self.base_section and self.base_section.has_tag(tag):
            return True

        for section in self.sections:
            if section.has_tag(tag):
                return True
        return False

    def get_tag_version(self, tag: str):
        tag_chapter = Chapter()
        if self.base_section and self.base_section.has_tag(tag):
            tag_chapter.base_section = self.base_section

        for section in self.sections:
            if section.has_tag(tag):
                tag_chapter.sections.append(section)
        return tag_chapter

    def load(self, root: Path):
        if self.base_section:
            self.base_section.load(root)

        for section in self.sections:
            section.load(root)

    def get_file_paths(self) -> list[Path]:
        paths = []
        if self.base_section:
            paths.append(self.base_section.get_path_with_extension())
        paths.extend([s.get_path_with_extension() for s in self.sections])
        return paths

    def deserialize(self, data: dict):
        if "file" in data:
            self.base_section = Section(Path(data["file"]))
        if "sections" in data:
            for entry in data["sections"]:
                if "file" in entry:
                    self.sections.append(Section(Path(entry["file"])))

    def serialize(self):
        ret = {}
        if self.base_section:
            ret["file"] = str(self.base_section.get_path())
        if self.sections:
            ret["sections"] = []
            for section in self.sections:
                ret["sections"].append({"file": str(section.get_path())})
        return ret
