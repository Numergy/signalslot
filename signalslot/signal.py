"""
Module defining the Signal class.
"""

import inspect

from . import exceptions


class Signal(object):
    """
    Define a signal by instanciating a :py:class:`Signal` object, ie.:

    >>> conf_pre_load = Signal()

    Optionaly, you can declare a list of argument names for this signal, ie.:

    >>> conf_pre_load = Signal(args=['conf'])

    Any callable can be connected to a Signal, it **must** accept keywords
    (``**kwargs``), ie.:

    >>> def yourmodule_conf(conf, **kwargs):
    ...     conf['yourmodule_option'] = 'foo'
    ...

    Connect your function to the signal using :py:meth:`connect`:

    >>> conf_pre_load.connect(yourmodule_conf)

    Emit the signal to call all connected callbacks using
    :py:meth:`emit`:

    >>> conf = {}
    >>> conf_pre_load.emit(conf=conf)
    >>> conf
    {'yourmodule_option': 'foo'}

    Note that you may disconnect a callback from a signal if it is already
    connected:

    >>> conf_pre_load.is_connected(yourmodule_conf)
    True
    >>> conf_pre_load.disconnect(yourmodule_conf)
    >>> conf_pre_load.is_connected(yourmodule_conf)
    False
    """
    def __init__(self, args=None, name=None):
        self.slots = []
        self.args = args or []
        self.name = name

    def connect(self, slot):
        """
        Connect a callback ``slot`` to this signal.
        """
        if inspect.getargspec(slot).keywords is None:
            raise exceptions.SlotMustAcceptKeywords(self, slot)

        if not self.is_connected(slot):
            self.slots.append(slot)

    def is_connected(self, slot):
        """
        Check if a callback ``slot`` is connected to this signal.
        """
        return slot in self.slots

    def disconnect(self, slot):
        """
        Disconnect a slot from a signal if it is connected else do nothing.
        """
        if self.is_connected(slot):
            self.slots.pop(self.slots.index(slot))

    def emit(self, **kwargs):
        """
        Emit this signal which will execute every connected callback ``slot``,
        passing keyword arguments.

        If a slot returns anything other than None, then :py:meth:`emit` will
        return that value preventing any other slot from being called.

        >>> need_something = Signal()
        >>> def get_something(**kwargs):
        ...     return 'got something'
        ...
        >>> def make_something(**kwargs):
        ...     print('I will not be called')
        ...
        >>> need_something.connect(get_something)
        >>> need_something.connect(make_something)
        >>> need_something.emit()
        'got something'
        """
        for slot in self.slots:
            result = slot(**kwargs)

            if result is not None:
                return result

    def __eq__(self, other):
        """
        Return True if other has the same slots connected.

        >>> a = Signal()
        >>> b = Signal()
        >>> a == b
        True
        >>> def slot(**kwargs):
        ...    pass
        ...
        >>> a.connect(slot)
        >>> a == b
        False
        >>> b.connect(slot)
        >>> a == b
        True
        """
        return self.slots == other.slots

    def __repr__(self):
        return '<signalslot.Signal: %s>' % (self.name or 'NO_NAME')
