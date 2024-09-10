import pytest
from autor.file_parser import FileParser
import os
import tempfile

def test_file_parser():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a temporary file
        with open(os.path.join(tmpdir, 'test.py'), 'w') as f:
            f.write("print('Hello, World!')")
        
        # Initialize FileParser with the temporary directory
        parser = FileParser(tmpdir)
        
        # Parse the files
        files = parser.parse()
        
        # Check if the file was parsed correctly
        assert 'test.py' in [os.path.basename(f) for f in files.keys()]
        assert "print('Hello, World!')" in files.values()

def test_file_parser_empty_directory():
    with tempfile.TemporaryDirectory() as tmpdir:
        parser = FileParser(tmpdir)
        files = parser.parse()
        assert len(files) == 0