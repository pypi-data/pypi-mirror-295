#!/usr/bin/python
import os
import sys
import time


def get_pid_filename(pidname):
    return f"{os.environ['XDG_RUNTIME_DIR']}/{pidname}.pid"


def exec():
    """
    Execute process and store pid in XDG_RUNTIME_DIR
    """
    pid_filename = get_pid_filename(sys.argv[1])
    with open(pid_filename, "w") as pidfile:
        pidfile.write(str(os.getpid()))
    os.execvp(sys.argv[2], sys.argv[2:])


def waitpid():
    """
    Wait until process of pid ends
    """
    pid_filename = get_pid_filename(sys.argv[1])
    if not os.path.exists(pid_filename):
        return
    with open(pid_filename) as pidfile:
        pid = int(pidfile.read())
    while 1:
        time.sleep(0.1)
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            break
    os.unlink(pid_filename)
