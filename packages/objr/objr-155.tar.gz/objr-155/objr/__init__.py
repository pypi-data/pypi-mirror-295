# This file is placed in the Public Domain.


"""objects runtime


SYNOPSIS

    >>> from objr import Reactor
    >>> reactor.register("command", command)
    >>> reactor.start()


INSTALL

    $ pip install objr


DESCRIPTION

    OBJR is a threaded, defer exceptions for later, keep on running
    callback engine.


COPYRIGHT

    OBJR is Public Domain.

"""


from . import reactor


from .reactor  import *


def __dir__():
    return (
        'Reactor',
    )
