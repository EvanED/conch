import pty
import os
import signal
import time
import fcntl
import errno
import itertools
import re

def read_available(f):
    out = ""
    try:
        while True:
            out += f.read()
    except IOError as e:
        if e.errno in [errno.EAGAIN, errno.EWOULDBLOCK]:
            return out
        raise


def get_completions(command):
    (child, masterfd) = pty.fork()

    if child == 0:
        os.execl("/bin/bash", "/bin/bash") 

    c = os.fdopen(masterfd, "r+")
    fcntl.fcntl(masterfd, fcntl.F_SETFL, os.O_NONBLOCK)

    c.write("PS1=ZZZZ___CONCH___ZZZZ\n")
    c.write(command)
    time.sleep(1)
    print "Dumping <{}>".format(read_available(c))
    time.sleep(0.01)
    print "Dumping <{}>".format(read_available(c))

    c.write("\t\t")
    completion = ""
    while completion == "":
        completion = read_available(c)
        time.sleep(1)

    print "Completion <{}>".format(completion)
    
    lines = completion.splitlines()
    if lines[0].strip() == "\x07":
        lines = lines[1:]
    else:
        print "Warning: first line of completion was expected to be just a control character, but it wasn't"
    if lines[-1].startswith("ZZZZ___CONCH___ZZZZ"):
        lines = lines[:-1]
    else:
        print "Warning: last line of completion was expected to start with sentinel, but it didn't"

    suggestions = [re.split("  +", line) for line in lines]
    
    os.kill(child, signal.SIGKILL)
    os.waitpid(child, 0)

    return (suggestion
            for suggestion in itertools.chain(*suggestions)
            if suggestion)

