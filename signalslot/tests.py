import mock
import unittest

import signalslot


@mock.patch.object(signalslot.Signal, 'is_compatible')
class NoArgumentsSignalTestCase(unittest.TestCase):
    def setUp(self):
        self.slot = mock.MagicMock()
        self.signal = signalslot.Signal()

    def test_not_connected(self, is_compatible):
        self.assertFalse(self.signal.connected(self.slot))

    def test_connected(self, is_compatible):
        self.signal.connect(self.slot)

        self.assertTrue(self.signal.connected(self.slot))

    def test_emit(self, is_compatible):
        self.signal.connect(self.slot)

        self.signal.emit()

        self.slot.assert_called_once_with()

    def test_several_slots(self, is_compatible):
        self.signal.connect(self.slot)
        slot_b = mock.MagicMock()
        self.signal.connect(slot_b)

        self.signal.emit()

        self.slot.assert_called_once_with()
        slot_b.assert_called_once_with()

    def test_disconnect(self, is_compatible):
        self.signal.connect(self.slot)
        self.signal.disconnect(self.slot)

        self.signal.emit()

        self.assertEqual(self.slot.call_count, 0)

    def test_is_connected(self, is_compatible):
        self.assertFalse(self.signal.is_connected(self.slot))

        self.signal.connect(self.slot)

        self.assertTrue(self.signal.is_connected(self.slot))

    def test_disconnect_raises_notconnected(self, is_compatible):
        def foo():
            pass

        with self.assertRaises(signalslot.NotConnected):
            self.signal.disconnect(foo)

    def test_connect(self, is_compatible):
        self.signal.connect(self.slot)
        self.assertTrue(self.signal.is_connected(self.slot))

        self.signal.connect(self.slot)
        self.assertTrue(self.signal.is_connected(self.slot))

        self.assertEqual(len(self.signal.slots), 1)


class SignalIsCompatibleTestCases(unittest.TestCase):
    def setUp(self):
        self.signal = signalslot.Signal(args=['firewall'])

    def test_connect_incompatible_slot_raises_exception(self):
        def foo(bar):
            pass

        with self.assertRaises(signalslot.IncompatibleSlotSignature):
            self.signal.connect(foo)

    def test_with_one_argument(self):
        def test_slot(firewall):
            pass

        self.assertTrue(self.signal.is_compatible(test_slot))

    def test_with_too_many_argument(self):
        def test_slot(firewall, bar):
            pass

        self.assertFalse(self.signal.is_compatible(test_slot))

    def test_with_one_argument_with_keyword(self):
        def test_slot(firewall=None):
            pass

        self.assertTrue(self.signal.is_compatible(test_slot))

    def test_with_asterisk_args(self):
        def test_slot(*args):
            pass

        self.assertFalse(self.signal.is_compatible(test_slot))

    def test_with_asterisk_kwargs(self):
        def test_slot(**kwargs):
            pass

        self.assertFalse(self.signal.is_compatible(test_slot))

    def test_connect_wrong_slot_signature(self):
        def test_slot():
            pass

        self.assertFalse(self.signal.is_compatible(test_slot))

    def test_connect_wrong_slot_signature_with_local(self):
        def test_slot():
            firewall = None

        self.assertFalse(self.signal.is_compatible(test_slot))


@mock.patch.object(signalslot.Signal, 'is_compatible')
class ArgumentedSignalTestCase(unittest.TestCase):
    def test_emit_with_arguments(self, is_compatible):
        is_compatible.return_value = True

        signal = signalslot.Signal(args=['firewall'])
        slot = mock.MagicMock()
        signal.connect(slot)
        signal.emit(firewall='foo')
        slot.assert_called_once_with(firewall='foo')
