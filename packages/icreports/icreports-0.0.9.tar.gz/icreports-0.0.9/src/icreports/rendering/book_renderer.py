import logging
import shutil
import os
from pathlib import Path
import typing

from icreports.document import Document, Book

from .build_context import BuildContext
from .document_renderer import DocumentRenderer


logger = logging.getLogger(__name__)


def copy_files_relative(paths: list[Path], src: Path, dst: Path):
    for path in paths:
        shutil.copy(src / path, dst / path)


class BookRenderer(DocumentRenderer):

    def copy_document_sources(self, doc: Document, build_ctx: BuildContext, tag: str):

        book = typing.cast(Book, doc)

        tag_dir = build_ctx.build_dir / tag
        doc.config.write(tag_dir / "_config.yml")

        working_toc = book.toc
        if tag != "default":
            working_toc = book.toc.get_tag_version(tag)
        working_toc.write(tag_dir / "_toc.yml")

        os.makedirs(tag_dir / "src", exist_ok=True)
        copy_files_relative(working_toc.get_file_paths(), build_ctx.source_dir, tag_dir)

        self.copy_media_files(tag_dir, doc, build_ctx)
