# This file is placed in the Public Domain.
# pylint: disable=R0903


"commands"


class Commands:

    "Commands"

    cmds     = {}
    modnames = {}

    @staticmethod
    def add(func):
        "add command."
        Commands.cmds[func.__name__] = func
        if func.__module__ != "__main__":
            Commands.modnames[func.__name__] = func.__module__


def __dir__():
    return (
        'Commands',
    )
