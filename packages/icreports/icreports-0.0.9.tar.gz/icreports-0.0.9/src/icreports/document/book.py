"""
This module represents a text document
"""

import logging

from .document import Document
from .config import DocumentConfig
from .table_of_contents import TableOfContents

logger = logging.getLogger(__name__)


class Book(Document):
    """
    This class represents a book
    """

    def __init__(self, config: DocumentConfig, toc: TableOfContents) -> None:
        super().__init__(config)

        self.toc = toc
