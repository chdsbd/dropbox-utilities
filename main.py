import argparse
import os
import time
import datetime
import pprint

def validate_path(string):
    if os.path.isdir(string):
        return string
    raise argparse.ArgumentTypeError('Directory must exist')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Organize screenshots into folders by year.')
    parser.add_argument('path', metavar='P', type=validate_path,
                    help='Path to screenshots folder.')

    args = parser.parse_args()
    screenshots = os.listdir(args.path)

    print(f'There are { len(screenshots) } items in this folder.')
    years = {}
    for screenshot in screenshots:
        created = datetime.datetime.fromtimestamp(os.path.getctime(os.path.join(args.path, screenshot)))
        modified = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(args.path, screenshot)))
        if created < modified:
            try:
                years[created.year] += 1
            except KeyError:
                years[created.year] = 1
        else:
            try:
                years[modified.year] += 1
            except KeyError:
                years[modified.year] = 1
    pprint.pprint(years)
