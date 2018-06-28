
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

from setuptools import setup, find_packages

setup(
	name='python-simpleevent',
	version='1.2',
	license='GPL-2',
	url='https://github.com/kampka/python-simpleevent',
	description='A simple python event notification system',
	long_description="A simple python event notification system \
		python-simpleevent lets you register multiple event handlers \
		to an event that will be invoked if an event occurs.",
	packages=find_packages(exclude=["tests", ".git"]),
	test_suite="tests.testsuite"
)
