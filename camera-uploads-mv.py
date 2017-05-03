import argparse

def validate_path(string):
    if os.path.isdir(string):
        return string
    raise argparse.ArgumentTypeError('Directory must exist')

def main():
    parser = argparse.ArgumentParser(
        description='Organize photos in camera uploads folder into separate tree structure by date.'
    )
    parser.add_argument(
        'Camera Uploads directory',
        metavar='C',
        type=validate_path,
        help='Path to directory (Camera Uploads) where photos need to be organized.')
    parser.add_argument(
        'Photos Directory',
        metavar='P',
        type=validate_path,
        help='Path to (Photos) directory where photos should be organized into tree by date.')

    args = parser.parse_args()
    print(args)

if __name__ == '__main__':
    main()
