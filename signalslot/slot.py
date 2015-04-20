"""
Module defining the Slot class.
"""

import sys
if sys.version_info < (3,4):
    from weakrefmethod import WeakMethod
else:
    from weakref import WeakMethod

import weakref
import types

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

    def is_alive(self):
        """
        Return True if this slot is "alive".
        """
        return (not self.weak) or (self._slot() is not None)
    
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

try:
    # Support for Tornado IOLoop slots
    import tornado
    class TornadoSlot(Slot):
        """
        A TornadoSlot is a Slot subclass that allows for calling a method
        from across IOLoop instances.
        """

        def __init__(self, slot, weak=False, io_loop=None, blocking=False):
            """
            Initialise a TornadoSlot instance.  The connection can take two
            forms:

            - Non-blocking slots cannot influence the calling signal, whereas
              a normal 'signalslot' slot can return a value to the caller by
              returning a value other than None, a non-blocking slot is ALWAYS
              assumed to return None.
            - Blocking slots either pause execution in the current thread while
              waiting for a response from the target IOLoop, or if the slot
              IOLoop is the current IOLoop, the function is called directly.
            """
            super(TornadoSlot, self).__init__(slot, weak)
            self._io_loop   = io_loop
            self._blocking  = blocking

        def __call__(self, **kwargs):
            func = self.func
            if func is None:
                return

            if self._blocking:
                if self._io_loop is tornado.ioloop.IOLoop.current():
                    # Direct call
                    return func(**kwargs)
                else:
                    class PoorMansFuture(object):
                        def __init__(self, func):
                            self.func       = func
                            self.event      = threading.Event()
                            self.value      = None
                            self.exc_info   = None
                        def run(self, **kwargs):
                            try:
                                self.value      = self.func(**kwargs)
                            except:
                                self.exc_info   = sys.exc_info()
                            self.event.set()
                        def spawn(self, io_loop):
                            io_loop.add_callback(self.run, **kwargs)
                            self.event.wait()
                            if self.exc_info is not None:
                                raise self.exc_info
                            else:
                                return self.value

                    pmf = PoorMansFuture(func)
                    return pmf.spawn(**kwargs)
            else:
                self._io_loop.add_callback(func, **kwargs)
            return None
except ImportError:
    pass
