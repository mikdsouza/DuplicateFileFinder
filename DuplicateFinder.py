import argparse
import os


parser = argparse.ArgumentParser(description='Find duplicates in a file structure')

parser.add_argument('--input_directory', type=str, help='Input directory. Leave blank to use current directory')
parser.add_argument('--output_file', type=str, help='Filename of the output file')
group = parser.add_mutually_exclusive_group()
group.add_argument('-f', '--filename', action="store_true", help='Look for duplicates based on the file name. '
                                                                 'Used if nothing else is specified')
group.add_argument('-s', '--hashcheck', action="store_true", help='Look for duplicates based on the MD5 hash of the '
                                                                  'file')
group.add_argument('-c', '--contents', action="store_true", help='Look for duplicates based on the contents of the '
                                                                 'file')

args = parser.parse_args()

input_directory = os.getcwd()
output_file = "dup.txt"

if args.input_directory != "":
    input_directory = args.input_directory

if args.output_file != "":
    output_file = args.output_file

if args.filename:
    pass
else:
    print("You must select -f")
    args.usage()
