from pathlib import Path
import logging

from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
from mdformat.renderer import MDRenderer
from bs4 import BeautifulSoup
import yaml

from icreports.hyperlink import Hyperlink

logger = logging.getLogger(__name__)


def _md_it_wikify_link(self, tokens, idx, options, env):
    if "href" in tokens[idx].attrs:
        link = Hyperlink(tokens[idx].attrs["href"])
        tokens[idx].attrSet("href", link.wikify())
    return self.renderToken(tokens, idx, options, env)


class ContentFile:

    def __init__(self, path: Path):
        self.path: Path = path
        self.src: str = ""
        self.tags: list[str] = []
        self.meta_key: str = "icreports"
        self.links: list[Hyperlink] = []
        self.extension: str = ""

    def has_tag(self, tag: str):
        return tag in self.tags

    def load(self, content_root: Path):
        with open(
            content_root / f"{self.path}.{self.extension}", "r", encoding="utf-8"
        ) as f:
            self.src = f.read()


class MarkdownContentFile(ContentFile):

    def __init__(self, path: Path) -> None:
        super().__init__(path)

        self.extension: str = "md"
        self.parser = MarkdownIt().use(front_matter_plugin)
        self.html: str = ""
        self.soup = None

    def load(self, content_root: Path):
        super().load(content_root)

        for token in self.parser.parse(self.src):
            if token.type == "front_matter":
                self._parse_frontmatter(token)

    def _parse_frontmatter(self, token):
        if not token.content:
            return
        try:
            meta = yaml.safe_load(token.content)
        except Exception as e:
            logger.error("Failed to load frontmatter yaml in %s", self.path)
            raise e
        if self.meta_key in meta:
            if "tags" in meta[self.meta_key]:
                self.tags = meta[self.meta_key]["tags"]

    def _wikify_link(self, token):
        if token.type != "link_open":
            return
        if "href" in token.attrs:
            link = Hyperlink(token.attrs["href"])
            token.attrSet("href", link.wikify())

    def _visit_token(self, token, func):
        if token.children is not None:
            for child in token.children:
                self._visit_token(child, func)
        else:
            func(token)

    def wikify_links(self):
        tokens = self.parser.parse(self.src)

        # self.md.add_renderer_rule("link_open", _md_it_wikify_link)
        for token in tokens:
            self._visit_token(token, self._wikify_link)

        md_renderer = MDRenderer()
        options = {}
        env = {}
        self.src = md_renderer.render(tokens, options, env)

    def render_html(self):
        self.html = self.parser.render(self.src)

        self.soup = BeautifulSoup(self.html, features="html.parser")
        self.links = self.soup.find_all("a", href=True)
