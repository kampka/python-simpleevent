
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

import random
import unittest
from SimpleEvent import *

class SimpleEventTestCase(unittest.TestCase):

	class _EventMock(object):
		def __init__(self):
			self.value = None
			self.message = "Event mock was not altered by any event handler."

	def setUp(self):
		self.em = EventManager(50)

	def test_emit(self):

		notification = random.random()

		def handler(n):
			self.assertEqual(notification, n, "Expected notification to be %s but got %s instead." % (notification, n,))

		self.em.registerHandler("notify", handler)

		result = self.em.emit(Event(notification))

		self.assertTrue(result.success(), "Event chain reported an error during execution that cannot have occurred.")
		self.assertFalse(result.failure(), "Event chain reported a failure that did not happen.")

	def test_emitUntil(self):

		def callableHandler(m):
			m.value = True
			m.message = ""
			return True

		def uncallableHandler(m):
			m.value = False
			m.message = "Result object was passed to uncallable handler"

		self.em.registerHandler("notify", callableHandler, 10)
		self.em.registerHandler("notify", uncallableHandler, 20)

		m = self._EventMock()
		self.em.emitUntil(Event("notify", m))

		self.assertTrue(m.value, m.message)

	def test_emitHaltOnError(self):
		m = self._EventMock()

		def handlerWithError(m):
			e = UserWarning("Notification handler raised an error.")
			m.value = e
			m.message = str(e)
			raise e

		def handle(m):

			m.value = False
			m.message = "Event should not have reached this handler"
			self.fail(m.message)

		self.em.registerHandler("notify", handlerWithError, 10)
		self.em.registerHandler("notify", handle, 20)

		result = self.em.emit(HaltingEvent("notify", m))

		self.assertEqual(m.value, result.exception, "Expected captured exception to be %s, but got %s" % (m.value, result.exception))
		self.assertEqual(m.message, result.message, "Expected result message to to be %s, but got %s" % (m.message, str(result.exception)))
		self.assertTrue(result.failure(), "Expected result to be marked as a failure, but it isn't")
		self.assertFalse(result.success(), "Did not expect result to be marked as a success, but it is")
		self.assertNotEqual(result.traceback, None, "Expected result to capture a traceback, but it does not have one")

	def test_priotityRanges(self):
		self.assertRaises(AssertionError, EventManager, -1)
		self.assertRaises(AssertionError, self.em.registerHandler, "notify", lambda x: None, 60)
		try:
			self.em.registerHandler("notify", lambda x: None, 50)
		except AssertionError as e:
			self.fail("Handler is in acceptable parameters but it is being rejected.")


	def tearDown(self):
		self.em = None
