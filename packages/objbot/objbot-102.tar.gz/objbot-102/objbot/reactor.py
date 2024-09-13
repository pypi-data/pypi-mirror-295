# This file is placed in the Public Domain.
# pylint: disable=R0903,W0105,W0212,W0613,W0718


"reactor"


import io
import queue
import threading
import traceback
import _thread


"errors"


class Errors:

    "Errors"

    errors = []

    @staticmethod
    def format(excp):
        "format an exception"
        result = ""
        stream = io.StringIO(
                             traceback.print_exception(
                                                       type(excp),
                                                       excp,
                                                       excp.__traceback__
                                                      )
                           )
        for line in stream.readlines():
            result += line + "\n"
        return result


def later(exc):
    "add an exception"
    excp = exc.with_traceback(exc.__traceback__)
    Errors.errors.append(excp)


def errors(outer):
    "display more errors."
    for exc in Errors.errors:
        outer(Errors.format(exc))


"reactor"


class Reactor:

    "Reactor"

    def __init__(self):
        self.cbs      = {}
        self.queue    = queue.Queue()
        self.stopped  = threading.Event()

    def callback(self, evt):
        "call callback based on event type."
        func = self.cbs.get(evt.type, None)
        if func:
            func(self, evt)

    def loop(self):
        "proces events until interrupted."
        while not self.stopped.is_set():
            try:
                evt = self.poll()
                self.callback(evt)
            except (KeyboardInterrupt, EOFError):
                _thread.interrupt_main()
            except Exception as ex:
                later(ex)

    def poll(self):
        "function to return event."
        return self.queue.get()

    def put(self, evt):
        "put event into the queue."
        self.queue.put_nowait(evt)

    def register(self, typ, cbs):
        "register callback for a type."
        self.cbs[typ] = cbs

    def start(self):
        "start the event loop."
        self.loop()

    def stop(self):
        "stop the event loop."
        self.stopped.set()


class Client(Reactor):

    "Client"

    def display(self, evt):
        "display event results."
        for text in evt.result:
            self.say(evt.channel, text)

    def dosay(self, channel, txt):
        "make say."
        self.raw(txt)

    def say(self, channel, txt):
        "echo on verbose."
        self.raw(txt)

    def raw(self, txt):
        "print to screen."
        raise NotImplementedError


"interface"


def __dir__():
    return (
        'Client',
        'Errors',
        'Reactor',
        'later',
        'errors'
    )
