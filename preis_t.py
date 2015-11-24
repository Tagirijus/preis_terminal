# coding=utf-8

import os, sys, uuid, imp
from tabulate import tabulate



### ### ###
### ### ### load configurarion file for variables
### ### ###

# !!!!! SET YOU INDIVIDUAL SETTINGS FILE HERE
# !!!!! IT MUST BE SET UP LIKE THE 'preis_t-settings-default.py' FILE
####
###
#

SETTINGS_FILE = 'preis_t-settings.py'

#
###
####
# !!!!!
# !!!!!

# get the actual path to the python script
path_to_project = os.path.dirname(os.path.realpath(__file__))


# check if user set an individual settings file, or load default otherwise

if os.path.isfile(path_to_project + '/' + SETTINGS_FILE):
	configuration = imp.load_source('preis_t-settings', path_to_project + '/' + SETTINGS_FILE)
else:
	if os.path.isfile(path_to_project + '/preis_t-settings-default.py'):
		configuration = imp.load_source('preis_t-settings', path_to_project + '/preis_t-settings-default.py')
	else:
		print 'No settings file found.'
		exit()


# getting the variables from the settings file - don't change the values here!

colorize = configuration.colorize

CL_TXT = configuration.CL_TXT
CL_INF = configuration.CL_INF
CL_DEF = configuration.CL_DEF
CL_DIM = configuration.CL_DIM
CL_OUT = configuration.CL_OUT
CL_E = configuration.CL_E

### ### ###
### ### ### load configurarion file for variables - END
### ### ###






# presets

def dict_merge(a, b):
	'''recursively merges dict's. not just simple a['key'] = b['key'], if
	both a and bhave a key who's value is a dict then dict_merge is called
	on both values and the result stored in the returned dictionary.'''
	if not isinstance(b, dict):
		return b

	result = a.copy()
	for k, v in b.iteritems():
		if k in result and isinstance(result[k], dict):
				result[k] = dict_merge(result[k], v)
		else:
			result[k] = v
	return result

def array_of_paths_to_dict(array):
	out = {}
	for i in array:
		out = dict_merge(out, reduce(lambda x, y: {y: x}, reversed(i)) )
	return out

def updateDict(the_dict, the_array):
	if type(the_array) is list:
		if len(the_array) > 2:
			the_dict[the_array[0]] = {}
			updateDict(the_dict, the_array[1:])
		elif len(the_array) == 2:
			the_dict[the_array[0]] = the_array[1]

cur_dir = os.path.dirname(os.path.realpath(__file__))

presets = {}
if os.path.isfile(cur_dir + '/presets.preis_presets'):
	with open (cur_dir + '/presets.preis_presets', 'r') as myfile:
		presets_file = myfile.read().splitlines()
		pre_presets = []
		for x in presets_file:
			pre_presets.append( x.split('>') )
		myfile.close()

		presets = array_of_paths_to_dict(pre_presets)




# classes

class Entries_Class(object):
	def __init__(self):
		self.list = []
		self.mods = []
		self.Wage = 40
		self.Wage_Pro = 40
		self.Wage_Edu = 33
		self.Wage_Low = 25

	def count(self):
		return len(self.list) + len(self.mods)

	def edit(self, which):
		if type(which) is not str:

			# it's an entry
			if which < len(self.list):

				delete = menu(CL_TXT + 'Delete [' + CL_DEF + 'no' + CL_TXT + ']: ' + CL_E)
				if delete == 'yes' or delete == 'y':
					self.list.pop(which)
					return

				which = int(which)

				title = menu(CL_TXT + 'Title [' + CL_DEF + self.list[which].title + CL_TXT + '] : ' + CL_E)
				title = title or self.list[which].title
				self.list[which].title = title

				h = menu(CL_TXT + 'H / Amount [' + CL_DEF + str(self.list[which].h) + CL_TXT + '] : ' + CL_E, 'float')
				if h == 0.0:
					h = self.hCalc()
				else:
					h = h or self.list[which].h
				self.list[which].h = h

				amount = menu(CL_TXT + 'Amount [' + CL_DEF + str(self.list[which].amount) + CL_TXT + '] : ' + CL_E, 'float')
				amount = amount or self.list[which].amount
				self.list[which].amount = amount

			# it's a modulator
			else:
				delete = menu(CL_TXT + 'Delete [' + CL_DEF + 'no' + CL_TXT + ']: ' + CL_E)
				if delete == 'yes' or delete == 'y':
					self.mods.pop(which - len(self.list))
					return

				which = int(which) - len(self.list)

				title = menu(CL_TXT + 'Title ['  + CL_DEF + self.mods[which].title + CL_TXT + '] : ' + CL_E)
				title = title or self.mods[which].title
				self.mods[which].title = title

				multi = menu(CL_TXT + 'Multiplicator [' + CL_DEF + str(self.mods[which].multi) + CL_TXT + '] : ' + CL_E, 'float')
				multi = multi or self.mods[which].multi
				self.mods[which].multi = multi

				entries = menu(CL_TXT + 'Entries [' + CL_DEF + self.entries_to_index(self.mods[which].entries) + CL_TXT + '] : ' + CL_E, 'tuple')
				if entries:
					entries = self.index_to_entries(entries, len(self.mods))
				else:
					entries = self.mods[which].entries
				self.mods[which].entries = entries

				time = menu(CL_TXT + 'Time [' + CL_DEF + self.mods[which].getTime_status() + CL_TXT + '] : ' + CL_E, 'bool')
				self.mods[which].time = time

	def add(self, what='entry', title='Music', h=1.6, amount=1, multi=0.2, entries=[], time=True):
		if what == 'entry':
			self.list.append( self.Single_Entry_Class(title=title, h=h, amount=amount) )
		elif what == 'mod':
			self.mods.append( self.Single_Mod_Class(title=title, multi=multi, entries=entries, time=time) )

	def hCalc(self):
		h_unit = menu(CL_TXT + '-- H / unit [' + CL_DEF + '0.4' + CL_TXT + '] : ' + CL_E, 'float')
		h_unit = h_unit or 0.4
		units = menu(CL_TXT + '-- units [' + CL_DEF + '1' + CL_TXT + '] : ' + CL_E, 'float')
		units = units or 1.0
		out = h_unit * units
		print CL_TXT + '-- H / Amount : ' + CL_DEF + str(out) + CL_E
		return out

	def add_edit(self, what):
		if what == 'entry':
			title = menu(CL_TXT + 'Title [' + CL_DEF + 'Music' + CL_TXT + '] : ' + CL_E)
			title = title or 'Music'

			h = menu(CL_TXT + 'H / Amount [' + CL_DEF + '1.6' + CL_TXT + '] : ' + CL_E, 'float')
			if h == 0.0:
				h = self.hCalc()
			else:
				h = h or 1.6

			amount = menu(CL_TXT + 'Amount [' + CL_DEF + '1' + CL_TXT + '] : ' + CL_E, 'float')
			amount = amount or 1

			self.add(what=what, title=title, h=h, amount=amount)
		elif what == 'mod':
			title = menu(CL_TXT + 'Title [' + CL_DEF + 'Exclusive' + CL_TXT + '] : ' + CL_E)
			title = title or 'Exclusive'

			multi = menu(CL_TXT + 'Multiplicator [' + CL_DEF + '3.0' + CL_TXT + '] : ' + CL_E, 'float')
			multi = multi or 3

			entries = menu(CL_TXT + 'Entries [] : ' + CL_E, 'tuple')
			if entries:
				entries = self.index_to_entries(entries, len(self.mods))
			else:
				entries = []

			time = menu(CL_TXT + 'Time [' + CL_DEF + 'False' + CL_TXT + '] : ' + CL_E, 'bool')

			self.add(what=what, title=title, multi=multi, entries=entries, time=time)

	def index_to_entries(self, index, which):
		out = []
		for x in index:
			out.append( self.list[int(x)].id )
		return out

	def entries_to_index(self, entries):
		out = ''
		for x in self.list:
			if x.id in entries:
				if out == '':
					out = str(self.list.index(x))
				else:
					out = out + ', ' + str(self.list.index(x))
		return out

	def sum(self):
		out_h = 0
		out_p = 0
		for x in self.list:
			out_h += x.getTime()
			out_p += x.getPrice(self.Wage)
		for x in self.mods:
			out_h += x.getTime(self.list)
			out_p += x.getPrice(self.Wage, self.list)
		return [out_h, out_p]

	def return_time(self, floaty):
		hours = int(floaty)
		minutes = int( (floaty - hours) * 60 )
		hours = str(hours) if hours > 9 else '0' + str(hours)
		minutes = str(minutes) if minutes > 9 else '0' + str(minutes)
		return hours + ':' + minutes if floaty > 0.0 else '*'

	def show_as_table(self, just_show=False, head=[CL_TXT + 'ID' + CL_E, CL_TXT + 'Title' + CL_E, CL_TXT + 'Amount' + CL_E, CL_TXT + 'H' + CL_E, CL_TXT + 'Price' + CL_E]):
		show = []

		i = 0
		for x in self.list:
			show.append( [CL_OUT + str(i) + CL_E, CL_OUT + x.title + CL_E, CL_OUT + str(x.amount) + CL_E, CL_OUT + str(self.return_time( x.getTime() )) + CL_E, CL_OUT + str(x.getPrice(self.Wage)) + CL_E] )
			i += 1
		for x in self.mods:
			show.append( [CL_OUT + str(i) + CL_E, CL_OUT + x.title + CL_E, CL_OUT + '*' + CL_E, CL_OUT + str(self.return_time( x.getTime(self.list) )) + CL_E, CL_OUT + str(x.getPrice(self.Wage, self.list)) + CL_E] )
			i += 1
		if not just_show:
			show.append( [CL_TXT + 'a' + CL_E, CL_TXT + '[New entry]' + CL_E, CL_TXT + '...' + CL_E, CL_TXT + '?' + CL_E, CL_TXT + '?' + CL_E] )
			show.append( [CL_TXT + 'm' + CL_E, CL_TXT + '[New mod]' + CL_E, CL_TXT + '...' + CL_E, CL_TXT + '?' + CL_E, CL_TXT + '?' + CL_E] )
			show.append( [CL_TXT + '--' + CL_E, CL_TXT + '----' + CL_E, CL_TXT + '----' + CL_E, CL_TXT + '----' + CL_E, CL_TXT + '----' + CL_E])
			show.append( [ '', '', '', CL_OUT + str(self.return_time( self.sum()[0] )) + CL_E, CL_OUT + str(self.sum()[1]) + CL_E])
			if self.sum()[0] > 0:
				show.append( [ '', '', '', '', CL_OUT + str( round(self.sum()[1] / self.sum()[0], 2) ) + ' E/h' + CL_E ])
		print tabulate(show, head)
		print

	def wage_select(self):
		print CL_TXT + 'Actual wage: ' + CL_DEF + str(self.Wage) + CL_E
		print CL_TXT + '(a) Pro [' + CL_DEF + str(self.Wage_Pro) + CL_TXT + ']' + CL_E
		print CL_TXT + '(b) Edu [' + CL_DEF + str(self.Wage_Edu) + CL_TXT +']' + CL_E
		print CL_TXT + '(c) Low [' + CL_DEF + str(self.Wage_Low) + CL_TXT + ']' + CL_E
		print CL_TXT + '(any number) Individual wage' + CL_E
		wager = menu()
		if wager == 'a':
			self.Wage = self.Wage_Pro
		elif wager == 'b':
			self.Wage = self.Wage_Edu
		elif wager == 'c':
			self.Wage = self.Wage_Low
		else:
			try:
				wager = int(wager)
				wager = wager or self.Wage
				self.Wage = wager
			except Exception, e:
				pass

	class Single_Entry_Class(object):
		def __init__(self, title='Music', h=1.6, amount=1):
			self.title = title
			self.h = h
			self.amount = amount
			self.id = str(uuid.uuid1())

		def getTime(self):
			return round(self.amount * self.h, 2)

		def getPrice(self, wage):
			return round(self.getTime() * wage, 2)

	class Single_Mod_Class(object):
		def __init__(self, title='Exclusive', multi=3, time=False, entries=()):
			self.title = title
			self.multi = multi
			self.time = time
			self.entries = entries

		def getTime_status(self):
			if not self.time:
				return 'False'
			else:
				return 'True'

		def has_entry(self, list_entry):
			if list_entry.id in self.entries:
				return True
			else:
				return False

		def getTime(self, list):
			out = 0.0
			for x in list:
				if self.has_entry(x) and self.time:
					out += x.getTime() * self.multi
			return round(out, 2)

		def getPrice(self, wage, list):
			out = 0.0
			for x in list:
				if self.has_entry(x):
					out += x.getPrice(wage) * self.multi
			return round(out, 2)




# functions only

def cls():
	print
	print CL_INF + '#' * 50 + CL_E
	print


def menu(txt=CL_TXT + '# ' + CL_E, typ='str'):
	out = raw_input(txt)
	if out:
		if typ == 'str':
			return out
		elif typ == 'int':
			try:
				return int(out)
			except ValueError:
				return 0
		elif typ == 'float':
			try:
				if '*' in out:
					calc = out.split('*')
					for x in xrange(0,len(calc)):
						calc[x] = calc[x].replace(',', '.')
						try:
							calc[x] = float(calc[x])
						except Exception, e:
							calc[x] = 1.0
					out = 1.0
					for x in calc:
						out = out*x
					return out
				else:
					return float(out.replace(',', '.'))
			except Exception, e:
				return 0.0
		elif typ == 'tuple':
			try:
				return tuple(out.split(','))
			except Exception, e:
				return ()
		elif typ == 'bool':
			try:
				if out == '1' or out.lower() == 'true':
					return True
				else:
					return False
			except Exception, e:
				return False
	else:
		return out

def preset_choser(what, preset, title=''):
	print
	if preset.has_key('h'):
		if what == 'entry':
			title_tmp = menu(CL_TXT + 'Tite [' + CL_DEF + title + CL_TXT + ']: ' + CL_E)
			if title_tmp:
				title = title_tmp
			amount = menu(CL_TXT + 'Amount: ' + CL_E, 'float')
			amount = amount or 1.0
			Entries.add(what='entry', title=title, h=float(preset['h']), amount=amount)
		elif what == 'mod':
			title_tmp = menu(CL_TXT + 'Tite [' + CL_DEF + title + CL_TXT + ']: ' + CL_E)
			if title_tmp:
				title = title_tmp
			entries = menu(CL_TXT + 'Entries: ' + CL_E, 'tuple')
			if entries:
				entries = Entries.index_to_entries(entries, len(Entries.mods))
			else:
				entries = []
			Entries.add(what='mod', title=title, multi=float(preset['h']), time=bool(preset['t']), entries=entries)
	else:
		i = 0
		c = []
		t = []
		print CL_TXT + '(' + str(i) + ') _Edit_' + CL_E
		c.append(0)
		for x in sorted(preset):
			i += 1
			print CL_TXT + '(' + str(i) + ') ' + x + CL_E
			c.append(x)
		chose = menu(CL_TXT + 'Preset: ' + CL_E, 'int')
		next_title_pre = '' if title == '' else title + ' > '
		if chose == 0 or not chose:
			Entries.add_edit(what)
		else:
			preset_choser(what, preset[c[chose]], next_title_pre + c[chose])




# start here --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

Entries = Entries_Class()
user = ''

print
print CL_INF + 'Preis terminal calculation' + CL_E

while user != 'exit' and user != 'e' and user != '.':

	cls()
	Entries.show_as_table()
	user = menu()


	# input is a command / string
	user = user.lower()

	# show the help
	if user == 'help' or user == 'h':
		print
		head = [CL_TXT + 'command' + CL_E, CL_TXT + 'result' + CL_E]
		content = [
			[CL_TXT + '0-99' + CL_E, CL_TXT + 'edit the entry / mod or chose a number higher to create a new one' + CL_E],
			[CL_TXT + 'entry / a' + CL_E, CL_TXT + 'adds a new entry' + CL_E],
			[CL_TXT + 'mod / m' + CL_E, CL_TXT + 'adds a new modulator' + CL_E],
			[CL_TXT + 'new / n' + CL_E, CL_TXT + 'creates a new project immediately' + CL_E],
			[CL_TXT + 'wage / w' + CL_E, CL_TXT + 'chose the wage' + CL_E],
			[CL_TXT + 'help / h' + CL_E, CL_TXT + 'this help text' + CL_E],
			[CL_TXT + 'exit / e / .' + CL_E, CL_TXT + 'end the program' + CL_E]
			]
		print tabulate(content, head)
		print

	# new  entry
	elif user == 'entry' or user == 'a':
		print
		preset_choser('entry', presets['E'])

	# new modulator
	elif user == 'mod' or user == 'm':
		print
		preset_choser('mod', presets['M'])

	# creates a new project
	elif user == 'new' or user == 'n':
		Entries = Entries_Class()

	# set the wage
	elif user == 'wage' or user == 'w':
		print
		Entries.wage_select()

	# testing
	elif user == 'test' or user == 't':
		print uuid.uuid1()
		print


	# input refers to an ID
	else:
		try:
			user = int(user)

			# Edit entry
			if user < Entries.count() and user >= 0:
				print
				Entries.edit(user)

		except Exception, e:
			pass

print