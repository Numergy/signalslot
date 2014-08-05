import pytest
import mock

from signalslot import Signal, SlotMustAcceptKeywords


@mock.patch('signalslot.signal.inspect')
class TestSignal(object):
    def setup_method(self, method):
        self.signal_a = Signal()
        self.signal_b = Signal(args=['foo'])

        self.slot_a = mock.Mock(spec=lambda **kwargs: None)
        self.slot_a.return_value = None
        self.slot_b = mock.Mock(spec=lambda **kwargs: None)
        self.slot_b.return_value = None

    def test_is_connected(self, inspect):
        self.signal_a.connect(self.slot_a)

        assert self.signal_a.is_connected(self.slot_a)
        assert not self.signal_a.is_connected(self.slot_b)
        assert not self.signal_b.is_connected(self.slot_a)
        assert not self.signal_b.is_connected(self.slot_b)

    def test_emit_one_slot(self, inspect):
        self.signal_a.connect(self.slot_a)

        self.signal_a.emit()

        self.slot_a.assert_called_once_with()
        assert self.slot_b.call_count == 0

    def test_emit_two_slots(self, inspect):
        self.signal_a.connect(self.slot_a)
        self.signal_a.connect(self.slot_b)

        self.signal_a.emit()

        self.slot_a.assert_called_once_with()
        self.slot_b.assert_called_once_with()

    def test_emit_one_slot_with_arguments(self, inspect):
        self.signal_b.connect(self.slot_a)

        self.signal_b.emit(foo='bar')

        self.slot_a.assert_called_once_with(foo='bar')
        assert self.slot_b.call_count == 0

    def test_emit_two_slots_with_arguments(self, inspect):
        self.signal_b.connect(self.slot_a)
        self.signal_b.connect(self.slot_b)

        self.signal_b.emit(foo='bar')

        self.slot_a.assert_called_once_with(foo='bar')
        self.slot_b.assert_called_once_with(foo='bar')

    def test_reconnect_does_not_duplicate(self, inspect):
        self.signal_a.connect(self.slot_a)
        self.signal_a.connect(self.slot_a)
        self.signal_a.emit()

        self.slot_a.assert_called_once_with()

    def test_disconnect_does_not_fail_on_not_connected_slot(self, inspect):
        self.signal_a.disconnect(self.slot_b)


def test_anonymous_signal_has_nice_repr():
    signal = Signal()
    assert repr(signal) == '<signalslot.Signal: NO_NAME>'


def test_named_signal_has_a_nice_repr():
    signal = Signal(name='update_stuff')
    assert repr(signal) == '<signalslot.Signal: update_stuff>'


class TestSignalConnect(object):
    def setup_method(self, method):
        self.signal = Signal()

    def test_connect_with_kwargs(self):
        def cb(**kwargs):
            pass

        self.signal.connect(cb)

    def test_connect_without_kwargs(self):
        def cb():
            pass

        with pytest.raises(SlotMustAcceptKeywords):
            self.signal.connect(cb)
