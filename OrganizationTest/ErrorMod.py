# This file will handle Custom Error Calls
import sys


class Error():
    # Ansi Code for changing back to white
    lEnd = '\033[0m'

    # Ansi Code to turn text Red
    BrightRed = '\033[1;31m'

    # Identifier of an error
    ErrorMsg = '[ERROR] '

    def print(err, stopping=True):
        print(Error.BrightRed + Error.ErrorMsg + err + Error.lEnd)
        if stopping:
            sys.exit()
