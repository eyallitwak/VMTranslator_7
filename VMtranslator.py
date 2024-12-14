import VMParser
import CodeWriter


def translate(vm_file):
    """Drives the translation proccess of a single .vm file.

    Args:
        vm_file (str): Path (either  relative or absolute) of the .vm file to be translated.
    """
    parser = VMParser.Parser(vm_file)
    writer = CodeWriter.CodeWriter(vm_file)

    while parser.has_more_lines():
        parser.advance()
        writer.comment(parser.current_command)
        if parser.command_type() == 'C_ARITHMETIC':
            writer.write_arithmetic(parser.arg1())
        else:
            writer.write_push_pop(parser.command_type(),
                                  parser.arg1(), parser.arg2())

    writer.close()
