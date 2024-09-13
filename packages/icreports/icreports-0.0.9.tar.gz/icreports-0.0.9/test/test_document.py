from pathlib import Path
from icreports.document import Book, DocumentConfig, TableOfContents


def get_test_data_dir():
    return Path(__file__).parent / "data"

def test_document():
    content_root = get_test_data_dir() / "mock_document"

    config = DocumentConfig()
    config.read(content_root / "_config.yml")

    toc = TableOfContents()
    toc.read(content_root / "_toc.yml")
    
    _ = Book(config, toc)
