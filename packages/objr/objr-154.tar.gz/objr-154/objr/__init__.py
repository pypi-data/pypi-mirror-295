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


from . import client, errors, reactor, repeater, thread, timer


from .client   import *
from .errors   import *
from .reactor  import *
from .repeater import *
from .thread   import *
from .timer    import *


def __dir__():
    return (
        'Client',
        'Errors',
        'errors',
        'later',
        'launch'
        'Reactor',
        'Repeater',
        'Thread',
        'Timer'
    )
