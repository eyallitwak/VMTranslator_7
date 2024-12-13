class Parser:

    def __init__(self, source_file):
        self.current_command = ''  # initially there is no current command
        self.command_index = 0
        self.all_commands = []

        # reads entire file into a list line-by-line
        # while removing comments and whitespace
        with open(source_file, 'r') as file:
            self.all_commands = file.read().splitlines()
            self.all_commands = [line.strip().split('//')[0]
                                 for line in self.all_commands]
            self.all_commands = [
                line for line in self.all_commands if line is not None]

    def has_more_lines(self):
        return self.command_index < len(self.all_commands)

    def advance(self):
        self.current_command = self.all_commands[self.command_index]
        self.command_index += 1

    def command_type(self):
        cmd = self.current_command.split(' ')[0]
        types = {'add': 'C_ARITHMETIC', 'sub': 'C_ARITHMETIC',
                 'neg': 'C_ARITHMETIC', 'eq': 'C_ARITHMETIC',
                 'gt': 'C_ARITHMETIC', 'lt': 'C_ARITHMETIC',
                 'and': 'C_ARITHMETIC', 'or': 'C_ARITHMETIC',
                 'not': 'C_ARITHMETIC', 'push': 'C_PUSH',
                 'pop': 'C_POP'}
        return types[cmd]

    def arg1(self) -> str:
        if self.command_type() == 'C_ARITHMETIC':
            return self.current_command.split(' ')[0]
        else:
            return self.current_command.split(' ')[1]

    def arg2(self) -> int:
        return int(self.current_command.split(' ')[2])
