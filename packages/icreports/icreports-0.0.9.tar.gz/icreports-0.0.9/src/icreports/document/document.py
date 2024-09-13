"""
This module represents a text document
"""

from .config import DocumentConfig


class Document:
    """
    A text document, such as a report or book
    """

    def __init__(self, config: DocumentConfig):
        self.config = config
