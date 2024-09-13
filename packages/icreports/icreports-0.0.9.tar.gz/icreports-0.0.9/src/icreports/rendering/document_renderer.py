import logging
import os
import shutil
from pathlib import Path

from icreports.document import Document

from .build_context import BuildContext
from .media_converter import MediaConverter

logger = logging.getLogger(__name__)


def copy_files(src: Path, dst: Path):
    for direntry in src.iterdir():
        if direntry.is_file():
            shutil.copy(direntry, dst)


def copy_files_relative(paths: list[Path], src: Path, dst: Path):
    for path in paths:
        shutil.copy(src / path, dst / path)


def clear_dir(src: Path):
    logger.info("Clearing directory %s", src)
    if src.exists():
        shutil.rmtree(src)
    os.makedirs(src)


class DocumentRenderer:

    def __init__(self):
        self.media_converter = MediaConverter()

    def validate(self, document: Document):
        # self.link_validator.validate_links(self.pages)
        pass

    def build_html(self, document_name: str, build_ctx: BuildContext):
        pass

    def build_pdf(self, document_name: str, build_ctx: BuildContext):
        pass

    def copy_media_files(self, tag_dir: Path, doc: Document, build_ctx: BuildContext):
        tag_media_dir = tag_dir / doc.config.media_dir
        os.makedirs(tag_media_dir)

        tag_build_media_dir = tag_dir / "_build/media"
        os.makedirs(tag_build_media_dir)

        copy_files(build_ctx.source_dir / doc.config.media_dir, tag_media_dir)
        copy_files(build_ctx.build_dir / "media", tag_build_media_dir)

    def copy_document_sources(self, doc: Document, build_ctx: BuildContext, tag: str):
        pass

    def build_tag(self, doc: Document, build_ctx: BuildContext, tag: str):

        tag_dir = build_ctx.build_dir / tag
        clear_dir(tag_dir)

        self.copy_document_sources(doc, build_ctx, tag)

        tag_build_ctx = BuildContext(
            tag_dir,
            tag_dir / "_build",
            build_ctx.formats,
            build_ctx.tags,
            build_ctx.rebuild,
        )
        logger.info("Building tag with %s", tag_build_ctx)

        self.build_formats(doc, tag_build_ctx)

        archive_path = build_ctx.build_dir / f"{doc.config.project_name}_{tag}"
        shutil.make_archive(str(archive_path), "zip", str(tag_dir))

    def build_formats(self, doc: Document, build_ctx: BuildContext):
        if "html" in build_ctx.formats:
            logger.info("Building html format")
            self.build_html(doc.config.project_name, build_ctx)

        if "pdf" in build_ctx.formats:
            logger.info("Building pdf format")
            self.build_pdf(doc.config.project_name, build_ctx)

    def render(self, doc: Document, build_ctx: BuildContext):

        logging.info("Building document with: %s", build_ctx)

        logger.info("Starting document checks")
        self.validate(doc)
        logger.info("Finished document checks")

        media_dir = build_ctx.source_dir / doc.config.media_dir
        os.makedirs(build_ctx.build_dir / "conversion", exist_ok=True)
        self.media_converter.run(
            media_dir, build_ctx.build_dir / "media", build_ctx.build_dir / "conversion"
        )

        logger.info("Has build tags: %s", build_ctx.tags)

        if not build_ctx.tags or "default" in build_ctx.tags:
            logger.info("Start building tag - default")
            self.build_tag(doc, build_ctx, "default")
            logger.info("Finished building tag - default")

        for tag in doc.config.tags:
            if not build_ctx.tags or tag in build_ctx.tags:
                logger.info("Start building tag - %s", tag)
                self.build_tag(doc, build_ctx, tag)
                logger.info("Finished building tag - %s", tag)
