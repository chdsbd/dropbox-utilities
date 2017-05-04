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
            date_created = exifread.process_file(
                f,
                details=False,
                stop_tag='DateTimeOriginal')['EXIF DateTimeOriginal']
            return datetime.strptime(str(date_created), '%Y:%m:%d %H:%M:%S')
        except KeyError:
            date_created = datetime.fromtimestamp(os.path.getctime(file_path))
            date_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
            return date_created if date_created < date_modified else date_modified

def organize_file(directory, filename, destination_root, organize_by_year=False):
    """Move photo to proper directory under the photo path provided in arguments.

        If folder structure doesn't exist, it will be created.
    """
    creation_date = find_creation_date(os.path.join(directory, filename))
    file_path = os.path.join(directory, filename)
    destination_directory = os.path.join(destination_root, str(creation_date.year))
    if not organize_by_year:
        month = creation_date.strftime("%-m - %B")
        destination_directory = os.path.join(destination_directory, month)
    destination_path = os.path.join(destination_directory, filename)

    os.makedirs(destination_directory, exist_ok=True)

    if not os.path.exists(destination_path):
        shutil.move(file_path, destination_path)
    else:
        print(f'Warning: File already exists at {destination_path}, leaving file at {file_path}')

def main():
    parser = argparse.ArgumentParser(
        description='Organize photos in camera uploads folder into separate tree structure by date. Duplicates will be left alone.'
    )
    parser.add_argument(
        'camera_uploads',
        metavar='src',
        type=validate_path,
        help='Path to Camera Uploads directory where photos need to be organized.')
    parser.add_argument(
        'photos_directory',
        metavar='dest',
        type=validate_path,
        help='Path to Photos directory where photos should be organized into tree by date.')
    parser.add_argument(
        '-y',
        '--organize-by-year',
        action='store_true',
        help='Organize photos into folders by year instead of year and month.')

    args = parser.parse_args()

    uploads_path = args.camera_uploads
    dest_path = args.photos_directory
    organize_by_year = args.organize_by_year

    uploaded_photos = os.listdir(uploads_path)
    for photo in uploaded_photos:
        photo_path = os.path.join(uploads_path, photo)
        if is_photo_video(photo_path):
            organize_file(uploads_path, photo, dest_path, organize_by_year=organize_by_year)

if __name__ == '__main__':
    main()
