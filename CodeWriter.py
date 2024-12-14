import os


class CodeWriter:
    comp_index = 0  # index to label comparison operations, since they need labeling

    def __init__(self, dest_file):
        """Creates a CodeWriter object, that will write to the specified file.

        Args:
            dest_file (path): Path to create the output file.
        """
        self.path = dest_file.split('.')[0]+'.asm'
        self.file = open(self.path, 'w+')
        self.file_name = os.path.basename(self.path)
        self.push_pop_dict = {'local': 'LCL',
                              'argument': 'ARG',
                              'this': 'THIS',
                              'that': 'THAT',
                              'temp': 5, }
        self.op_dict = {'add': '+',
                        'sub': '-',
                        'neg': '-',
                        'eq': 'EQ',
                        'gt': 'GT',
                        'lt': 'LT',
                        'and': '&',
                        'or': '|',
                        'not': '!'}

    def write_arithmetic(self, operator):
        asm_command = ''
        if operator == 'neg' or operator == 'not':
            asm_command = self.one_operand(operator)
        elif operator == 'eq' or operator == 'gt' or operator == 'lt':
            asm_command = self.comparison_op(operator)
        else:
            asm_command = self.two_operands(operator)
        self.file.write(asm_command)
        pass

    def write_push_pop(self, command_type, segment, index):
        asm_command = ''
        if command_type == 'C_PUSH':
            if segment == 'constant':
                asm_command = self.push_constant(index)
            elif command_type == 'static':
                asm_command = self.push_static(index)
            else:
                asm_command = self.push(segment, index)
        else:
            if segment == 'static':
                asm_command = self.pop_static(index)
            else:
                asm_command = self.pop(segment, index)
        self.file.write(asm_command)

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
        return lines

    def push(self, segment, index):
        """Writes appropriate ASM commands that implement pushing from local, argument, this, that, temp or pointer.

        Args:
            segment (str): The segment to push from.
            index (int): The offset index in specified segment.
        """
        if segment == 'pointer':
            segment = 'THAT' if index == 1 else 'THIS'
            index = 0
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
    M=M+1'''.format(seg=self.push_pop_dict[segment], i=index)
        return lines

    def pop(self, segment, index):
        """Writes appropriate ASM commands that implement popping to local, argument, this, that, temp or pointer.

        Args:
            segment (str): The segment to pop into.
            index (int): The offset index in specified segment.
        """
        if segment == 'pointer':
            segment = 'THAT' if index == 1 else 'THIS'
            index = 0
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
    M=D'''.format(seg=self.push_pop_dict[segment], i=index)
        return lines

    def push_static(self, index):
        """Implements pushing from static segment.

        Args:
            index (int): The offset within the segment to push from.
        """
        lines = '''@{label}
    D=M
    // RAM[SP] = D
    @SP
    A=M
    M=D
    // SP++
    @SP
    M=M+1'''.format(label=self.file_name.split('.')[0]+'.'+index)
        return lines

    def pop_static(self, index):
        """Implement popping into static segment.

        Args:
            index (int): The offset within the segment to pop into.
        """
        lines = '''M=M-1
    A=M
    D=M
    @{label}
    M=D'''.format(label=self.file_name.split('.')[0]+'.'+index)
        return lines

    def one_operand(self, op):
        lines = '''@SP
    M=M-1
    A=M
    M={}M
    @SP
    M=M+1'''.format(self.op_dict[op])
        return lines

    def two_operands(self, op):
        lines = '''@SP
    M=M-1
    A=M
    D=M
    @SP
    M=M-1
    A=M
    M=M{}D
    @SP
    M=M+1'''.format(self.op_dict[op])
        return lines

    def comparison_op(self, op):
        lines = '''@SP
    M=M-1
    A=M
    D=M
    @SP
    M=M-1
    A=M
    D=M-D
    @TRUE{c}
    D;J{o}
    D=0
    @FINISHCOMP{c}
    0;JMP
    (TRUE{c})
    D=-1
    (FINISHCOMP{c})
    @SP
    A=M
    M=D
    @SP
    M=M+1'''.format(o=self.comp_index[op], c=CodeWriter.comp_index)
        CodeWriter.comp_index += 1
        return lines

    def close(self):
        self.file.close()
