"""
remove_exif_datetime.py

Author: https://github.com/OneCoinOnePlay/

This script batch processes all images in a given directory to remove EXIF date and time metadata.
"""

import os
import piexif
from PIL import Image

def remove_exif_data(image_path):
    """Remove date, time digitized, and date time original metadata from an image."""
    with Image.open(image_path) as img:
        exif_dict = piexif.load(img.info['exif'])

        # The tags for DateTime, DateTimeOriginal, and DateTimeDigitized in the Exif data
        tags_to_remove = [
            piexif.ExifIFD.DateTimeOriginal, 
            piexif.ExifIFD.DateTimeDigitized, 
            piexif.ImageIFD.DateTime
        ]

        for tag in tags_to_remove:
            if tag in exif_dict["Exif"]:
                del exif_dict["Exif"][tag]
            if tag in exif_dict["0th"]:
                del exif_dict["0th"][tag]

        exif_bytes = piexif.dump(exif_dict)
        img.save(image_path, exif=exif_bytes)

def remove_date_from_images_in_directory(directory):
    """Scan all images in a directory and remove date, time digitized, and date time original metadata."""
    file_count = 0
    processed_count = 0
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_count += 1
                image_path = os.path.join(root, file)
                try:
                    remove_exif_data(image_path)
                    print(f"Processed {image_path}")
                    processed_count += 1
                except Exception as e:
                    print(f"Failed processing {image_path}. Error: {e}")

    print(f"Total image files found: {file_count}")
    print(f"Total image files processed: {processed_count}")

if __name__ == "__main__":
    directory_path = input("Enter the directory path: ").strip()

    # Ensure the path ends with the appropriate path separator
    if not directory_path.endswith(os.path.sep):
        directory_path += os.path.sep

    print(f"Using directory path: {directory_path}")

    remove_date_from_images_in_directory(directory_path)
    print("Processing complete.")
