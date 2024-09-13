from pathlib import Path

import yaml

from iccore.serialization import read_yaml


class DocumentConfig:

    def __init__(self) -> None:
        self.data: dict = {}
        self.version: str = ""
        self.project_name: str = "document"
        self.tags: list[str] = []
        self.media_dir = Path("src/media")
        self.source_dir = Path("src")

        self._key: str = "icreports"

    def read(self, path: Path):
        self.deserialize(read_yaml(path))

    def deserialize(self, data: dict):
        self.data = data
        if self._key not in self.data:
            return

        config = self.data[self._key]

        if "project_name" in config:
            self.project_name = config["project_name"]

        if not self.version:
            if "version" in config:
                self.version = config["version"]
            else:
                self.version = "0.0.0"

        if "tags" in config:
            self.tags = config["tags"]

        if "media_dir" in config:
            self.media_dir = config["media_dir"]

    def serialize(self):
        ret = self.data
        ret["version"] = self.version
        ret["project_name"] = self.project_name
        ret["tag"] = self.tags
        ret["media_dir"] = str(self.media_dir)
        return ret

    def write(self, path: Path):
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(self.serialize(), f)
