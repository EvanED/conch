import subprocess


def execute(ast):
    args = ast.get_argv()
    child = subprocess.Popen(args,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE)
    return child
