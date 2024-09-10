"""
This module defines the ZettelFileParser class and associated helper functions for parsing zettel files.
It includes functionality to extract metadata from filenames and file content using specific patterns and external utilities.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from doogat.core.domain.value_objects.zettel_data import ZettelData
from buvis.pybase.filesystem import FileMetadataReader

from doogat.core.infrastructure.persistence.file_parsers.parsers.markdown.markdown import (
    MarkdownZettelFileParser,
)

DATETIME_PATTERN = re.compile(r"^\d{8}\d{6}")


class ZettelFileParser:
    """
    A parser for zettel files that extracts raw data and metadata from the file content and filename.

    This parser uses the ZettelParserMarkdown for parsing the content of the file and enriches the parsed data
    with additional metadata extracted from the file path and system metadata.
    """

    @staticmethod
    def from_file(file_path: Path) -> ZettelData:
        """
        Parses a zettel file from a given path and returns the raw data with enriched metadata.

        Args:
            file_path (Path): The path to the zettel file to be parsed.

        Returns:
            ZettelData: An object containing the parsed content and metadata of the zettel.
        """
        with Path(file_path).open("r", encoding="utf-8") as file:
            content = file.read()

        zettel_raw_data = MarkdownZettelFileParser.parse(content)

        if zettel_raw_data.metadata.get("date", None) is None:
            zettel_raw_data.metadata["date"] = _get_date_from_file(file_path)

        if zettel_raw_data.metadata.get("title", None) is None:
            zettel_raw_data.metadata["title"] = _get_title_from_filename(file_path.stem)

        return zettel_raw_data


def _get_date_from_file(file_path: Path) -> datetime | None:
    """
    Attempts to extract a datetime object from the file name based on predefined patterns.
    If no valid date is found in the filename, it falls back to file system creation date or git first commit date.

    Args:
        file_path (Path): The path to the file from which to extract the date.

    Returns:
        datetime | None: The extracted datetime object, if any, otherwise None.
    """
    if DATETIME_PATTERN.match(file_path.stem):
        try:
            return datetime.strptime(file_path.stem[:14], "%Y%m%d%H%M%S").replace(
                tzinfo=timezone.utc,
            )
        except ValueError:
            try:
                return datetime.strptime(file_path.stem[:12], "%Y%m%d%H%M").replace(
                    tzinfo=timezone.utc,
                )
            except ValueError:
                pass

    fs_creation_date = FileMetadataReader.get_creation_datetime(file_path)
    git_first_commit_date = FileMetadataReader.get_first_commit_datetime(file_path)

    if fs_creation_date is not None and git_first_commit_date is not None:
        return min(fs_creation_date, git_first_commit_date)
    if fs_creation_date is not None:
        return fs_creation_date
    if git_first_commit_date is not None:
        return git_first_commit_date

    return None


def _get_title_from_filename(filename: str) -> str | None:
    """
    Extracts a human-readable title from a filename by stripping away predefined patterns and formatting.

    Args:
        filename (str): The filename from which to extract the title.

    Returns:
        str | None: The extracted title, if any, otherwise None.
    """
    if DATETIME_PATTERN.match(filename):
        title_from_filename = filename[15:]
    else:
        title_from_filename = filename

    if len(title_from_filename) > 0:
        title_from_filename = title_from_filename.replace("-", " ")
        return title_from_filename[0].upper() + title_from_filename[1:]

    return None
