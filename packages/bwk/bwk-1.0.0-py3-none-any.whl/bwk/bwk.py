#-== @h1
# Blessed Window Kit (bwk)
#
#-== A simple Python windowing kit module
# for use with _*Blessed*_ terminal formatting.
#
#-== * Documentation:   !https://blessed.readthedocs.io/en/1.20.0/
#    * Source Code:     !https://github.com/jquast/blessed
#    * Installation: /- pip3 install blessed==1.20.0 -/
#
#-== - Use in your project by importing the module:
#		-- /-from bwk import Border, Window, echo, flush-/

from blessed import Terminal

from .characters import UnicodeChars as UTF
#-==@class
# bwk.characters.UnicodeChars
# -== A struct-like class which contains
# Unicode characters commonly used in
# Text-Based User Interfaces (TUI's).

#-==@class
# bwk
#
#-== @constants
# DEFAULT_WINDOW_BORDER	:	a /borderchar string (see /Border object)
#							which uses the solid line Unicode characters

#-==@method
def echo(str, end='', flush=False):
	#-== @params
	#	str:	the string to output
	#	end:	a suffix to append to the string
	#	flush:	whether or not to flush the buffer
	#			of the output stream
	#
	#-== A convenience method for working with _*Blessed*_ .
	# This method will use the built-in Python /print() method
	# but with the above parameters defaulted differently.
	# It is intended to be used as a way to buffer output for
	# the current outstream without flushing it.

	print(str, end=end, flush=flush)

#-==@method
def flush():
	#-== A convenience method which flushes the current output stream.
	# Equivalent to /-
	print('', end='', flush=True)
	# -/ .


#-==@method
def window_shopper(termstuff, *args, **kwargs):
	#-== @params
	#	termstuff:	a function to execute within
	#					a _*Blessed*_ terminal context
	#	args:		arguments to be passed to /termstuff
	#	kwargs:		keyword arguments to be passed to /termstuff
	#
	#-== This method provides a default terminal context
	# to preview window layouts. The terminal context provided is
	# A fullscreen /blessed.Terminal with a hidden cursor.
	# Pressing any key ends the terminal context.
	#
	#-== The /termstuff function must receive the /Terminal object
	# as its first argument, it must include /*args and /**kwargs ,
	# and has no return value.
	#@codeblock
	#  //def mywindowfunc(term, *args, **kwargs):
	#  //   # do window layout here
	#@endcodeblock
	#
	#-==@note
	# The terminal context will automaticaly flush the stream,
	# so you do not need to use the /flush() method, only /echo() .

	term = Terminal()
	with term.fullscreen(), term.cbreak(), term.hidden_cursor():
		termstuff(term, *args, **kwargs)
		flush()
		c = term.inkey()



#-==@class
class Border:
	#-== A class for defining the borders of a /Window object.
	#
	#-== @attributes
	#	upper_left_corner:	( *default:* /'' )
	#	top_border:			( *default:* /'' )
	#	upper_right_corner:	( *default:* /'' )
	#	right_border:		( *default:* /'' )
	#	lower_right_corner:	( *default:* /'' )
	#	bottom_border:		( *default:* /'' )
	#	lower_left_corner:	( *default:* /'' )
	#	left_border:		( *default:* /'' )

	#-==@method
	def __init__(self, borderchars=''):
		#-== @params
		# borderchars:	a string of characters to use for the border
		#
		#-== Creates a new /Border object.
		# The /borderchars string must be exactly 8 characters long.
		# If it is not, then no border is used.
		# The characters form the corners and sides
		# starting with the upper left corner and going clockwise.
		#
		#-== *Example:* /-borderchars='1=2:3+4|-/'
		#@codeblock
		#  1=====2
		#  |     :
		#  |     :
		#  4+++++3
		#@endcodeblock
		#
		#-== You can also directly alter any of the border characters
		# via the object's attributes (see *Attributes* above)

		self.upper_left_corner  = ''
		self.top_border         = ''
		self.upper_right_corner = ''
		self.right_border       = ''
		self.lower_right_corner = ''
		self.bottom_border      = ''
		self.lower_left_corner  = ''
		self.left_border        = ''
		if len(borderchars) == 8:
			self.upper_left_corner  = borderchars[0]
			self.top_border         = borderchars[1]
			self.upper_right_corner = borderchars[2]
			self.right_border       = borderchars[3]
			self.lower_right_corner = borderchars[4]
			self.bottom_border      = borderchars[5]
			self.lower_left_corner  = borderchars[6]
			self.left_border        = borderchars[7]

	def top_border_height(self):
		return max(
			len(self.upper_left_corner),
			len(self.top_border),
			len(self.upper_right_corner),
		)

	def bottom_border_height(self):
		return max(
			len(self.lower_left_corner),
			len(self.bottom_border),
			len(self.lower_right_corner),
		)

	def height_reduction(self):
		reduce = 0
		reduce += self.top_border_height()
		reduce += self.bottom_border_height()
		return reduce

	def left_border_width(self):
		return max(
			len(self.upper_left_corner),
			len(self.left_border),
			len(self.lower_left_corner),
		)

	def right_border_width(self):
		return max(
			len(self.upper_right_corner),
			len(self.right_border),
			len(self.lower_right_corner),
		)

	def width_reduction(self):
		reduce = 0
		reduce += self.left_border_width()
		reduce += self.right_border_width()
		return reduce


DEFAULT_WINDOW_BORDER =	UTF.line.solid.corner.upper_left + \
						UTF.line.solid.horizontal + \
						UTF.line.solid.corner.upper_right + \
						UTF.line.solid.vertical + \
						UTF.line.solid.corner.lower_right + \
						UTF.line.solid.horizontal + \
						UTF.line.solid.corner.lower_left + \
						UTF.line.solid.vertical


#-==@class
class Window:

	TITLE_ALIGNS = ['left', 'center', 'right']

	#-== A rectangular container for displaying content.
	#
	#-== @constants
	#	TITLE_ALIGNS:	A set of strings to identify
	#						the alignment of the window /title
	#
	#-== @attributes
	#	term:	the /blessed.Terminal object used for display
	#	x:		the column of the terminal that the upper left corner is placed
	#	y:		the row of the terminal that the upper left corner is placed
	#	height:	the total height of the window (including the borders)
	#	width:	the total width of the window (including borders)
	#	border:	a /Border object which defines the border display of the window
	#	title:	the title displayed at the top of the window
	#	title_align: the alignment of the /title
	#	content: a string of characters to display in the window
	#
	#-== @note
	# When a /Window is defined, there must be content added to it,
	# either by setting the /content attribute directly, or by overriding
	# the /render_content() method. The window is not buffered to the
	# output stream unless the /render() method is called.

	#-==@method
	def __init__(self, term, x, y, height=None, width=None,
					fore_color=None, bg_color=None,
					border=DEFAULT_WINDOW_BORDER,
					title='', title_align='center'):
		#-== @params
		#	term:	the /blessed.Terminal object used for display
		#	x:		the column of the terminal that the upper left corner is placed
		#	y:		the row of the terminal that the upper left corner is placed
		#	height:	the total height of the window (including the borders)
		#	width:	the total width of the window (including borders)
		#	fore_color: _not yet implemented_
		#	bg_color: _not yet implemented_
		#	border:	a /borderchar string or a /Border object
		#	title:	the title displayed at the top of the window
		#	title_align: the alignment of the /title
		#
		#-== If /height or /width is not provided, then that dimension
		# will stretch all the way to the edge of the terminal.
		# If /border is set to /None , then no border will be drawn.
		# The /title will not be displayed unless there is a /border with
		# at least the /top_border attribute set.
		# The /title_align string must be
		# one of the following values: /left , /center , or /right .

		self.term = term # blessed.Terminal object
		self.x = x
		self.y = y
		self.height = height
		self.width = width
		self.border = border # can be a string of 8 chars
							 # representing the border or
							 # a Border object
		if border is not None:
			if isinstance(border, str):
				self.border = Border(border)
			elif isinstance(border, Border):
				self.border = border
			else:
				raise TypeError('border must be type str or Border')

		self.fore_color = fore_color
		self.bg_color = bg_color
		self.title = title
		if title_align not in self.TITLE_ALIGNS:
			raise ValueError("title_align must be 'left', 'center', or 'right'")
		self.title_align = title_align

		self.content = ''


	#-==@method
	def render(self):
		#-== Echoes the window to the output stream buffer (via the /echo() function).
		# The content of the window is limited by the /height and /width of the window
		# (minus the height and width of the border). Any characters which are beyond
		# the dimensions of the window will not be displayed.

		render_height = self.height
		render_width = self.width

		if render_height is None:
			render_height = self.term.height - self.y

		if render_width is None:
			render_width = self.term.width - self.x

		if self.border is not None:
			render_height -= self.border.height_reduction()
			render_width -= self.border.width_reduction()

		echo(self.term.move_xy(self.x, self.y))

		if self.border is not None:
			if self.border.top_border_height() > 0:
				echo(self.border.upper_left_corner)
				title_func = self.term.center
				if self.title_align == 'left':
					title_func = self.term.ljust
				elif self.title_align == 'center':
					title_func = self.term.center
				elif self.title_align == 'right':
					title_func = self.term.rjust

				echo(title_func(self.title, width=render_width, fillchar=self.border.top_border))
				echo(self.border.upper_right_corner)
				echo(self.term.move_down(self.border.top_border_height()), self.term.move_x(self.x))

		content = self.render_content(render_width, render_height)
		if isinstance(content, str):
			content = content.split('\n')

		i = 0
		while i < render_height:

			if self.border is not None:
				echo(self.border.left_border)

			clean_line = ''
			if i < len(content):
				clean_line = str(content[i]).strip('\n\r')
				clean_line = self.term.truncate(clean_line, width=render_width)
			echo(self.term.ljust(clean_line, width = render_width))

			if self.border is not None:
				echo(self.border.right_border)

			echo(self.term.move_down(1), self.term.move_x(self.x))
			i += 1

		if self.border is not None:
			echo(self.border.lower_left_corner + self.border.bottom_border*render_width + self.border.lower_right_corner)


	#-==@method
	def render_content(self, max_width, max_height):
		#-== @params
		#	max_width:	the total width of the window
		#					(minus the width of the borders)
		#	max_height:	the total height of the window
		#					(minus the height of the borders)
		#
		#-== @return
		# A string or list of strings which will fit
		# in the dimensions of the window.
		#
		#-== This method is provided to be overriden, either by
		# overwriting the instance attrbute /render_content with
		# a different function, or by overriding this function in
		# a subclass. By default, this method simply returns the
		# window's /content string.
		#
		#-== This method is called by the /render() method.
		# If the return value is a string, /render() will
		# iterate over the each line (delimited by a /\\n ).
		# If the return value is a list of strings,
		# /render() will iterate over the list.

		return self.content



