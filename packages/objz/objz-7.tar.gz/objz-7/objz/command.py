# This file is placed in the Public Domain.
# pylint: disable=R0903,W0718


"commands"


import time


from .thread import later


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


def command(bot, evt):
    "check for and run a command."
    func = Commands.cmds.get(evt.cmd, None)
    if func:
        try:
            func(evt)
            bot.display(evt)
        except Exception as ex:
            later(ex)
            time.sleep(1)


def __dir__():
    return (
        'Commands',
        'command',
        'parse'
    )
