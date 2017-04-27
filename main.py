import argparse
import os
import datetime
import shutil

def validate_path(string):
    if os.path.isdir(string):
        return string
    raise argparse.ArgumentTypeError('Directory must exist')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Organize screenshots into folders by year. Duplicates are left in place.')
    parser.add_argument('path', metavar='P', type=validate_path,
                    help='Path to screenshots folder.')
    args = parser.parse_args()
    path = args.path

    screenshots = os.listdir(path)

    for screenshot in screenshots:
        if not screenshot.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            continue
        created = datetime.datetime.fromtimestamp(os.path.getctime(os.path.join(path, screenshot)))
        modified = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(path, screenshot)))
        year = created.year if created < modified else modified.year

        folder_path = os.path.join(path, str(year))
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)

        if os.path.exists(os.path.join(path, str(year), screenshot)):
            continue
        screenshot_path = os.path.join(path, screenshot)
        shutil.move(screenshot_path, folder_path)
