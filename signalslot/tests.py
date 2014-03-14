import mock
import unittest

import signalslot


class NoArgumentsSignalTestCase(unittest.TestCase):
    def setUp(self):
        self.slot = mock.MagicMock()
        self.signal = signalslot.Signal()

    def test_not_connected(self):
        self.assertFalse(self.signal.connected(self.slot))

    def test_connected(self):
        self.signal.connect(self.slot)

        self.assertTrue(self.signal.connected(self.slot))

    def test_cannot_reconnect(self):
        self.signal.connect(self.slot)

        with self.assertRaises(signalslot.AlreadyConnected):
            self.signal.connect(self.slot)

    def test_emit(self):
        self.signal.connect(self.slot)

        self.signal.emit()

        self.slot.assert_called_once_with()


class SignalIsCompatibleTestCases(unittest.TestCase):
    def test_with_one_argument(self):
        signal = signalslot.Signal(args=['firewall'])

        def test_slot(firewall):
            pass

        self.assertTrue(signal.is_compatible(test_slot))

    def test_with_one_argument_with_keyword(self):
        signal = signalslot.Signal(args=['firewall'])

        def test_slot(firewall=None):
            pass

        self.assertTrue(signal.is_compatible(test_slot))

    def test_with_asterisk_args(self):
        signal = signalslot.Signal(args=['firewall'])

        def test_slot(*args):
            pass

        self.assertFalse(signal.is_compatible(test_slot))

    def test_with_asterisk_args(self):
        signal = signalslot.Signal(args=['firewall'])

        def test_slot(**kwargs):
            pass

        self.assertFalse(signal.is_compatible(test_slot))

    def test_connect_wrong_slot_signature(self):
        signal = signalslot.Signal(args=['firewall'])

        def test_slot():
            pass

        self.assertFalse(signal.is_compatible(test_slot))
