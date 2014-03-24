from signalslot import Signal


class DynamicState(object):
    """
    Base class for classes which require having dynamic states.

    .. py:attribute:: fetch_attribute

        Signal emited when a non-existent attribute is being accessed before
        AttributeError is raised.

    The dynamic state pattern attempts to solve a problem: having a property
    fetched OAOO (Once And Only Once) by a decoupled module.

    Subclass :py:class:`DynamicState` to implement the dynamic state pattern:

    >>> class YourObject(DynamicState):
    ...     pass

    Consider the following function, provided by another module,  which should
    compute the initial value for a particular attribute ``foo``:

    >>> def fetch_foo(obj, name, **kwargs):
    ...     if name != 'foo':
    ...         return  # not my responsability
    ...     return 'bar'
    ...

    Connect that function to ``YourObject.fetch_attribute`` signal as usual:

    >>> YourObject.fetch_attribute.connect(fetch_foo)

    Now, the first time ``YourObject.foo`` is accessed, it will emit
    ``YourObject.fetch_attribute`` which will execute every slot until one of
    them returns a non-None value:

    >>> test = YourObject()
    >>> assert test.foo == 'bar'

    However, if no slots are connected, or each of them return None, then a
    normal AttributeError is raised:

    >>> import pytest
    >>> with pytest.raises(AttributeError):
    ...     test.oops
    """
    fetch_attribute = Signal(args=['obj', 'name'])

    def __getattr__(self, name):
        if name not in self.__dict__:
            result = self.fetch_attribute.emit(obj=self, name=name)

            if result is not None:
                setattr(self, name, result)
            else:
                raise AttributeError

        return getattr(self, name)
