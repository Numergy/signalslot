class SignalSlotException(Exception):
    """Base class for all exceptions of this module."""
    pass


class SlotMustAcceptKeywords(SignalSlotException):
    """
    Raised when connecting a slot that does not accept ``**kwargs`` in its
    signature.
    """
    def __init__(self, signal, slot):
        m = 'Cannot connect %s to %s because it does not accept **kwargs' % (
            slot, signal)

        super(SlotMustAcceptKeywords, self).__init__(m)
