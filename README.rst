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

Rationale against Signal/Slot is detailed in the "Pattern"
section of the documentation.

Install
-------

Install latest stable version::

    pip install signalslot

Install development version::

    pip install -e git+https://github.com/Numergy/signalslot

Upgrade
-------

Upgrade to the last stable version::

    pip install -U signalslot

Uninstall
---------

::

    pip uninstall signalslot
