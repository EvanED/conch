import shlex

class FakeAst(object):
    def __init__(self, argv):
        self.argv = argv

    def get_argv(self):
        return self.argv


def parse_to_ast(command_string):
    return FakeAst(shlex.split(command_string))
