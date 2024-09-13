import os
from pathlib import Path
from icreports.document.table_of_contents import TableOfContents

def get_test_data_dir():
    return Path(__file__).parent / "data"


def test_table_of_contents():
    toc_file = get_test_data_dir() / "mock_document/_toc.yml"

    toc = TableOfContents()
    toc.read(toc_file)

    toc_out = Path(os.getcwd()) / "_toc_test.yml"
    toc.write(toc_out)

    toc_1 = TableOfContents()
    toc_1.read(toc_out)

    toc_out.unlink()

    assert len(toc_1.parts[0].chapters[2].sections) == 2
    
