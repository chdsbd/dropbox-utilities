# TODO: Make it reversable
import copy
import filecmp
import fnmatch
import sys
from os import walk
from os.path import expanduser, isfile, join, splitext
from random import randint
from shutil import copy, move

mv = False
# origin_path = os.path.expanduser('~/Dropbox/photos/')
# dest_path = os.path.expanduser('/Users/chris/Downloads/screenshots')
origin_path = expanduser(sys.argv[1])
dest_path = expanduser(sys.argv[2])
try:
    # Move false by default
    mv = bool(sys.argv[3])
    print("Moving files")
except IndexError:
    print("Copying only")


def main(origin, dest, file_type='*.png'):
    for dirpath, _, files in walk(origin):
        for photo in files:
            if fnmatch.fnmatch(photo, file_type):
                start = join(dirpath, photo)
                end = join(dest, photo)

                # New file
                if not isfile(end):
                    print('Copying/Moving "{}" to "{}"'.format(start, end))
                    if mv:
                        move(start, end)
                    else:
                        copy(start, end)
                    continue

                # Name collision
                if not filecmp.cmp(start, end):
                    photo, file_extention = splitext(photo)
                    photo += ('-unique-' + str(randint(0, 10000)) +\
                     file_extention)
                    print('Name Collision: "{0}" and "{1}"\
Copying/Moving to "{2}" with filename "{3}"'
                          .format(start, end, dest_path, photo))
                    end = join(dest, photo)
                    if mv:
                        move(start, end)
                    else:
                        copy(start, end)
                    continue

                # Duplicate file
                if filecmp.cmp(start, end):
                    print('Dupe: "{0}" "{1}"\n'.format(start, end))
                    # TODO: Create directory if not existant

                    dest += 'dupes/'
                    end = join(dest, photo)
                    if mv:
                        move(start, end)
                        print("Moving file")
                    else:
                        print("Leaving file")


if __name__ == '__main__':
    main(origin_path, dest_path)
