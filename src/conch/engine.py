import subprocess
import pty

class Process(object):
    def __init__(self, stdin, stdout):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stdout #??

def execute(ast):
    args = ast.get_argv()
    (child_pid, master_fd) = pty.fork()
    if child_pid == 0:
        # Child. master_fd is invalid
        os.execvp(args[0], args)
    stdout = os.fdopen(master_fd, "r", 0)
    stdin = os.fdopen(master_fd, "w", 0)

    return Process(stdin, stdout)
