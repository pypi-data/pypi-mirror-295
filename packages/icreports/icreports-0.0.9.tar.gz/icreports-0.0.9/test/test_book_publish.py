import shutil
from pathlib import Path
import os

from icreports.document import Book, DocumentConfig, TableOfContents
from icreports.rendering import BuildContext
from icreports.rendering.jupyter_book import JupyterBookRenderer


def get_test_data_dir():
    return Path(__file__).parent / "data"

def test_book_publish():
    content_root = get_test_data_dir() / "mock_document"

    config = DocumentConfig()
    config.read(content_root / "_config.yml")

    toc = TableOfContents()
    toc.read(content_root / "_toc.yml")
    toc.load_content(content_root)
    
    book = Book(config, toc)

    build_dir = Path(os.getcwd()) / "test_book_publish"
    build_ctx = BuildContext(content_root, build_dir)

    renderer = JupyterBookRenderer()
    renderer.render(book, build_ctx)

    shutil.rmtree(build_dir)
