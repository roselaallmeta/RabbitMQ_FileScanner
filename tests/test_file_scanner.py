"""
Tests for file_scanner module.
"""
import os
import tempfile
import pytest
from pathlib import Path

from src.file_scanner import FileScanner


@pytest.fixture
def temp_directory():
    """Create a temporary directory with test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = Path(tmpdir)
        (test_dir / "file1.txt").write_text("test content 1")
        (test_dir / "file2.py").write_text("print('hello')")
        (test_dir / "subdir").mkdir()
        (test_dir / "subdir" / "file3.json").write_text('{"key": "value"}')
        yield test_dir


def test_file_scanner_initialization():
    """Test FileScanner initialization."""
    scanner = FileScanner("/tmp")
    assert scanner.root_directory == Path("/tmp").resolve()
    assert scanner.follow_symlinks is False


def test_validate_directory_exists(temp_directory):
    """Test directory validation with existing directory."""
    scanner = FileScanner(str(temp_directory))
    files = list(scanner.scan())
    assert len(files) >= 3


def test_validate_directory_not_exists():
    """Test directory validation with non-existent directory."""
    scanner = FileScanner("/nonexistent/directory/12345")
    files = list(scanner.scan())
    assert len(files) == 0


def test_scan_files(temp_directory):
    """Test scanning files in directory."""
    scanner = FileScanner(str(temp_directory))
    files = list(scanner.scan())
    
    
    for file_info in files:
        assert 'filename' in file_info
        assert 'path' in file_info
        assert 'size' in file_info
        assert 'relative_path' in file_info


def test_get_file_info(temp_directory):
    """Test getting file information."""
    scanner = FileScanner(str(temp_directory))
    test_file = temp_directory / "file1.txt"
    file_info = scanner.get_file_info(test_file)
    
    assert file_info is not None
    assert file_info['filename'] == "file1.txt"
    assert file_info['size'] > 0
    # assert file_info['extension'] == ".txt"


def test_format_size():
    """Test size formatting."""
    assert FileScanner.format_size(0) == "0.00 B"
    assert FileScanner.format_size(1024) == "1.00 KB"
    assert FileScanner.format_size(1024 * 1024) == "1.00 MB"

