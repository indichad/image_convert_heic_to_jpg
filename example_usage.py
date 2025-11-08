#!/usr/bin/env python3
"""
Example usage of the HEIC to JPG converter.
This file demonstrates how to use the HEICToJPGConverter class programmatically.
"""

from main import HEICToJPGConverter
from pathlib import Path


def example_batch_conversion():
    """Example of batch converting HEIC files from a folder."""
    
    # Initialize the converter with custom settings
    converter = HEICToJPGConverter(
        quality=90,  # JPG quality (1-100)
        verbose=True  # Enable detailed logging
    )
    
    # Example 1: Convert all HEIC files in a folder to the same folder
    input_folder = r"C:\Users\YourUsername\Pictures\HEIC_Photos"
    
    try:
        stats = converter.convert_folder(input_folder)
        print(f"Conversion completed! Converted {stats['converted']} out of {stats['total']} files.")
    except Exception as e:
        print(f"Error during conversion: {e}")
    
    # Example 2: Convert to a different output folder
    output_folder = r"C:\Users\YourUsername\Pictures\Converted_JPG"
    
    try:
        stats = converter.convert_folder(input_folder, output_folder)
        print(f"Files saved to: {output_folder}")
    except Exception as e:
        print(f"Error during conversion: {e}")


def example_single_file_conversion():
    """Example of converting a single HEIC file."""
    
    converter = HEICToJPGConverter(quality=95, verbose=True)
    
    # Convert a single file
    heic_file = Path(r"C:\Users\YourUsername\Pictures\photo.heic")
    output_folder = Path(r"C:\Users\YourUsername\Pictures\JPG")
    
    if heic_file.exists():
        success = converter.convert_single_file(heic_file, output_folder)
        if success:
            print(f"Successfully converted {heic_file.name}")
        else:
            print(f"Failed to convert {heic_file.name}")
    else:
        print(f"File not found: {heic_file}")


if __name__ == "__main__":
    print("HEIC to JPG Converter - Example Usage")
    print("=" * 40)
    
    # Uncomment the example you want to run:
    
    # Example 1: Batch conversion
    # example_batch_conversion()
    
    # Example 2: Single file conversion
    # example_single_file_conversion()
    
    print("\nTo use this converter:")
    print("1. Update the file paths in the examples above")
    print("2. Uncomment the example you want to run")
    print("3. Run this script")
    print("\nOr use the command line interface:")
    print("python main.py 'C:\\path\\to\\heic\\folder' -o 'C:\\path\\to\\output\\folder'")