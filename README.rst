===========
SimpleEvent
===========
-----------------------------------------
A simple python event notification system
-----------------------------------------

This module provides a simple event notification system.
An object that wishes to be notified about an event can register a callback function
with the `EventManager`. Whenever an `Event` is emitted though that
`EventManager`, the object will be notified by calling the registered callback
methods for all callbacks registered for that event.

Example::
	>>> from SimpleEvent import *
	>>> em = EventManager()
	
	>>> def receiver(notififcation):
	...	print notification
	
	>>> em.registerHandler("notify", receiver)
	
	>>> em.emit(Event("notify", "Hello event notification"))
	"Hello event notification"
