
from signalslot import Signal


class DynamicStateSignalDescriptor(property):
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()


class DynamicState(object):
    """
    Base class for classes which require having dynamic states.

    .. py:attribute:: fetch_attribute

        Signal emited when a non-existent attribute is being accessed before
        AttributeError is raised. If any slot returns a non-None value, then
        this value will be used to set the attribute and AttributeError won't
        be raised.

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
    def __getattr__(self, name):
        if name not in self.__dict__:
            result = self.fetch_attribute.emit(obj=self, name=name)

            if result is not None:
                setattr(self, name, result)
            else:
                raise AttributeError

        return getattr(self, name)

    @classmethod
    def get_fetch_attribute(cls):
        """
        Using a property descriptor, we ensure that each DynamicState subclass
        has its own signal.

        >>> class YourObject(DynamicState):
        ...     pass
        ...
        >>> class YourData(DynamicState):
        ...     pass
        ...
        >>> def fetch_yourobject_foo(obj, name, **kwargs):
        ...     if name != 'foo':
        ...         return  # not my responsability
        ...     return 'yourobject foo'
        ...
        >>> def fetch_yourobject_data(obj, name, **kwargs):
        ...     if name != 'data':
        ...         return  # not my responsability
        ...     return YourData()
        ...
        >>> def fetch_yourdata_foo(obj, name, **kwargs):
        ...     if name != 'foo':
        ...         return  # not my responsability
        ...     return 'yourdata foo'
        ...
        >>> YourObject.fetch_attribute.connect(fetch_yourobject_foo)
        >>> YourObject.fetch_attribute.connect(fetch_yourobject_data)
        >>> YourData.fetch_attribute.connect(fetch_yourdata_foo)
        >>> your_object = YourObject()
        >>> assert your_object.foo == 'yourobject foo'
        >>> assert your_object.data.foo == 'yourdata foo'
        """
        fetch_attribute = getattr(cls, '_fetch_attribute', None)

        if fetch_attribute is None:
            cls._fetch_attribute = Signal(args=['obj', 'name'])

        return cls._fetch_attribute

    @classmethod
    def set_fetch_attribute(cls, value):
        cls._fetch_attribute = value

    fetch_attribute = DynamicStateSignalDescriptor(get_fetch_attribute,
                                                   set_fetch_attribute)
