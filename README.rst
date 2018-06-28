===========
SimpleEvent
===========
-----------------------------------------
A simple python event notification system
-----------------------------------------

.. image:: https://travis-ci.org/kampka/python-simpleevent.svg?branch=master
    :target: https://travis-ci.org/kampka/python-simpleevent

This module provides a simple event notification system.
An object that wishes to be notified about an event can register a callback function
with the `EventManager`. Whenever an `Event` is emitted though that
`EventManager`, the object will be notified by calling the registered callback
methods for all callbacks registered for that event.

Example::
	>>> em = EventManager()

	>>> def receiver(notification):
	...	print notification

	>>> em.registerHandler("notify", receiver)

	>>> result = em.emit(Event("notify", "Hello event notification"))
	Hello event notification
