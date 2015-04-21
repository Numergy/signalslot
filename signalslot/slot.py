"""
Module defining the Slot class.
"""

import types
import weakref
import sys

if sys.version_info < (3, 4):
    from weakrefmethod import WeakMethod
else:
    from weakref import WeakMethod


class Slot(object):
    """
    A slot is a callable object that manages a connection to a signal.
    If weak is true or the slot is a subclass of weakref.ref, the slot
    is automatically de-referenced to the called function.
    """
    def __init__(self, slot, weak=False):
        self._weak = weak or isinstance(slot, weakref.ref)
        if weak and not isinstance(slot, weakref.ref):
            if isinstance(slot, types.MethodType):
                slot = WeakMethod(slot)
            else:
                slot = weakref.ref(slot)
        self._slot = slot

    @property
    def is_alive(self):
        """
        Return True if this slot is "alive".
        """
        return (not self._weak) or (self._slot() is not None)

    @property
    def func(self):
        """
        Return the function that is called by this slot.
        """
        if self._weak:
            return self._slot()
        else:
            return self._slot

    def __call__(self, **kwargs):
        """
        Execute this slot.
        """
        func = self.func
        if func is not None:
            return func(**kwargs)

    def __eq__(self, other):
        """
        Compare this slot to another.
        """
        return self.func == other.func

    def __repr__(self):
        return '<signalslot.Slot: %s>' % (self.func or 'dead')
