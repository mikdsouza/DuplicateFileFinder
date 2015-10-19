import argparse
import hashlib
import os
from os import listdir
from os.path import basename, isfile, join


def find_dup_filename(input_dir, out, key_function):
    file_list = get_file_list(input_dir)
    file_check = {}

    for filename in file_list:
        key = key_function(filename)

        if key in file_check:
            file_check[key].append(filename)
        else:
            file_check[key] = [filename]

    for k, v in file_check.items():
        if len(v) > 1:
            out.write("Duplicate file: " + k + "\n")
            out.write(str(v) + "\n\n")

    return file_check


def get_file_list(input_dir):
    """
    Recursively gets all the files in the directory
    :param input_dir: Directory name
    :return: List of all the file names will full paths
    """
    # Tuples containing (name, is it a file?)
    dir_stuff = [(join(input_dir, s), isfile(join(input_dir, s))) for s in listdir(input_dir)]
    result = []

    for thing in dir_stuff:
        if thing[1]:  # file
            result.append(thing[0])
        else:  # directory
            result += get_file_list(thing[0])

    return result


def main():
    parser = argparse.ArgumentParser(description='Find duplicates in a file structure')

    parser.add_argument('--input_directory', type=str, help='Input directory. Leave blank to use current directory')
    parser.add_argument('--output_file', type=str, help='Filename of the output file')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f', '--filename', action="store_true", help='Look for duplicates based on the file name. '
                                                                     'Used if nothing else is specified')
    group.add_argument('-s', '--hashcheck', action="store_true",
                       help='Look for duplicates based on the MD5 hash of the file. This method is slow')
    group.add_argument('-c', '--contents', action="store_true", help='Look for duplicates based on the contents of the '
                                                                     'file. This method is very slow')

    args = parser.parse_args()

    input_directory = os.getcwd()
    output_file = "dup.txt"

    if args.input_directory is not None:
        input_directory = args.input_directory

    if args.output_file is not None:
        output_file = args.output_file

    if args.filename:
        file = open(output_file, 'w')
        find_dup_filename(input_directory, file, lambda x: basename(x))
        file.close()
    elif args.hashcheck:
        file = open(output_file, 'w')
        find_dup_filename(input_directory, file, lambda x: hashlib.md5(open(x, 'rb').read()).hexdigest())
        file.close()
    else:
        print("You must select a duplicate finding method")
        parser.print_help()


main()
