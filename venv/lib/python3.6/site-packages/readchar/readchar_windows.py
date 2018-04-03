# -*- coding: utf-8 -*-
# Initially taken from:
# http://code.activestate.com/recipes/134892/#c9
# Thanks to Stephen Chappell
import msvcrt


def readchar():
    "Get a single character on Windows."

    while msvcrt.kbhit():
        msvcrt.getch()
    ch = msvcrt.getch()
    while ch in '\x00\xe0':
        msvcrt.getch()
        ch = msvcrt.getch()
    return ch.decode()
