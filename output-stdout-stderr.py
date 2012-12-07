import sys
import time

print "standard output"
sys.stdout.flush()
time.sleep(1)
print >> sys.stderr, "standard error"
time.sleep(1)
print "standard output again"
time.sleep(1)
print >> sys.stderr, "standard error again"
