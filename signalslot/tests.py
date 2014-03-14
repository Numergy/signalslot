import mock
import unittest

import signalslot


class SignalSlotTestCase(unittest.TestCase):
    def setUp(self):
        self.slot = mock.MagicMock()
        self.signal = signalslot.Signal()

    def test_not_connected(self):
        self.assertFalse(self.signal.connected(self.slot))

    def test_connected(self):
        self.signal.connect(self.slot)

        self.assertTrue(self.signal.connected(self.slot))
