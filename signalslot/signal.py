from . import exceptions


class Signal(object):
    def __init__(self, args=None):
        self.slots = []
        self.args = args or []

    def connect(self, slot):
        """ Connect a slot to this signal. """
        if self.connected(slot):
            raise exceptions.AlreadyConnected()

        if not self.is_compatible(slot):
            raise exceptions.IncompatibleSlotSignature()

        self.slots.append(slot)

    def connected(self, slot):
        """ Returns True if slot is connected, False otherwise.  """
        return slot in self.slots

    def disconnect(self, slot):
        """ Disconnect a slot from a signal. """
        self.slots.pop(self.slots.index(slot))

    def emit(self, *args, **kwargs):
        """ Call all slots connected to this signal. """
        for slot in self.slots:
            slot(*args, **kwargs)

    def is_compatible(self, slot):
        """ Return True if slot is compatible with args of this signal. """
        args = slot.func_code.co_varnames[:slot.func_code.co_argcount]
        return list(args) == list(self.args)
