class SignalSlotException(Exception):
    """ Base class for all exceptions of this module. """
    pass


class AlreadyConnected(SignalSlotException):
    """
    Raised when attempting to connect a slot to a signal which is already
    connected to that slot.
    """
    pass
