import VMtranslator
import sys
import os


def main():
    # Terminate if not given exactly 1 input
    if len(sys.argv) != 2:
        print("Error: exactly one (1) .vm file or directory as input expected")
        return

    file_name = sys.argv[1]

    # Terminate if given input is not .vm
    if os.path.splitext(file_name)[1] != '.vm':
        print("Error: input file should have the extension \".vm\"")
        return

    # Terminate if given input is not an existing file
    if not os.path.isfile(file_name):
        print("Error: given input file doesn't exist")
        return

    VMtranslator.translate(file_name)


if __name__ == '__main__':
    main()
