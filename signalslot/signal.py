from . import exceptions


class Signal(object):
    def __init__(self):
        self.slots = []

    def connect(self, slot):
        """ Connect a slot to this signal. """
        if self.connected(slot):
            raise exceptions.AlreadyConnected()

        self.slots.append(slot)

    def connected(self, slot):
        """ Returns True if slot is connected, False otherwise.  """
        return slot in self.slots

    def emit(self):
        """ Call all slots connected to this signal. """
        for slot in self.slots:
            slot()
