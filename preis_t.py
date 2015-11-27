# coding=utf-8

import os, sys, shutil, uuid, imp, pickle, datetime
from tabulate import tabulate

try:
	import secretary
	secretary_available = True
except Exception, e:
	print 'Export feature disabled. Need module \'secretary\'. Use \'pip install secretary\' for getting it.'
	secretary_available = False



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

def_project_client_title 	= configuration.def_project_client_title
def_project_client_name 	= configuration.def_project_client_name
def_project_client_address 	= configuration.def_project_client_address
def_project_client_city 	= configuration.def_project_client_city

def_project_name		 	= configuration.def_project_name
def_project_offer_filename 	= configuration.def_project_offer_filename
offer_template_filename	 	= configuration.offer_template_filename

date_format		 	= configuration.date_format
placeholde_date 	= configuration.placeholde_date

placeholde_title 	= configuration.placeholde_title
placeholde_name 	= configuration.placeholde_name
placeholde_address 	= configuration.placeholde_address
placeholde_city 	= configuration.placeholde_city

placeholde_project 	= configuration.placeholde_project

placeholde_option 	= configuration.placeholde_option
placeholde_task 	= configuration.placeholde_task
placeholde_amount 	= configuration.placeholde_amount
placeholde_price 	= configuration.placeholde_price
placeholde_SUM	 	= configuration.placeholde_SUM

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






# functions

def check_file_exists(the_file):
	if os.path.isfile(the_file):
		user = menu( CL_INF + 'File already exists. Overwrite? [' + CL_DEF + 'no' + CL_TXT + ']: ' + CL_E )
		if user:
			if user == 'y' or user == 'yes':
				print CL_INF + 'File will be overwritten on export!' + CL_E
				return True
		return False
	return True


loaded_project = def_project_name

def LoadObject(file):
	with open(file, 'r') as f:
		return pickle.load(f)


def Loader():
	global loaded_project

	if os.path.isdir(path_to_project + '/projects'):
		all_in_dir = os.listdir(path_to_project + '/projects')
		project_files = []
		project_names = []
		for x in all_in_dir:
			if '.preis_t' in x:
				project_files.append( path_to_project + '/projects/' + x )
				project_names.append( x.replace('.preis_t', '').replace('_', ' ') )
		if len(project_files) > 0:
			print CL_TXT + 'Projects:' + CL_E
			print
			for y, x in enumerate(project_names):
				print CL_TXT + '(' + str(y) + ') ' + x + CL_E
			print
			user = raw_input(CL_TXT + 'Chose project [' + CL_DEF + 'none' + CL_TXT + ']: ' + CL_E)
			if user:
				Saver = LoadObject( project_files[int(user)] )
				Entries.list = Saver[0]
				Entries.mods = Saver[1]
				Entries.Wage = Saver[2]
				loaded_project = project_names[int(user)]
		else:
			print CL_INF + 'No projects exists.' + CL_E
			print
	else:
		print CL_INF + 'No projects exists.' + CL_E
		print


def SaveObject(obj, file):
	with open(file, 'wb') as f:
		pickle.dump(obj, f)


def Saver(obj):
	global loaded_project

	user = raw_input( CL_TXT + 'Project name or \'.\' to cancel [' + CL_DEF + loaded_project + CL_TXT + ']: ' + CL_E)
	if not user == '.':
		if not user:
			user = loaded_project
		loaded_project_tmp = user
		user = user.replace(' ', '_')
		if not os.path.isdir(path_to_project + '/projects'):
			os.makedirs(path_to_project + '/projects')
		file_name = path_to_project + '/projects/' + user + '.preis_t'
		write_it = False
		if os.path.isfile(file_name):
			user2 = raw_input( CL_INF + 'Overwrite? [' + CL_DEF + 'no' + CL_INF + ']: ' + CL_E)
			if user2 == 'y' or user2 == 'yes':
				write_it = True
		else:
			write_it = True
		if write_it:
			Saver = []
			Saver.append( obj.list )
			Saver.append( obj.mods )
			Saver.append( obj.Wage )
			SaveObject(Saver, file_name)
			loaded_project = loaded_project_tmp


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

def preset_choser(what, preset, title='', comment=''):
	print
	if preset.has_key('h'):
		if what == 'entry':
			title_tmp = menu(CL_TXT + 'Title [' + CL_DEF + title + CL_TXT + ']: ' + CL_E)
			if title_tmp:
				title = title_tmp
			comment_tmp = menu(CL_TXT + 'Comment [' + CL_DEF + comment + CL_TXT + ']: ' + CL_E)
			if comment_tmp:
				comment = comment_tmp
			amount = menu(CL_TXT + 'Amount: ' + CL_E, 'float')
			amount = amount or 1.0
			Entries.add(what='entry', title=title, h=float(preset['h']), amount=amount, comment=comment)
		elif what == 'mod':
			title_tmp = menu(CL_TXT + 'Title [' + CL_DEF + title + CL_TXT + ']: ' + CL_E)
			if title_tmp:
				title = title_tmp
			comment_tmp = menu(CL_TXT + 'Comment [' + CL_DEF + comment + CL_TXT + ']: ' + CL_E)
			if comment_tmp:
				comment = comment_tmp
			entries = menu(CL_TXT + 'Entries: ' + CL_E, 'tuple')
			if entries:
				entries = Entries.index_to_entries(entries, len(Entries.mods))
			else:
				entries = []
			Entries.add(what='mod', title=title, multi=float(preset['h']), time=bool(preset['t']), entries=entries, comment=comment)
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


# presets

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
		self.project_client_title = def_project_client_title
		self.project_client_name = def_project_client_name
		self.project_client_address = def_project_client_address
		self.project_client_city = def_project_client_city
		self.project_name = def_project_name
		self.project_offer_filename = def_project_offer_filename
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

				comment = menu(CL_TXT + 'Comment [' + CL_DEF + self.list[which].comment + CL_TXT + '] : ' + CL_E)
				comment = comment or self.list[which].comment
				self.list[which].comment = comment

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

				comment = menu(CL_TXT + 'Comment ['  + CL_DEF + self.mods[which].comment + CL_TXT + '] : ' + CL_E)
				comment = comment or self.mods[which].comment
				self.mods[which].comment = comment

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

	def add(self, what='entry', title='Music', h=1.6, amount=1, multi=0.2, entries=[], time=True, comment=''):
		if what == 'entry':
			self.list.append( Single_Entry_Class(title=title, h=h, amount=amount, comment=comment) )
		elif what == 'mod':
			self.mods.append( Single_Mod_Class(title=title, multi=multi, entries=entries, time=time, comment=comment) )

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

			comment = menu(CL_TXT + 'Comment [] : ' + CL_E)

			h = menu(CL_TXT + 'H / Amount [' + CL_DEF + '1.6' + CL_TXT + '] : ' + CL_E, 'float')
			if h == 0.0:
				h = self.hCalc()
			else:
				h = h or 1.6

			amount = menu(CL_TXT + 'Amount [' + CL_DEF + '1' + CL_TXT + '] : ' + CL_E, 'float')
			amount = amount or 1

			self.add(what=what, title=title, h=h, amount=amount, comment=comment)
		elif what == 'mod':
			title = menu(CL_TXT + 'Title [' + CL_DEF + 'Exclusive' + CL_TXT + '] : ' + CL_E)
			title = title or 'Exclusive'

			comment = menu(CL_TXT + 'Comment [] : ' + CL_E)

			multi = menu(CL_TXT + 'Multiplicator [' + CL_DEF + '3.0' + CL_TXT + '] : ' + CL_E, 'float')
			multi = multi or 3

			entries = menu(CL_TXT + 'Entries [] : ' + CL_E, 'tuple')
			if entries:
				entries = self.index_to_entries(entries, len(self.mods))
			else:
				entries = []

			time = menu(CL_TXT + 'Time [' + CL_DEF + 'False' + CL_TXT + '] : ' + CL_E, 'bool')

			self.add(what=what, title=title, multi=multi, entries=entries, time=time, comment=comment)

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
			show.append( [CL_OUT + str(i) + CL_E, CL_OUT + unicode(x.title, 'utf-8') + CL_E, CL_OUT + str(x.amount) + CL_E, CL_OUT + str(self.return_time( x.getTime() )) + CL_E, CL_OUT + str(x.getPrice(self.Wage)) + CL_E] )
			i += 1
		for x in self.mods:
			show.append( [CL_OUT + str(i) + CL_E, CL_OUT + unicode(x.title, 'utf-8') + CL_E, CL_OUT + '*' + CL_E, CL_OUT + str(self.return_time( x.getTime(self.list) )) + CL_E, CL_OUT + str(x.getPrice(self.Wage, self.list)) + CL_E] )
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

	def project_setup(self):
		print CL_TXT + 'Enter clients information:' + CL_E

		user = menu(CL_TXT + 'Client title [' + CL_DEF + self.project_client_title + CL_TXT + '] : ' + CL_E)
		if user:
			self.project_client_title = user

		user = menu(CL_TXT + 'Client name [' + CL_DEF + self.project_client_name + CL_TXT + '] : ' + CL_E)
		if user:
			self.project_client_name = user

		user = menu(CL_TXT + 'Client address [' + CL_DEF + self.project_client_address + CL_TXT + '] : ' + CL_E)
		if user:
			self.project_client_address = user

		user = menu(CL_TXT + 'Client city [' + CL_DEF + self.project_client_city + CL_TXT + '] : ' + CL_E)
		if user:
			self.project_client_city = user

		user = menu(CL_TXT + 'Project name [' + CL_DEF + self.project_name + CL_TXT + '] : ' + CL_E)
		if user:
			self.project_name = user

		user = menu(CL_TXT + 'Offer output file [' + CL_DEF + self.project_offer_filename + CL_TXT + '] : ' + CL_E)
		if user and check_file_exists(user):
			self.project_offer_filename = user

		print

	def export_to_odt(self):
		if secretary_available:
			user = menu(CL_TXT + 'Filename for export [' + CL_DEF + self.project_offer_filename + CL_TXT + '] : ' + CL_E)
			if not user == '.':
				if not user:
					user = self.project_offer_filename
				if check_file_exists(user):
					self.project_offer_filename = user

					print CL_TXT + 'Exporting to file ...' + CL_E


					# generate content for output
					print CL_INF + 'Feature will be available soon ...' + CL_E

		else:
			print 'No secretary-module was loaded. Use \'pip install secretary\' to install it.'

		print


class Single_Entry_Class(object):
	def __init__(self, title='Music', h=1.6, amount=1, comment=''):
		self.title = title
		self.comment = comment
		self.h = h
		self.amount = amount
		self.id = str(uuid.uuid1())

	def getTime(self):
		return round(self.amount * self.h, 2)

	def getPrice(self, wage):
		return round(self.getTime() * wage, 2)


class Single_Mod_Class(object):
	def __init__(self, title='Exclusive', multi=3, time=False, entries=(), comment=''):
		self.title = title
		self.comment = comment
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
			[CL_TXT + 'project / p' + CL_E, CL_TXT + 'set up project name etc.' + CL_E],
			[CL_TXT + 'wage / w' + CL_E, CL_TXT + 'chose the wage' + CL_E],
			[CL_TXT + 'save / s' + CL_E, CL_TXT + 'saves the project' + CL_E],
			[CL_TXT + 'load / l' + CL_E, CL_TXT + 'loads the project' + CL_E],
			[CL_TXT + 'export / exp' + CL_E, CL_TXT + 'exports the project' + CL_E],
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

	# set up project variables
	elif user == 'project' or user == 'p':
		print
		Entries.project_setup()

	# set the wage
	elif user == 'wage' or user == 'w':
		print
		Entries.wage_select()

	# save the project
	elif user == 'save' or user == 's':
		print
		Saver(Entries)

	# load the project
	elif user == 'load' or user == 'l':
		print
		Loader()

	# exports the project
	elif user == 'export' or user == 'exp':
		print
		Entries.export_to_odt()

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