class Signal(object):
    def __init__(self):
        self.slots = []

    def connect(self, slot):
        """ Connect a slot to this signal. """
        self.slots.append(slot)

    def connected(self, slot):
        """ Returns True if slot is connected, False otherwise.  """
        return slot in self.slots
