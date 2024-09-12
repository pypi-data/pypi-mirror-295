#-== @h1
# Blessed Window Kit Screen Tools (bwk.screen)
#
#-== An extension of the Blessed Window Kit (BWK) for quickly
# building Text-Based User Interface (TUI) applications.
#
#-== - Use in your project by importing the module:
#		-- /-import bwk.screen-/

import traceback

from blessed import Terminal

from .bwk import Window, Border, echo, flush
from .characters import DotDict

#-==@class
class Screen:
	#-== A barebones implementation for rendering
	# output to a terminal and processing input.
	# This can be used with or without the BWK itself
	# (see the /ScreenManager classes below).
	#
	#-== @attributes
	#	man:		a /ScreenManager which the sceen is associated to.
	#	name:		the name of the screen
	#	commands: 	a dictionary of commands.
	#					Each value is a function which will execute when
	#					input matching its key is received by the screen.

	#-==@method
	def __init__(self, manager, name, commands={}):
		#-== @params
		#	man:		a /ScreenManager which the sceen is associated to.
		#	name:		the name of the screen
		#	commands: 	a dictionary of commands.
		#					Each value is a function which will execute when
		#					input matching its key is received by the screen.
		#
		# After setting the /man, /name, and /commands , this method calls the
		# /set_commands() method to modify the provided /commands (if any) and
		# add any new commands.

		self.man = manager
		self.name = name
		self.commands = commands
		self.set_commands()

	#-==@method
	def set_commands(self):
		#-== Use this method to append commands to the screen.
		# When the /process_input() method is called, it checks if the input
		# matches any keys in /self.commands . If there is a matching key,
		# the screen will execute the function stored by that key.
		# Typically this method is used to add methods of the class itself
		# ( /self.method_name() ), as they cannot be accessed easily
		# from outside the class.
		# Therefore, the typical structure of this method
		# looks like the example below.
		#
		#-== *Example:*
		# @codeblock
		# def set_commands(self):
		#//  self.commands['d'] = self.method_one
		#//  self.commands['x'] = self.method_two
		#//  self.commands['3'] = self.method_three
		# @codeblockend

		pass

	#-==@method
	def pre_process_input(self, userin):
		#-== @params
		#	userin:	the input received to the screen
		#
		#-== This method executes after a screen receives input,
		# but before a matching command is executed.

		pass

	#-==@method
	def post_process_input(self, userin):
		#-== @params
		#	userin:	the input received to the screen
		#
		#-== This method executes after the input has been processed
		# by the screen (which may be a command, or an error).

		pass

	#-==@method
	def process_input(self, userin):
		#-== @params
		#	userin:	the input received to the screen
		#
		#-== This is the main method which handles input to the screen.
		# It executes the following steps in order:
		# * /self.pre_process_input(userin)
		# * if /userin matches a key in /self.commands,
		#		executes the corresponding function
		# * if /userin does not match a key in /self.commands,
		#		executes /self.process_input_error(userin)
		# * /self.post_process_input(userin)

		self.pre_process_input(userin)
		try:
			self.commands[userin]()
		except KeyError:
			self.process_input_error(userin)
		self.post_process_input(userin)

	#-==@method
	def process_input_error(self, userin):
		#-== @params
		#	userin:	the input received to the screen
		#
		#-== This method executes when an input does not match
		# any key in /self.commands .

		pass

	#-==@method
	def render(self):
		#-== This method will render the screen content to the terminal.

		print('ERROR: No screen render implemented')


#-==@class
class GenericScreenManager:
	#-== A barebones implementation for running
	# an application loop with /Screen objects.
	#
	#-== @attributes
	#	running:		a boolean indicating if the run loop should continue
	#	curr_screen:	the current /Screen object being used
	#						to render output and process input

	#-==@method
	def __init__(self):
		#-== Initializes the manager.

		self.running = False
		self.curr_screen = None

	#-==@method
	def pre_run(self):
		#-== This method executes before the run loop begins.
		# Any necessary preparation before the application starts
		# should be done here.

		assert self.curr_screen, 'No current screen assigned'

	#-==@method
	def post_run(self):
		#-== This method executes after the run loop ends.
		# Any necessary cleanup after the application has ended
		# should be done here.

		pass

	#-==@method
	def run(self):
		#-== This is the main entrypoint for the /ScreenManager .
		# Execute this method to begin the application loop,
		# including the /pre_run() and /post_run() methods.

		self.pre_run()
		self._run()
		self.post_run()

	def _run(self):
		# This is a private method to separate the run loop
		# from the pre and post steps.
		self.running = True
		try:
			self.run_loop()
		except Exception as exc:
			self.handle_crash(exc)

	#-==@method
	def run_loop(self):
		#-== The actual implementation of the application loop.
		# It executes the follwoing setps in order:
		# * /self.render()
		# * /self.get_user_input()
		# * /self.process_input(userin)
		#
		#-== The above steps will continue to execute until
		# /self.running is False or there is no /self.curr_screen set
		# (meaning that there is no way to display output or process input).

		while self.running and self.curr_screen:
			self.render()
			userin = self.get_user_input()
			self.process_input(userin)

	#-==@method
	def render(self):
		#-== Renders output to the terminal.
		# This is typically done via /self.curr_screen.render() .

		self.curr_screen.render()

	#-==@method
	def get_user_input(self):
		#-== Gets input from the user.
		# This can be overriden for specific input types.
		# By default, it uses Python's /input() method.

		return input()

	#-==@method
	def process_input(self, userin):
		#-== @params
		#	userin:	the input received from the user
		#
		#-== Processes the input received from the user.
		# This is typically done via /self.curr_screen.process_input(userin) .

		self.curr_screen.process_input(userin)

	#-==@method
	def quit(self):
		#-== A convenience method for ending the application loop.
		# By default, this simply sets /self.running to False.

		self.running = False

	def handle_crash(self, exc):
		#-== @params
		#	exc:	the /Exception raised during the application loop
		#
		#-== In the event that an exception is not caught
		# during the application loop, the manager will
		# gracefully catch the exception and handle it here.
		# After this method executes, the /post_run() method
		# executes, to ensure that all necessary cleanup is still
		# performed despite the program crashing.
		
		traceback.print_exc()


#-==@class
class BwkScreenManager(GenericScreenManager):
	#-== A screen manager for running specifically for handling
	# screens which utilize the Blessed Window Kit for rendering.
	#
	#-== @attributes
	#	running:		a boolean indicating if the run loop should continue
	#	curr_screen:	the current /Screen object being used
	#						to render output and process input
	#	term:			the /blessed.Terminal object used to render screens

	#-==@method
	def __init__(self, term=None):
		#-== @params
		#	term:	the /blessed.Terminal object used to render screens
		#
		#-== Initializes the screen manager. If no /term is provided,
		# a default /Terminal() is used.

		super().__init__()
		self.term = term
		if self.term is None:
			self.term = Terminal()

	#-==@method
	# def run(self):
	#-== Overrides the original /run() with special context managers for BWK:
	# * /term.fullscreen
	# * /term.cbreak
	# * /term.hidden_cursor
	#
	#-== This ensures that the application behaves similarly to the /window_shopper()
	# method provided by the BWK to simplify building and managing screens.

	def _run(self):
		with self.term.fullscreen(), self.term.cbreak(), self.term.hidden_cursor():
			self.running = True
			self.run_loop()

	#-==@method
	def get_user_input(self):
		#-== Overrides this method to use the /self.term.inkey()
		# method to get user input, rather than the default Python
		# /input() method.

		return self.term.inkey()

	#-==@method
	def process_input(self, userin):
		#-== Overrides this method to ensure that proper key
		# name is sent to the screen's /process_input() method.

		keyname = userin
		if userin.is_sequence:
			keyname = userin.name
		self.curr_screen.process_input(keyname)