#!/usr/bin/env python3
"""
Shared utilities for 100 Greatest Series scripts.
Handles book root detection and config loading.
"""

import yaml
from pathlib import Path
from typing import Dict, Any


def find_book_root(start_path: Path = None) -> Path:
    """
    Find the book root directory by looking for config.yaml.

    Args:
        start_path: Starting path for search (default: current working directory)

    Returns:
        Path to book root directory

    Raises:
        FileNotFoundError: If config.yaml cannot be found
    """
    if start_path is None:
        start_path = Path.cwd()

    current = start_path.resolve()

    # Walk up directory tree looking for config.yaml
    for parent in [current] + list(current.parents):
        config_path = parent / 'config.yaml'
        if config_path.exists():
            return parent

    raise FileNotFoundError(
        f"Could not find config.yaml in {start_path} or any parent directory. "
        "Are you running from within a book directory?"
    )


def load_config(book_root: Path = None) -> Dict[str, Any]:
    """
    Load book configuration from config.yaml.

    Args:
        book_root: Path to book root (default: auto-detect)

    Returns:
        Dictionary containing book configuration
    """
    if book_root is None:
        book_root = find_book_root()

    config_path = book_root / 'config.yaml'

    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    return config


def get_book_path(book_root: Path, path_key: str) -> Path:
    """
    Get a configured path relative to book root.

    Args:
        book_root: Path to book root
        path_key: Key in config structure section (e.g., 'database_dir', 'writeups_dir')

    Returns:
        Absolute path to the configured directory
    """
    config = load_config(book_root)
    relative_path = config['structure'][path_key]
    return book_root / relative_path


def get_series_root(book_root: Path = None) -> Path:
    """
    Get the series root directory (parent of books/).

    Args:
        book_root: Path to book root (default: auto-detect)

    Returns:
        Path to series root directory
    """
    if book_root is None:
        book_root = find_book_root()

    # Book root should be in books/book-name/, so series root is 2 levels up
    return book_root.parent.parent


if __name__ == '__main__':
    # Test the utilities
    try:
        book_root = find_book_root()
        print(f"Book root: {book_root}")

        config = load_config(book_root)
        print(f"Book title: {config['book']['title']}")
        print(f"Short name: {config['book']['short_name']}")

        series_root = get_series_root(book_root)
        print(f"Series root: {series_root}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
