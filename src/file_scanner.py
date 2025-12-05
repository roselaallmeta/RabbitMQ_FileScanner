"""
File scanner module for recursively scanning directories and collecting file information.
"""
import os
from pathlib import Path
from typing import Dict, Any, Iterator



class FileScanner:
    """Recursively scans directories and collects file information."""
    
    def __init__(self, root_directory: str, follow_symlinks: bool = False):
        """Initialize file scanner."""
        self.root_directory = Path(root_directory).resolve()
        self.follow_symlinks = follow_symlinks
    
    def get_file_info(self, file_path: Path) -> Dict[str, Any]:
        """Get information about a file."""
        try:
            stat_info = file_path.stat()
            return {
                'filename': file_path.name,
                'path': str(file_path),
                'relative_path': str(file_path.relative_to(self.root_directory)),
                'size': stat_info.st_size
                
            }
        except Exception:
            return None
    
    def scan(self) -> Iterator[Dict[str, Any]]:
        """Recursively scan directory and yield file information."""
        if not self.root_directory.exists() or not self.root_directory.is_dir():
            return
        
        for root, dirs, files in os.walk(self.root_directory, followlinks=self.follow_symlinks):
            for filename in files:
                file_path = Path(root) / filename
                file_info = self.get_file_info(file_path)
                if file_info:
                    yield file_info
    
    @staticmethod
    def format_size(size_bytes: int) -> str:
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
