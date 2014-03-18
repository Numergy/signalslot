.. image:: https://secure.travis-ci.org/Numergy/signalslot.png?branch=master
    :target: http://travis-ci.org/Numergy/signalslot
.. image:: https://pypip.in/d/signalslot/badge.png
    :target: https://crate.io/packages/signalslot
.. image:: https://pypip.in/v/signalslot/badge.png   
    :target: https://crate.io/packages/signalslot
.. image:: https://coveralls.io/repos/Numergy/signalslot/badge.png 
    :target: https://coveralls.io/r/Numergy/signalslot

signalslot: simple Signal/Slot implementation for Python
========================================================

This package provides a simple and stupid implementation of the `Signal/Slot
pattern <http://en.wikipedia.org/wiki/Signals_and_slots>`_ for Python.
Wikipedia has a nice introduction:

    Signals and slots is a language construct introduced in Qt for
    communication between objects[1] which makes it easy to implement the
    Observer pattern while avoiding boilerplate code. 

Why signalslot ?
----------------

Signal/Slot is a pattern that allows loose coupling various components of a
software without having to introduce boilerplate code. Loose coupling of
components allows better modularity in software code which has the nice side
effect of making it easier to test because less dependencies means less mocking
and monkey patching.

Signal/Slot is a widely used pattern, many frameworks have it built-in
including Django, Qt and probably many others. If you have a standalone project
then you probably don't want to add a big dependency like PyQt or Django just
for a Signal/Slot framework. There are a couple of standalone libraries which
allow to acheive a similar result, like Circuits or PyPubSub,  which has way
more features than ``signalslots``, like messaging over the network and is a
quite complicated and has weird (non-PyPi hosted) dependencies and is not PEP8
compliant ...

``signalslot`` has the vocation of being a light and simple implementation of
the well known Signal/Slot design pattern provided as a classic quality Python
package.

Install
-------

Install latest stable version::

    pip install signalslot

Install development version::

    pip install -e git+https://github.com/Numergy/signalslot

Usage
-----

Tight coupling
``````````````

Consider such a code in ``your_client.py``:

.. code-block:: python

    import your_service
    import your_plugin

    class YourClient(object):
        def something_happens(self, some_argument):
            your_service.something_happens(some_argument)
            your_plugin.something_happens(some_argument)

The problem with that code is that it ties ``your_client`` with
``your_service`` and ``your_plugin``, which makes it harder to test and
maintain.

An improvement would be to acheive the same while keeping components loosely
coupled.

Observer pattern
````````````````

You could implement an Observer pattern in ``YourClient`` by adding
boilerplate code:

.. code-block:: python

    class YourClient(object):
        def __init__(self):
            self.observers = []

        def register_observer(self, observer):
            self.observers.append(observer)

        def something_happens(self, context, router):
            for observer in self.observers:
                observer.something_happens(context, router)

This implementation is a bit dumb, it doesn't check the compatibility of
observers for example, also it's additionnal code you'd have to test.

And, this would work if you have control on instanciation of
``YourClient``, ie.:

.. code-block:: python

    your_client = YourClient()
    your_client.register_observer(your_service)
    your_client.register_observer(your_plugin)

If ``YourClient`` is used by a framework with IoC (Inversion of Control)
then it's a lot harder. Example:

.. code-block:: python

    client = some_framework.Service.create(
        client='your_client')

As you can see in the above example, it's a lot harder to get your hands on the
``YourClient`` instance and call ``register_observer``.

Using signalslot
````````````````

Consider such a signal definition in ``your_client/signals.py``

.. code-block:: python

    import signalslot

    something_happens = signalslot.Signal(args=['some_argument'])

You can then connect slots to this signal in each loosely coupled module.
``your_service/slots.py`` and ``your_plugin/slots.py`` would contain something
like:

.. code-block:: python

    from your_client.signals import something_happens

    def something_happens(context, router):
        # ....

    something_happens.connect(something_happens)

Then, ``your_service.something_happens`` and ``your_plugin.something_happens``
would be called every time the ``something_happens`` signal is emited, ie.:

.. code-block:: python

    from . import signals

    class YourClient(object):
        def something_happens(self, some_argument):
            signals.something_happens.emit(some_argument)

All you have to do is import ``your_client`` and ``your_plugin`` somewhere
before ``YourClient`` to ensure that the ``connect()`` calls are executed, ie.:

.. code-block:: python

    from your_service import slots
    from your_plugin import slots

    client = some_framework.Service.create(
        client='your_client')
