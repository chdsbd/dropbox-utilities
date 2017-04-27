import argparse
import os

def validate_path(string):
    if os.path.isdir(string):
        return string
    raise argparse.ArgumentTypeError('Directory must exist')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Organize screenshots into folders by year.')
    parser.add_argument('path', metavar='P', type=validate_path,
                    help='Path to screenshots folder.')

    args = parser.parse_args()

