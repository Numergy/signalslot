class SignalSlotException(Exception):
    """ Base class for all exceptions of this module. """
    pass


class AlreadyConnected(SignalSlotException):
    """
    Raised when attempting to connect a slot to a signal which is already
    connected to that slot.
    """
    pass


class IncompatibleSlotSignature(SignalSlotException):
    """
    Raised when attempting to connect a slot with a signature that is not
    compatible with the Signal's signature (args).
    """
    pass


class NotConnected(SignalSlotException):
    """
    Raised when attempting to disconnect a signal that is not connected.
    """
    pass
