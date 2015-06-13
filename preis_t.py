import os
import uuid
from tabulate import tabulate



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
				
				delete = menu('Delete [no]: ')
				if delete == 'yes' or delete == 'y':
					self.list.pop(which)
					return

				which = int(which)

				title = menu('Title [' + self.list[which].title + '] : ')
				title = title or self.list[which].title
				self.list[which].title = title
				
				h = menu('H / Amount [' + str(self.list[which].h) + '] : ', 'float')
				if h == 0.0:
					h = self.hCalc()
				else:
					h = h or self.list[which].h
				self.list[which].h = h
				
				amount = menu('Amount [' + str(self.list[which].amount) + '] : ', 'float')
				amount = amount or self.list[which].amount
				self.list[which].amount = amount

			# it's a modulator
			else:
				delete = menu('Delete [no]: ')
				if delete == 'yes' or delete == 'y':
					self.mods.pop(which)
					return

				which = int(which) - len(self.list)
				
				title = menu('Title [' + self.mods[which].title + '] : ')
				title = title or self.mods[which].title
				self.mods[which].title = title

				multi = menu('Multiplicator [' + str(self.mods[which].multi) + '] : ', 'float')
				multi = multi or self.mods[which].multi
				self.mods[which].multi = multi

				entries = menu('Entries [' + self.entries_to_index(self.mods[which].entries) + '] : ', 'tuple')
				if entries:
					entries = self.index_to_entries(entries, len(self.mods))
				else:
					entries = self.mods[which].entries
				self.mods[which].entries = entries

				time = menu('Time [' + self.mods[which].getTime_status() + '] : ', 'bool')
				self.mods[which].time = time
	
	def add(self, what='entry', title='Music', h=1.6, amount=1, multi=0.2, entries=[], time=True):
		if what == 'entry':
			self.list.append( self.Single_Entry_Class(title=title, h=h, amount=amount) )
		elif what == 'mod':
			self.mods.append( self.Single_Mod_Class(title=title, multi=multi, entries=entries, time=time) )

	def hCalc(self):
		h_unit = menu('-- H / unit [0.3] : ', 'float')
		h_unit = h_unit or 0.3
		units = menu('-- units [1] : ', 'float')
		units = units or 1.0
		out = h_unit * units
		print '-- H / Amount :', str(out)
		return out

	def add_edit(self, what):
		if what == 'entry':
			title = menu('Title [Music] : ')
			title = title or 'Music'
			
			h = menu('H / Amount [1.6] : ', 'float')
			if h == 0.0:
				h = self.hCalc()
			else:
				h = h or 1.6

			amount = menu('Amount [1] : ', 'float')
			amount = amount or 1
			
			self.add(what=what, title=title, h=h, amount=amount)
		elif what == 'mod':
			title = menu('Title [Exclusive] : ')
			title = title or 'Exclusive'
			
			multi = menu('Multiplicator [3.0] : ', 'float')
			multi = multi or 3

			entries = menu('Entries [] : ', 'tuple')
			if entries:
				entries = self.index_to_entries(entries, len(self.mods))
			else:
				entries = []

			time = menu('Time [False] : ', 'bool')
			
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
		return hours + ':' + minutes if floaty > 0 else '*'
	
	def show_as_table(self, just_show=False, head=['ID', 'Title', 'Amount', 'H','Price']):
		show = []

		i = 0
		for x in self.list:
			show.append( [i, x.title, x.amount, self.return_time( x.getTime() ), x.getPrice(self.Wage)] )
			i += 1
		for x in self.mods:
			show.append( [i, x.title, '*', self.return_time( x.getTime(self.list) ), x.getPrice(self.Wage, self.list)] )
			i += 1
		if not just_show:
			show.append( [str(i), '[New entry]', '...', '?', '?'] )
			show.append( [str(i+1), '[New mod]', '...', '?', '?'] )
			show.append( [ '--', '----', '----', '----', '----' ])
			show.append( [ '', '', '', self.return_time( self.sum()[0] ), self.sum()[1]])
			if self.sum()[0] > 0:
				show.append( [ '', '', '', '', str( round(self.sum()[1] / self.sum()[0], 2) ) + ' E/h' ])
		print tabulate(show, head)
		print
		
	def wage_select(self):
		print 'Actual wage: ' + str(self.Wage)
		print '(a) Pro [' + str(self.Wage_Pro) + ']'
		print '(b) Edu [' + str(self.Wage_Edu) + ']'
		print '(c) Low [' + str(self.Wage_Low) + ']'
		print '(any number) Individual wage'
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
	print
	print
	print '#' * 50
	print


def Enter():
	print
	raw_input('Press enter ...')


def menu(txt='# ', typ='str'):
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
			amount = menu('Amount: ', 'float')
			amount = amount or 1.0
			Entries.add(what='entry', title=title, h=float(preset['h']), amount=amount)
		elif what == 'mod':
			entries = menu('Entries: ', 'tuple')
			if entries:
				entries = Entries.index_to_entries(entries, len(Entries.mods))
			else:
				entries = []
			Entries.add(what='mod', title=title, multi=float(preset['h']), time=bool(preset['t']), entries=entries)
	else:
		i = 0
		c = []
		t = []
		print '(' + str(i) + ') _Edit_'
		c.append(0)
		for x in sorted(preset):
			i += 1
			print '(' + str(i) + ') ' + x
			c.append(x)
		chose = menu('Preset: ', 'int')
		next_title_pre = '' if title == '' else title + ' > '
		if chose == 0 or not chose:
			Entries.add_edit(what)
		else:
			preset_choser(what, preset[c[chose]], next_title_pre + c[chose])




# start here --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

Entries = Entries_Class()
user = ''


while user != 'exit' and user != 'e':
	
	cls()
	Entries.show_as_table()
	user = menu()

	
	# input is a command / string
	user = user.lower()

	# show the help
	if user == 'help' or user == 'h':
		print
		head = ['command', 'result']
		content = [
			['0-99', 'edit the entry / mod or chose a number higher to create a new one'],
			['new / n', 'creates a new project immediately'],
			['wage / w', 'chose the wage'],
			['help / h', 'this help text'],
			['exit / e', 'end the program']
			]
		print tabulate(content, head)
		Enter()

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
		Enter()

	
	# input refers to an ID
	else:
		try:
			user = int(user)

			# Edit entry
			if user < Entries.count() and user >= 0:
				print
				Entries.edit(user)

			# new  entry
			elif user == Entries.count():
				print
				preset_choser('entry', presets['E'])

			# new modulator
			elif user == Entries.count()+1:
				print
				preset_choser('mod', presets['M'])
		
		except Exception, e:
			pass