from collections import deque

from .signal import Signal
from .exceptions import QueueCantQueueNonSignalInstance


class Queue(object):
    """
    Queue signals with :py:meth:`queue` and emit them with :py:meth:`flush`.

    To create a queue, instanciate a queue object:

    >>> queue = Queue()

    Consider a basic signal and slot:

    >>> something = Signal()
    >>> def do_something(**kwargs):
    ...     print('I did something with %s' % kwargs)
    ...
    >>> something.connect(do_something)

    Instead of calling ``something.emit()`` which would execute callbacks
    directly, you could queue as many calls as you wish with :py:meth:`queue`:

    >>> queue.queue(something)
    >>> queue.queue(something, foo='bar')

    And let the queue emit them all at once with :py:meth:`flush`:

    >>> queue.flush()
    I did something with {}
    I did something with {'foo': 'bar'}
    """
    def __init__(self):
        self._queue = deque()

    def queue(self, signal, **kwargs):
        """
        Queue a given :py:class:`Signal` emission with kwargs:

        >>> import pytest
        >>> with pytest.raises(QueueCantQueueNonSignalInstance):
        ...     Queue().queue('foo')
        """
        if not isinstance(signal, Signal):
            raise QueueCantQueueNonSignalInstance(self, signal)

        self._queue.append((signal, kwargs))

    def flush(self):
        """
        Flush a queue by emiting all signals one by one.
        """
        while len(self._queue):
            signal, kwargs = self._queue.popleft()
            signal.emit(**kwargs)
