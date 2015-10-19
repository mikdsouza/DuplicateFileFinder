import argparse
import hashlib
import os
from os import listdir
from os.path import basename, isfile, join


def find_dup_filename(input_dir, out, key_function):
    """
    Finds duplicates based on a key_function. Duplicate keys are considered as duplicate files
    :param input_dir: Directory to scan recursively
    :param out: Write to write output to. Can be None to not write anything
    :param key_function: Function to prove a key based on the filename
    :return: A dict containing the key and the list of matching files
    """
    file_list = get_file_list(input_dir)
    file_check = {}

    for filename in file_list:
        key = key_function(filename)

        if key in file_check:
            file_check[key].append(filename)
        else:
            file_check[key] = [filename]

    if out is not None:
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


def full_file_check(file_check_dict, out, key_function):
    """
    This function is used to matching files with matching keys from the find_dup_filename method and to carry out a
    secondary hash to create a double match of content
    :param file_check_dict: A dictionary mapping the primary hash key to the list of file(s) with that key
    :param out: A file to write output to. Can be None
    :param key_function: A secondary hash function
    :return: A dict of the primary key mapping to a dict of the secondary key mapping to a list of files
    """

    # We are only interested in the duplicates
    duplicates = {key: file_list for key, file_list in file_check_dict.items() if len(file_list) > 1}
    duplicates_dict = {}

    for key, value in duplicates.items():
        sha_duplicates = {}

        for filename in value:
            secondary_key = key_function(filename)

            if secondary_key in sha_duplicates:
                sha_duplicates[secondary_key].append(filename)
            else:
                sha_duplicates[secondary_key] = [filename]

        duplicates_dict[key] = sha_duplicates

    if out is not None:
        for key1, value1 in duplicates_dict.items():
            for key2, value2 in value1.items():
                if len(value2) > 1:
                    out.write('Duplicate with primary hash: {0} and secondary hash: {1}\n'.format(key1, key2))
                    out.write(str(value2) + "\n\n")

    return duplicates_dict


def main():
    parser = argparse.ArgumentParser(description='Find duplicates in a file structure')

    parser.add_argument('--input-directory', type=str, help='Input directory. Leave blank to use current directory')
    parser.add_argument('--output-file', type=str, help='Filename of the output file')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f', '--filename', action="store_true", help='Look for duplicates based on the file name')
    group.add_argument('-s', '--hashcheck', action="store_true",
                       help='Look for duplicates based on the MD5 hash of the file. This method is slow. Output is a '
                            'list of possible duplicates')
    group.add_argument('-d', '--double-hashcheck', action="store_true",
                       help='Look for duplicates based on MD5 and SHA224. This method is very slow. Output is a list of'
                            ' very likely duplicates')

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
    elif args.double_hashcheck:
        file = open(output_file, 'w')
        file_check = find_dup_filename(input_directory, None, lambda x: hashlib.md5(open(x, 'rb').read()).hexdigest())
        full_file_check(file_check, file, lambda x: hashlib.sha224(open(x, 'rb').read()).hexdigest())
        file.close()
    else:
        print("You must select a duplicate finding method")
        parser.print_help()


main()
