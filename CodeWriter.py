class CodeWriter:
    def __init__(self, dest_file):
        """Creates a CodeWriter object, that will write to the specified file.

        Args:
            dest_file (path): Path to create the output file.
        """
        self.file = open(dest_file, 'w')
        self.dict = {'local': 'LCL',
                     'argument': 'ARG',
                     'this': 'THIS',
                     'that': 'THAT'}

    def write_arithmetic(self, command):
        # TODO
        pass

    def write_push_pop(self, command_type, segment, index):
        # TODO
        pass

    def comment(self, command):
        """Writes the current VM line as a comment on the output file.

        Args:
            command: Current VM command.
        """
        line = '// '+str(command)+'\n'
        self.file.write(line)

    def push_constant(self, index):
        """Writes appropriate ASM commands that implement pushing a constant.

        Args:
            index (int): The constant value to push.
        """
        lines = '''// D = {n}
    @{n}
    D=A
    // RAM[SP] = D
    @SP
    A=M
    M=D
    // SP++
    @SP
    M=M+1\n'''.format(n=index)
        self.file.write(lines)

    def push(self, segment, index):
        """Writes appropriate ASM commands that implement pushing from local, argument, this or that.

        Args:
            segment (str): The segment to push from.
            index (int): The offset index in specified segment.
        """        
        lines = '''// D = RAM[{seg} + {i}]
    @{i}
    D=A
    @{seg}
    D=D+A
    A=D
    D=M
    // RAM[SP] = D
    @SP
    A=M
    M=D
    // SP++
    @SP
    M=M+1'''.format(seg=self.dict[segment], i=index)
        self.file.write(lines)

    def pop(self, segment, index):
        """Writes appropriate ASM commands that implement popping to local, argument, this or that.

        Args:
            segment (str): The segment to pop into.
            index (int): The offset index in specified segment.
        """        
        lines = '''// RAM[13] = {seg} + {i}
    @{i}
    D=A
    @{seg}
    D=D+A
    @R13
    M=D
    // SP--
    @SP
    M=M-1
    // RAM[R13] = RAM[SP]
    A=M
    D=M
    @13
    A=M
    M=D'''.format(seg=self.dict[segment], i=index)
        self.file.write(lines)
