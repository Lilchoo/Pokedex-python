from enum import Enum


class FileExtensions(Enum):
    """File Extension class"""
    TXT = ".txt"


class InvalidFileTypeError(Exception):
    """InvalidFileTypeError class"""

    def __init__(self, message):
        super().__init__(message)
