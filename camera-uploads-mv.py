import argparse
from datetime import datetime
import os
import pprint
import shutil

import exifread


def validate_path(path):
    """Return boolean of whether or not path is valid"""
    if os.path.isdir(path):
        return path
    raise argparse.ArgumentTypeError('Directory must exist')

def is_photo_video(photo_path):
    """Return boolean whether or not file is photo/video"""
    return photo_path.lower().endswith(
        (
        '.png',
        '.jpg',
        '.jpeg',
        '.bmp',
        '.tiff',
        '.mov',
        '.mp4')
        )

def find_creation_date(file_path):
    """Return datetime date for creation date for photo

        We check for EXIF photo creation metadata and use that if possible.
        We fall back to returning the oldest of the date modified or created
    """
    with open(file_path, 'rb') as f:
        try:
            created = exifread.process_file(f, details=False, stop_tag='DateTimeOriginal')['EXIF DateTimeOriginal']
            return datetime.strptime(str(created), '%Y:%m:%d %H:%M:%S')
        except KeyError:
            created = datetime.fromtimestamp(os.path.getctime(file_path))
            modified = datetime.fromtimestamp(os.path.getmtime(file_path))
            return created if created < modified else modified

def organize_photo(directory, filename, dest_root):
    """Move photo to proper directory under the photo path provided in arguments.

        If folder structure doesn't exist, it will be created.
    """
    date_created = find_creation_date(os.path.join(directory, filename))
    photo_path = os.path.join(directory, filename)
    destination_directory = os.path.join(dest_root, str(date_created.year), str(date_created.month))
    destination_path = os.path.join(destination_directory, filename)
    os.makedirs(destination_directory, exist_ok=True)
    print(f'Moving {photo_path} -> {destination_path}')
    shutil.move(photo_path, destination_path)

def main():
    parser = argparse.ArgumentParser(
        description='Organize photos in camera uploads folder into separate tree structure by date.'
    )
    parser.add_argument(
        'camera_uploads',
        metavar='U',
        type=validate_path,
        help='Path to Camera Uploads directory where photos need to be organized.')
    parser.add_argument(
        'photos_directory',
        metavar='P',
        type=validate_path,
        help='Path to Photos directory where photos should be organized into tree by date.')

    args = parser.parse_args()

    uploads_path = args.camera_uploads
    dest_path = args.photos_directory

    uploads_photos = os.listdir(uploads_path)

    for photo in uploads_photos:
        photo_path = os.path.join(uploads_path, photo)
        if not is_photo_video(photo_path):
            continue
        organize_photo(uploads_path, photo, dest_path)

if __name__ == '__main__':
    main()
