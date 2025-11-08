#!/usr/bin/env python3
"""
Test script to verify HEIC to JPG converter functionality.
This script tests the converter without requiring actual HEIC files.
"""

import tempfile
import os
from pathlib import Path
from main import HEICToJPGConverter


def test_converter_initialization():
    """Test that the converter initializes correctly."""
    print("Testing converter initialization...")
    
    # Test default initialization
    converter = HEICToJPGConverter()
    assert converter.quality == 95
    assert converter.verbose is False
    
    # Test custom initialization
    converter = HEICToJPGConverter(quality=85, verbose=True)
    assert converter.quality == 85
    assert converter.verbose is True
    
    print("✓ Converter initialization test passed")


def test_find_heic_files():
    """Test the HEIC file discovery functionality."""
    print("Testing HEIC file discovery...")
    
    converter = HEICToJPGConverter()
    
    # Create a temporary directory structure
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create test files
        (temp_path / "test1.heic").touch()
        (temp_path / "test2.HEIC").touch()
        (temp_path / "test3.heif").touch()
        (temp_path / "test4.HEIF").touch()
        (temp_path / "not_heic.jpg").touch()
        
        # Create subdirectory with HEIC files
        sub_dir = temp_path / "subfolder"
        sub_dir.mkdir()
        (sub_dir / "test5.heic").touch()
        
        # Test file discovery
        heic_files = converter.find_heic_files(temp_path)
        
        # Should find 5 HEIC files (4 in root, 1 in subfolder)
        assert len(heic_files) == 5
        
        # Check that all found files have correct extensions
        extensions = {f.suffix.lower() for f in heic_files}
        assert extensions == {'.heic', '.heif'}
    
    print("✓ HEIC file discovery test passed")


def test_invalid_folder():
    """Test behavior with invalid folder paths."""
    print("Testing invalid folder handling...")
    
    converter = HEICToJPGConverter()
    
    # Test non-existent folder
    try:
        converter.convert_folder("/non/existent/path")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "does not exist" in str(e)
    
    # Test file instead of folder
    with tempfile.NamedTemporaryFile() as temp_file:
        try:
            converter.convert_folder(temp_file.name)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "not a directory" in str(e)
    
    print("✓ Invalid folder handling test passed")


def test_empty_folder():
    """Test behavior with folder containing no HEIC files."""
    print("Testing empty folder handling...")
    
    converter = HEICToJPGConverter()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create some non-HEIC files
        temp_path = Path(temp_dir)
        (temp_path / "test.jpg").touch()
        (temp_path / "test.png").touch()
        
        stats = converter.convert_folder(temp_dir)
        
        assert stats['total'] == 0
        assert stats['converted'] == 0
        assert stats['failed'] == 0
    
    print("✓ Empty folder handling test passed")


def test_imports():
    """Test that all required modules can be imported."""
    print("Testing module imports...")
    
    try:
        import pillow_heif
        print("✓ pillow-heif imported successfully")
    except ImportError:
        print("✗ Failed to import pillow-heif")
        return False
    
    try:
        from PIL import Image, ExifTags
        print("✓ PIL imported successfully")
    except ImportError:
        print("✗ Failed to import PIL")
        return False
    
    try:
        import piexif
        print("✓ piexif imported successfully")
    except ImportError:
        print("✗ Failed to import piexif")
        return False
    
    print("✓ All module imports test passed")
    return True


def main():
    """Run all tests."""
    print("HEIC to JPG Converter - Test Suite")
    print("=" * 40)
    
    try:
        test_imports()
        test_converter_initialization()
        test_find_heic_files()
        test_invalid_folder()
        test_empty_folder()
        
        print("\n" + "=" * 40)
        print("✓ All tests passed!")
        print("\nThe converter is ready to use.")
        print("To convert HEIC files, run:")
        print("python main.py 'path/to/heic/folder'")
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)