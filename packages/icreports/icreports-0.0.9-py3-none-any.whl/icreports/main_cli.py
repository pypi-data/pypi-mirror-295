import os
import logging
import argparse
from pathlib import Path

from icreports.document import Book, DocumentConfig, TableOfContents
from icreports.rendering import BuildContext
from icreports.rendering.jupyter_book import JupyterBookRenderer

logger = logging.getLogger(__name__)


def publish_book(cli_args):

    source_dir = cli_args.source_dir.resolve()

    config_path = cli_args.config.resolve()
    if not config_path.exists():
        config_path = source_dir / "_config.yml"

    logger.info("Loading config from %s", config_path)
    config = DocumentConfig()
    config.read(config_path)
    if cli_args.version:
        config.version = cli_args.version

    toc_path = source_dir / "_toc.yml"
    logger.info("Loading toc from %s", toc_path)
    toc = TableOfContents()
    toc.read(source_dir / "_toc.yml")
    toc.load_content(source_dir)

    book = Book(config, toc)

    formats = list(filter(None, cli_args.formats.split(",")))
    if not formats:
        formats = ["pdf", "html"]
    tags = list(filter(None, cli_args.tags.split(",")))
    build_ctx = BuildContext(
        source_dir, cli_args.build_dir.resolve(), formats, tags, cli_args.rebuild
    )

    renderer = JupyterBookRenderer()
    renderer.render(book, build_ctx)

def main_cli():
    
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True)

    book_parser = subparsers.add_parser("book")
    book_parser.add_argument(
        "--source_dir",
        type=Path,
        default=Path(os.getcwd()),
        help="Path to the document sources",
    )
    book_parser.add_argument(
        "--config",
        type=Path,
        default=Path(os.getcwd()) / "_config.yml",
        help="Path to document config",
    )
    book_parser.add_argument(
        "--build_dir",
        type=Path,
        default=Path(os.getcwd()) / "_build",
        help="Path for build output",
    )
    book_parser.add_argument(
        "--version", type=str, default="", help="Override the project version"
    )
    book_parser.add_argument(
        "--tags", type=str, default="", help="Comma separated list of tags to build"
    )
    book_parser.add_argument(
        "--rebuild",
        type=bool,
        default=True,
        help="If true do a clean rebuild of the book",
    )
    book_parser.add_argument(
        "--formats",
        type=str,
        default="",
        help="Comma separated list of output formats. Supports 'pdf', 'html'",
    )

    book_parser.set_defaults(func=publish_book)
    args = parser.parse_args()

    logging.basicConfig(encoding="utf-8", level=logging.INFO)

    args.func(args)
    
if __name__ == "__main__":

    main_cli()

