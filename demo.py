#!/usr/bin/env python3
"""
Utility script with common HEIC to JPG conversion scenarios.
Run this script to see practical examples of using the converter.
"""

import os
from pathlib import Path
from main import HEICToJPGConverter


def print_separator(title):
    """Print a formatted separator with title."""
    print("\n" + "=" * 50)
    print(f" {title}")
    print("=" * 50)


def demo_basic_usage():
    """Demonstrate basic converter usage."""
    print_separator("BASIC USAGE DEMO")
    
    print("Creating a converter with default settings:")
    converter = HEICToJPGConverter()
    print(f"✓ Default quality: {converter.quality}")
    print(f"✓ Verbose logging: {converter.verbose}")
    
    print("\nCreating a converter with custom settings:")
    converter = HEICToJPGConverter(quality=85, verbose=True)
    print(f"✓ Custom quality: {converter.quality}")
    print(f"✓ Verbose logging: {converter.verbose}")


def demo_folder_scenarios():
    """Demonstrate different folder scenarios."""
    print_separator("FOLDER SCENARIOS")
    
    # Example folder paths (adjust these for your system)
    example_paths = [
        r"C:\Users\%USERNAME%\Pictures\iPhone",
        r"C:\Users\%USERNAME%\Pictures\HEIC_Photos",
        r"D:\Photos\Camera_Roll",
        r"C:\Photos\HEIC"
    ]
    
    print("Common folder locations where you might find HEIC files:")
    for i, path in enumerate(example_paths, 1):
        print(f"{i}. {path}")
    
    print("\nTo use the converter with these folders:")
    print('python main.py "C:\\Users\\YourUsername\\Pictures\\iPhone"')
    print('python main.py "C:\\Users\\YourUsername\\Pictures\\HEIC_Photos" -o "C:\\Users\\YourUsername\\Pictures\\JPG_Photos"')


def demo_command_examples():
    """Show practical command line examples."""
    print_separator("COMMAND LINE EXAMPLES")
    
    examples = [
        {
            "description": "Convert all HEIC files in a folder (saves JPG in same location)",
            "command": 'python main.py "C:\\Photos\\HEIC"'
        },
        {
            "description": "Convert with custom output folder",
            "command": 'python main.py "C:\\Photos\\HEIC" -o "C:\\Photos\\JPG"'
        },
        {
            "description": "Convert with lower quality for smaller files",
            "command": 'python main.py "C:\\Photos\\HEIC" -q 75'
        },
        {
            "description": "Convert with verbose output to see progress",
            "command": 'python main.py "C:\\Photos\\HEIC" -v'
        },
        {
            "description": "Full example with all options",
            "command": 'python main.py "C:\\Photos\\HEIC" -o "C:\\Photos\\JPG" -q 90 -v'
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['description']}:")
        print(f"   {example['command']}")


def demo_programmatic_usage():
    """Show programmatic usage examples."""
    print_separator("PROGRAMMATIC USAGE EXAMPLES")
    
    code_examples = [
        {
            "title": "Simple batch conversion",
            "code": '''from main import HEICToJPGConverter

converter = HEICToJPGConverter()
stats = converter.convert_folder("C:\\\\Photos\\\\HEIC")
print(f"Converted {stats['converted']} files")'''
        },
        {
            "title": "Conversion with custom settings",
            "code": '''from main import HEICToJPGConverter

converter = HEICToJPGConverter(quality=80, verbose=True)
stats = converter.convert_folder(
    input_folder="C:\\\\Photos\\\\HEIC",
    output_folder="C:\\\\Photos\\\\JPG"
)'''
        },
        {
            "title": "Single file conversion",
            "code": '''from main import HEICToJPGConverter
from pathlib import Path

converter = HEICToJPGConverter()
success = converter.convert_single_file(
    source_path=Path("photo.heic"),
    output_folder=Path("converted")
)'''
        }
    ]
    
    for example in code_examples:
        print(f"\n{example['title']}:")
        print("-" * 30)
        print(example['code'])


def demo_tips_and_tricks():
    """Show tips and best practices."""
    print_separator("TIPS AND BEST PRACTICES")
    
    tips = [
        "💡 Quality 95 is the default - good balance of quality and file size",
        "💡 Quality 85-90 is good for web use or when you need smaller files",
        "💡 Quality 100 gives best quality but largest file sizes",
        "💡 Use -v (verbose) flag to see detailed progress and any errors",
        "💡 The converter preserves folder structure when using output folder",
        "💡 Already converted files are automatically skipped",
        "💡 EXIF data (camera settings, GPS, dates) is preserved",
        "💡 Run from command line for batch operations",
        "💡 Use programmatic interface for integration with other scripts"
    ]
    
    for tip in tips:
        print(tip)


def check_for_heic_files():
    """Check common locations for HEIC files."""
    print_separator("CHECKING FOR HEIC FILES")
    
    # Common locations where HEIC files might be found
    common_locations = [
        Path.home() / "Pictures",
        Path.home() / "Pictures" / "iPhone",
        Path.home() / "Desktop",
        Path.home() / "Downloads"
    ]
    
    print("Checking common locations for HEIC files...")
    found_any = False
    
    for location in common_locations:
        if location.exists() and location.is_dir():
            try:
                heic_files = list(location.rglob("*.heic")) + list(location.rglob("*.HEIC"))
                if heic_files:
                    print(f"✓ Found {len(heic_files)} HEIC files in: {location}")
                    found_any = True
                    # Show first few files as examples
                    for file in heic_files[:3]:
                        print(f"  - {file.name}")
                    if len(heic_files) > 3:
                        print(f"  ... and {len(heic_files) - 3} more")
            except PermissionError:
                print(f"✗ No access to: {location}")
    
    if not found_any:
        print("No HEIC files found in common locations.")
        print("You can still use the converter by specifying the correct folder path.")


def main():
    """Run all demonstrations."""
    print("HEIC to JPG Converter - Usage Guide")
    print("This guide shows you how to use the converter effectively")
    
    demo_basic_usage()
    demo_folder_scenarios()
    demo_command_examples()
    demo_programmatic_usage()
    demo_tips_and_tricks()
    check_for_heic_files()
    
    print_separator("READY TO CONVERT")
    print("The converter is ready to use!")
    print("\nQuick start:")
    print("1. Find a folder containing HEIC files")
    print("2. Run: python main.py 'path/to/heic/folder'")
    print("3. Check the output folder for your JPG files")
    print("\nFor help: python main.py --help")


if __name__ == "__main__":
    main()