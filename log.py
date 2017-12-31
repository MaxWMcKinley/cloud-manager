from __future__ import print_function
import sys

LOGFILE = 'aggiestack-log.txt'

# Print to stderr
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# Log a message to the logfile
def log(message):
    message += "\n"

    file = open(LOGFILE, 'a')
    file.write(message)
    file.close()

# Log a whole command to the logfile
# To be given as a list of components
def logCmd(argv):
    cmd = ''
    for arg in argv:
        cmd += arg + ' '

    cmd += "\n"

    file = open(LOGFILE, 'a')
    file.writelines(cmd)
    file.close()
