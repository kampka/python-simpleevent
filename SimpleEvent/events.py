
# SimpleEvent - A simple python event notification system
# Copyright (C) 2010  Christian Kampka
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

"""
This module provides a simple event notification system.
An object that wishes to be notified about an event can register a callback function
with the :class:`EventManager`. Whenever an :class:`Event` is emitted though that
:class:`EventManager`, the object will be notified by calling the registered callback
methods for all callbacks registered for that event.

Example::
	
	>>> em = EventManager()
	
	>>> def receiver(notififcation):
	...	print notification
	
	>>> em.registerHandler("notify", receiver)
	
	>>> em.emit(Event("notify", "Hello event notification"))
	"Hello event notification"
"""

import sys

class EventManager(object):
	"""
	The basic event manager that handles (de-)registering of event handlers (callbacks)
	and dispatching of event.
	Usually, only a single instance of this class exists throughout a program.
	"""
	
	def __init__(self, maxPriority=100):
		"""
		Create a new EventManager

		:param maxPriority: The maximum priotiry range an event can be registered in.
		:type maxPriority: int.
		"""
		
		assert maxPriority > 0

		self._maxPriority = maxPriority
		self._handlers = {}
		
	def registerHandler(self, event, handler, priority=50):
		"""
		Register a function as a callback for an event to be called when an event is emitted.
		
		:param event: The event identifier to register the handler with.
		:type event: str.
		
		:param handler: The handler to call when the event occurs.
			This must be a callable function.
		:type handler: function.
		:param priorirty: Specifies the priority of this handler.
			Handlers are called in ascending order of their priority.
			Valid values are between 0 and 100, the default if 50.

		:type priority: int.
		:returns: :class:`EventResult` - An object representing the result of the event dispatch.
		"""
		assert priority >= 0
		assert priority <= self._maxPriority
		
		if not self._handlers.has_key(event):
			self._handlers[event] = {}
		
		if not self._handlers[event].has_key(priority):
			self._handlers[event][priority] = []

		if not handler in self._handlers[event][priority]:
			self._handlers[event][priority].append(handler)


	def deregisterHandler(self, event, handler):
		"""
		Deregister a function from an event that is allready registered as a handler.
		
		:param event: The event to deregiester the handler from.
		:type event: str.
		
		:param handler: The handler function to deregister from the event.
		:type handler: function.
		
		"""
		if self._handlers.has_key(event):
			for priority in self._handlers[event].keys():
				if handler in self._handlers[event][priority]:
					self._handlers[event][priority].remove(handler)

	def emit(self, event):
		"""
		Emits an event to all handlers registered with the event name.

		:param event: The event to emit to the handlers regiestered for it.
		:type event: :class:`Event`
		
		:returns: :class:`EventResult` - If an :class:`Exception` occurred while calling a handler, the :class:`EventResult` will encapsulate
		  that exception. Notification emitter which rely onto weather the event was successfully dispatched should check this object for success/failure.
		"""
		result = EventResult()
		if self._handlers.has_key(event.name):
			for key, handlers in sorted(self._handlers[event.name].items()):
				for handler in handlers:
					try:
						handler(*event.args, **event.kwargs)
					except:
						result.fail()
						if getattr(event, "haltOnError", False):
							return result
						
		return result

	def emitUntil(self, event):
		"""
		Emits an event to all handlers registered with the event name until True is returned by one of the handlers.
		Once a handler returns True, the rest of the handlers will be ignored and :meth:`emitUntil` will return the result
		that it got so far.
		
		:param event: The event to emit to the handlers regiestered for it.
		:type event: :class:`Event`
		
		:returns: :class:`EventResult` - If an :class:`Exception` occurred while calling a handler, the :class:`EventResult` will encapsulate
		  that exception. Notification emitter which rely onto weather the event was successfully dispatched should check this object for success/failure.
		"""
		result = EventResult()
		if self._handlers.has_key(event.name):
			for key, handlers in sorted(self._handlers[event.name].items()):
				for handler in handlers:
					try:
						r = handler(*event.args, **event.kwargs)
						if r:
							return result
					except:
						result.fail()
						if getattr(event, "haltOnError", False):
							return result
		return result

class NonErrorEventException(BaseException):
	pass

class EventResult(object):
	"""
	This Class represents a result from an emitted event.
	If the :class:`EventManager` encounters an :class:`Exception` while dispatching an event,
	this class will encapsulate that exception. Otherwise, this class will represent a successful
	notification.
	"""
	def __init__(self):
		self.result = True
		self.type = None
		self.exception = None
		self.traceback  = None
		self.fail()

	def success(self):
		"""
		Returns True if this represents a successful notification, or False otherwise.
		"""
		return self.result
	
	def failure(self):
		"""
		Returns True if this represents a unsuccessful notification, or False otherwise. 
		"""
		return not self.result

	def fail(self):
		"""
		Mark this :class:`EventResult` as failed, despite of any actually occurring errors.
		"""
		self.maybeFail()
		
		if not self.exception:
			self.exception = NonErrorEventException("Marked as failed without an actual exception present.")
			self.message = str(self.exception)
		self.result = False

	def maybeFail(self):
		"""
		In case of an occurring Exception, calling :meth:`maybeFail` on an EventResult object will
		encapsulate that Exception into the EventResult, thus marking it as a failure.
		If no Exception occurred, calling this function will have no effect.
		"""
		self.type, self.exception, self.traceback = sys.exc_info()
		
		if self.traceback is not None:
			sys.exc_clear()
			self.result = False
			self.message = str(self.exception)

	def __eq__(self, other):
		return self.success() == bool(other)
	
	def __nonzero__(self):
		return self.success()

class Event(object):
	"""
	This class represents an event that can be emitted through the EventManager.
	Any additional *args and **kwargs will be passed to the handler callback respectively.
	"""
	def __init__(self, name, *args, **kwargs):
		"""
		:param name: The name of the event this object represents. It specifies which handlers to be called by the :class:EventManager.
		:type name: str.
		"""
		self.name = name
		self.args = args
		self.kwargs = kwargs

class HaltingEvent(Event):

	def __init__(self, name, *args, **kwargs):
		"""
		:param haltOnError: If ``haltOnError`` is set to True, the :class:`EventManager` will stop
		  to call any following handlers if one handler throws an exception and instead return a failed :class:`EventResult`.
		  If not, it will continue, to call all handlers remaining handlers and return only the latest failure if one occurred.
		  Normaly, registered handler should not raise Exceptions up to the EventManager.
		:type haltOnError: bool.
		"""	
		Event.__init__(self, name, *args, **kwargs)
		self.haltOnError = True



__all__ = ["EventManager", "Event", "HaltingEvent"]
