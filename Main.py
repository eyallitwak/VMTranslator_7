import VMtranslator
import sys
import os


def main():
    if len(sys.argv) != 2:
        print("Error: exactly one (1) .vm file or directory as input")
        return

    file_name = sys.argv[1]

    if os.path.splitext(file_name)[1] != '.vm':
        print("Error: input file shpuld have the extension \".vm\"")
        return

    if not os.path.isfile(file_name):
        print("Error: given input file doesn't exist")

    VMtranslator.translate(file_name)
