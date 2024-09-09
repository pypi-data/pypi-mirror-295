# This file is placed in the Public Domain.


"console"


import _thread


from .client  import Client, command
from .event   import Event


class Console(Client):

    "Console"

    def callback(self, evt):
        "wait for callback."
        Client.callback(self, evt)
        evt.wait()

    def poll(self):
        "poll console and create event."
        evt      = Event()
        evt.txt  = input("> ")
        evt.type = "command"
        return evt


def __dir__():
    return (
        'Console',
    )
