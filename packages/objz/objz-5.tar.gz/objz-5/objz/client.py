# This file is placed in the Public Domain.


"client"


from objr.reactor import Reactor
from objt.errors  import later
from objx.object  import Object


from .command import Commands
from .fleet   import Fleet
from .parse   import parse


class Client(Reactor):

    "Client"

    cache = Object()

    def __init__(self, outer=None):
        Reactor.__init__(self)
        self.register("command", command)
        Fleet.register(self)

    def dosay(self, channel, txt):
        "make say."
        self.raw(txt)

    def say(self, _channel, txt):
        "echo on verbose."
        self.raw(txt)

    def raw(self, txt):
        "print to screen."
        raise NotImplementedError


def command(bot, evt):
    "check for and run a command."
    parse(evt)
    func = Commands.cmds.get(evt.cmd, None)
    if func:
        try:
            func(evt)
        except Exception as ex:
            later(ex)
    if "ready" in dir(evt):
        evt.display()
        evt.ready()


def __dir__():
    return (
       'Client',
    )
