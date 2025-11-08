# HEIC to JPG Converter

A Python script to convert HEIC (High Efficiency Image Container) images to JPG format while preserving all metadata including EXIF data.

## Features

- **Batch conversion**: Convert all HEIC files in a folder and its subfolders
- **Metadata preservation**: Retains EXIF data and other image metadata
- **Flexible output**: Save to the same folder or specify a different output directory
- **Quality control**: Adjustable JPG quality settings (1-100)
- **Progress tracking**: Detailed logging and conversion statistics
- **Error handling**: Robust error handling with informative messages
- **Folder structure preservation**: Maintains subfolder structure when using output directory

## Requirements

- Python 3.12+
- pillow-heif
- pillow
- piexif

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install pillow-heif pillow piexif
   ```

## Usage

### Command Line Interface

#### Basic usage (convert in place):
```bash
python main.py "C:\path\to\heic\folder"
```

#### Convert to a different folder:
```bash
python main.py "C:\path\to\heic\folder" -o "C:\path\to\output\folder"
```

#### Adjust JPG quality:
```bash
python main.py "C:\path\to\heic\folder" -q 85
```

#### Enable verbose logging:
```bash
python main.py "C:\path\to\heic\folder" -v
```

#### Full example with all options:
```bash
python main.py "C:\Users\Username\Pictures\HEIC_Photos" -o "C:\Users\Username\Pictures\JPG_Photos" -q 90 -v
```

### Programmatic Usage

```python
from main import HEICToJPGConverter

# Create converter instance
converter = HEICToJPGConverter(quality=95, verbose=True)

# Convert all HEIC files in a folder
stats = converter.convert_folder(
    input_folder="C:\\path\\to\\heic\\folder",
    output_folder="C:\\path\\to\\output\\folder"  # Optional
)

print(f"Converted {stats['converted']} out of {stats['total']} files")
```

## Command Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `input_folder` | Path to folder containing HEIC images (required) | - |
| `-o, --output` | Output folder path (optional) | Same as input |
| `-q, --quality` | JPG quality (1-100) | 95 |
| `-v, --verbose` | Enable verbose logging | False |

## Features in Detail

### Metadata Preservation
The converter preserves:
- **EXIF data**: Camera settings, GPS coordinates, timestamps
- **Image info**: Color profiles, orientation data
- **Other metadata**: Any additional metadata stored in the image

### Folder Structure
When using an output folder, the converter maintains the original folder structure:
```
Input:
├── Photos/
│   ├── 2023/
│   │   └── vacation.heic
│   └── 2024/
│       └── birthday.heic

Output:
├── JPG_Photos/
│   ├── 2023/
│   │   └── vacation.jpg
│   └── 2024/
│       └── birthday.jpg
```

### Error Handling
- **File not found**: Clear error messages for missing files/folders
- **Permission errors**: Handles read/write permission issues
- **Corrupted files**: Skips corrupted images and continues processing
- **Metadata errors**: Continues conversion even if metadata extraction fails

### Performance
- **Memory efficient**: Processes images one at a time
- **Skip existing**: Automatically skips files that have already been converted
- **Progress reporting**: Shows conversion progress and statistics

## Example Output

```
2024-11-04 10:30:15 - INFO - Found 25 HEIC files to convert
2024-11-04 10:30:15 - INFO - Converting: IMG_001.heic -> IMG_001.jpg
2024-11-04 10:30:16 - INFO - Successfully converted: C:\Output\IMG_001.jpg
2024-11-04 10:30:16 - INFO - Converting: IMG_002.heic -> IMG_002.jpg
...

Conversion Summary:
  Total files: 25
  Converted: 24
  Failed: 1
  Success rate: 96.0%
```

## Troubleshooting

### Common Issues

1. **"No HEIC files found"**
   - Check if the folder path is correct
   - Ensure files have .heic or .heif extensions

2. **"Permission denied"**
   - Run with administrator privileges
   - Check folder write permissions

3. **"Module not found"**
   - Install required dependencies: `pip install pillow-heif pillow piexif`

4. **"Conversion failed"**
   - Check if the HEIC file is corrupted
   - Ensure sufficient disk space

### Supported File Extensions
- `.heic`
- `.heif`
- `.HEIC` (case insensitive)
- `.HEIF` (case insensitive)

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
