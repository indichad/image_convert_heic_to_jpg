import os
import sys
import argparse
from pathlib import Path
from typing import List, Optional
import logging

from pillow_heif import register_heif_opener
from PIL import Image, ExifTags
import piexif


# Register HEIF opener with Pillow
register_heif_opener()


class HEICToJPGConverter:
    """A class to convert HEIC images to JPG format while preserving metadata."""
    
    def __init__(self, quality: int = 95, verbose: bool = False):
        """
        Initialize the converter.
        
        Args:
            quality: JPG quality (1-100, default: 95)
            verbose: Enable verbose logging
        """
        self.quality = quality
        self.verbose = verbose
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging configuration."""
        level = logging.DEBUG if self.verbose else logging.INFO
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)
    
    def find_heic_files(self, folder_path: Path) -> List[Path]:
        """
        Find all HEIC files in the given folder and subfolders.
        
        Args:
            folder_path: Path to the folder to search
            
        Returns:
            List of HEIC file paths
        """
        heic_extensions = {'.heic', '.heif', '.HEIC', '.HEIF'}
        heic_files = []
        
        try:
            for file_path in folder_path.rglob('*'):
                if file_path.is_file() and file_path.suffix in heic_extensions:
                    heic_files.append(file_path)
                    self.logger.debug(f"Found HEIC file: {file_path}")
        except Exception as e:
            self.logger.error(f"Error searching for HEIC files in {folder_path}: {e}")
            
        return heic_files
    
    def preserve_metadata(self, source_image: Image.Image, target_path: Path) -> dict:
        """
        Extract and preserve metadata from the source image.
        
        Args:
            source_image: Source PIL Image object
            target_path: Target file path for saving metadata info
            
        Returns:
            Dictionary containing metadata information
        """
        metadata_info = {}
        
        try:
            # Get comprehensive image info (includes EXIF, XMP, ICC profiles, etc.)
            if hasattr(source_image, 'info') and source_image.info:
                metadata_info['info'] = source_image.info.copy()
                self.logger.debug(f"Extracted image info with {len(source_image.info)} items")
                
                # Extract EXIF data if present in info
                if 'exif' in source_image.info:
                    metadata_info['exif_raw'] = source_image.info['exif']
                    self.logger.debug(f"Found raw EXIF data: {len(source_image.info['exif'])} bytes")
                
                # Extract XMP data if present
                if 'xmp' in source_image.info:
                    metadata_info['xmp'] = source_image.info['xmp']
                    self.logger.debug(f"Found XMP data: {len(source_image.info['xmp'])} bytes")
                
                # Extract ICC profile if present
                if 'icc_profile' in source_image.info:
                    metadata_info['icc_profile'] = source_image.info['icc_profile']
                    self.logger.debug(f"Found ICC profile: {len(source_image.info['icc_profile'])} bytes")
            
            # Try alternative EXIF extraction method
            try:
                exif_dict = source_image.getexif()
                if exif_dict:
                    metadata_info['exif_dict'] = dict(exif_dict)
                    self.logger.debug(f"Extracted EXIF dictionary with {len(exif_dict)} entries")
            except Exception as e:
                self.logger.debug(f"Alternative EXIF extraction failed: {e}")
            
            # Try legacy _getexif method
            try:
                if hasattr(source_image, '_getexif') and source_image._getexif():
                    legacy_exif = source_image._getexif()
                    metadata_info['legacy_exif'] = legacy_exif
                    self.logger.debug(f"Extracted legacy EXIF data with {len(legacy_exif)} entries")
            except Exception as e:
                self.logger.debug(f"Legacy EXIF extraction failed: {e}")
                
        except Exception as e:
            self.logger.warning(f"Could not extract some metadata: {e}")
            
        return metadata_info
    
    def verify_metadata_preservation(self, original_path: Path, converted_path: Path) -> dict:
        """
        Verify that metadata was preserved in the converted image.
        
        Args:
            original_path: Path to original HEIC file
            converted_path: Path to converted JPG file
            
        Returns:
            Dictionary with comparison results
        """
        verification = {
            'exif_preserved': False,
            'icc_profile_preserved': False,
            'metadata_count_original': 0,
            'metadata_count_converted': 0,
            'preserved_tags': []
        }
        
        try:
            # Check original metadata
            with Image.open(original_path) as original_img:
                original_metadata = self.preserve_metadata(original_img, converted_path)
                verification['metadata_count_original'] = len(original_metadata.get('info', {}))
            
            # Check converted metadata
            with Image.open(converted_path) as converted_img:
                converted_exif = converted_img.getexif()
                converted_info = converted_img.info
                
                verification['metadata_count_converted'] = len(converted_info)
                verification['exif_preserved'] = len(converted_exif) > 0
                verification['icc_profile_preserved'] = 'icc_profile' in converted_info
                
                # Count preserved EXIF tags
                if converted_exif:
                    verification['preserved_tags'] = list(converted_exif.keys())
                
                self.logger.debug(f"Verification: Original metadata items: {verification['metadata_count_original']}, "
                                f"Converted metadata items: {verification['metadata_count_converted']}, "
                                f"EXIF tags preserved: {len(verification['preserved_tags'])}")
                
        except Exception as e:
            self.logger.warning(f"Could not verify metadata preservation: {e}")
        
        return verification
    
    def convert_single_file(self, source_path: Path, output_folder: Optional[Path] = None) -> bool:
        """
        Convert a single HEIC file to JPG format.
        
        Args:
            source_path: Path to the source HEIC file
            output_folder: Optional output folder (default: same as source)
            
        Returns:
            True if conversion successful, False otherwise
        """
        try:
            # Determine output path
            if output_folder:
                output_folder.mkdir(parents=True, exist_ok=True)
                output_path = output_folder / f"{source_path.stem}.jpg"
            else:
                output_path = source_path.parent / f"{source_path.stem}.jpg"
            
            # Skip if output already exists
            if output_path.exists():
                self.logger.info(f"Skipping {source_path.name} - output already exists")
                return True
            
            self.logger.info(f"Converting: {source_path.name} -> {output_path.name}")
            
            # Open and convert the image
            with Image.open(source_path) as img:
                # Convert to RGB if necessary (HEIC can be in different color modes)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Preserve metadata
                metadata = self.preserve_metadata(img, output_path)
                
                # Prepare save arguments with comprehensive metadata preservation
                save_kwargs = {
                    'format': 'JPEG',
                    'quality': self.quality,
                    'optimize': True
                }
                
                # Add EXIF data - try multiple sources
                exif_data = None
                
                # First try: raw EXIF from image info
                if 'exif_raw' in metadata:
                    try:
                        exif_data = metadata['exif_raw']
                        self.logger.debug("Using raw EXIF data from image info")
                    except Exception as e:
                        self.logger.debug(f"Failed to use raw EXIF: {e}")
                
                # Second try: convert EXIF dictionary using piexif
                if not exif_data and 'exif_dict' in metadata:
                    try:
                        # Convert PIL EXIF dict to piexif format
                        exif_ifd = {}
                        for tag_id, value in metadata['exif_dict'].items():
                            try:
                                # Only include valid EXIF tags
                                if isinstance(tag_id, int) and tag_id in range(0, 65536):
                                    exif_ifd[tag_id] = value
                            except Exception:
                                continue
                        
                        if exif_ifd:
                            exif_data = piexif.dump({"Exif": exif_ifd})
                            self.logger.debug(f"Converted EXIF dictionary to bytes: {len(exif_ifd)} tags")
                    except Exception as e:
                        self.logger.debug(f"Failed to convert EXIF dictionary: {e}")
                
                # Third try: legacy EXIF
                if not exif_data and 'legacy_exif' in metadata:
                    try:
                        exif_data = piexif.dump({"Exif": metadata['legacy_exif']})
                        self.logger.debug("Using legacy EXIF data")
                    except Exception as e:
                        self.logger.debug(f"Failed to use legacy EXIF: {e}")
                
                # Add EXIF to save parameters
                if exif_data:
                    save_kwargs['exif'] = exif_data
                    self.logger.debug("EXIF data will be preserved in JPG")
                else:
                    self.logger.warning("No EXIF data could be preserved")
                
                # Add ICC profile if available
                if 'icc_profile' in metadata:
                    try:
                        save_kwargs['icc_profile'] = metadata['icc_profile']
                        self.logger.debug("ICC color profile will be preserved")
                    except Exception as e:
                        self.logger.debug(f"Failed to preserve ICC profile: {e}")
                
                # Add other metadata if supported
                if 'info' in metadata:
                    # Preserve any other metadata that PIL can handle
                    for key, value in metadata['info'].items():
                        if key not in ['exif', 'icc_profile', 'xmp'] and isinstance(value, (str, bytes, int, float)):
                            try:
                                save_kwargs[key] = value
                            except Exception:
                                pass  # Some metadata might not be compatible with JPEG
                
                # Save the image with all preserved metadata
                img.save(output_path, **save_kwargs)
                
            # Verify metadata preservation if verbose mode is enabled
            if self.verbose:
                verification = self.verify_metadata_preservation(source_path, output_path)
                if verification['exif_preserved']:
                    self.logger.info(f"✓ EXIF preserved: {len(verification['preserved_tags'])} tags")
                else:
                    self.logger.warning("✗ No EXIF data preserved")
                
                if verification['icc_profile_preserved']:
                    self.logger.info("✓ ICC color profile preserved")
                else:
                    self.logger.debug("No ICC profile to preserve")
                
            self.logger.info(f"Successfully converted: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error converting {source_path}: {e}")
            return False
    
    def convert_folder(self, input_folder: str, output_folder: Optional[str] = None) -> dict:
        """
        Convert all HEIC files in a folder to JPG format.
        
        Args:
            input_folder: Path to input folder containing HEIC files
            output_folder: Optional output folder path
            
        Returns:
            Dictionary with conversion statistics
        """
        input_path = Path(input_folder)
        output_path = Path(output_folder) if output_folder else None
        
        if not input_path.exists():
            raise ValueError(f"Input folder does not exist: {input_folder}")
        
        if not input_path.is_dir():
            raise ValueError(f"Input path is not a directory: {input_folder}")
        
        # Find all HEIC files
        heic_files = self.find_heic_files(input_path)
        
        if not heic_files:
            self.logger.warning(f"No HEIC files found in {input_folder}")
            return {'total': 0, 'converted': 0, 'failed': 0, 'skipped': 0}
        
        self.logger.info(f"Found {len(heic_files)} HEIC files to convert")
        
        # Convert each file
        stats = {'total': len(heic_files), 'converted': 0, 'failed': 0, 'skipped': 0}
        
        for heic_file in heic_files:
            try:
                # Maintain folder structure if output folder is specified
                if output_path:
                    relative_path = heic_file.relative_to(input_path)
                    file_output_folder = output_path / relative_path.parent
                else:
                    file_output_folder = None
                
                success = self.convert_single_file(heic_file, file_output_folder)
                
                if success:
                    stats['converted'] += 1
                else:
                    stats['failed'] += 1
                    
            except Exception as e:
                self.logger.error(f"Unexpected error processing {heic_file}: {e}")
                stats['failed'] += 1
        
        # Print summary
        self.logger.info(f"""
Conversion Summary:
  Total files: {stats['total']}
  Converted: {stats['converted']}
  Failed: {stats['failed']}
  Success rate: {(stats['converted'] / stats['total'] * 100):.1f}%
        """)
        
        return stats


def main():
    """Main function to handle command line arguments and run the converter."""
    parser = argparse.ArgumentParser(
        description='Convert HEIC images to JPG format while preserving metadata'
    )
    parser.add_argument(
        'input_folder',
        help='Path to folder containing HEIC images'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output folder (default: same as input folder)'
    )
    parser.add_argument(
        '-q', '--quality',
        type=int,
        default=95,
        help='JPG quality (1-100, default: 95)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Validate quality
    if not 1 <= args.quality <= 100:
        print("Error: Quality must be between 1 and 100")
        sys.exit(1)
    
    # Create converter
    converter = HEICToJPGConverter(quality=args.quality, verbose=args.verbose)
    
    try:
        # Convert files
        stats = converter.convert_folder(args.input_folder, args.output)
        
        # Exit with appropriate code
        if stats['failed'] == 0:
            sys.exit(0)  # Success
        elif stats['converted'] > 0:
            sys.exit(1)  # Partial success
        else:
            sys.exit(2)  # Complete failure
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(3)


if __name__ == "__main__":
    main()
