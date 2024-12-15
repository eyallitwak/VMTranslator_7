import VMtranslator
import sys
import os


def main():
    # Terminate if not given exactly 1 input
    if len(sys.argv) != 2:
        print("Error: exactly one (1) .vm file or directory as input expected")
        sys.exit()

    file_name = sys.argv[1]

    # When receiving a file as input
    if os.path.isfile(file_name):

        # Terminate if given input is not .vm
        if os.path.splitext(file_name)[1] != '.vm':
            print("Error: input file should have the extension \".vm\"")
            sys.exit()

        VMtranslator.translate(file_name)

    # When receiving a directory of .vm files as input
    elif os.path.isdir(file_name):
        files = os.listdir(file_name)
        files = [os.path.join(file_name, f)
                 for f in files if os.path.splitext(f)[1] == '.vm']

        for f in files:
            VMtranslator.translate(f)

    # Terminate if given input is not an existing file or directory
    else:
        print("Error: given input file doesn't exist")
        sys.exit()


if __name__ == '__main__':
    main()
