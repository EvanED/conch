import subprocess
import pty
import os
import signal
import time
import fcntl
import errno

def read_available(f):
    out = ""
    try:
        while True:
            out += f.read()
    except IOError as e:
        if e.errno in [errno.EAGAIN, errno.EWOULDBLOCK]:
            return out
        raise

(child, masterfd) = pty.fork()

if child == 0:
    os.execl("/bin/bash", "/bin/bash")

c = os.fdopen(masterfd, "r+")
fcntl.fcntl(masterfd, fcntl.F_SETFL, os.O_NONBLOCK)

c.write("ls s")
time.sleep(1)
print "Dumping <{}>".format(read_available(c))
time.sleep(0.01)
print "Dumping <{}>".format(read_available(c))

c.write("\t\t")
time.sleep(0.01)
print "Completion <{}>".format(read_available(c))
time.sleep(1)
print "Completion <{}>".format(read_available(c))

os.kill(child, signal.SIGKILL)
os.waitpid(child, 0)

