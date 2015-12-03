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

date_format		 			= configuration.date_format
decimal			 			= configuration.decimal
def_commodity	 			= configuration.def_commodity

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
		user = raw_input( CL_INF + 'File already exists. Overwrite? [' + CL_DEF + 'no' + CL_TXT + ']: ' + CL_E )
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
			if '.preis_t' in x and not x[0:1] == '_':
				project_files.append( path_to_project + '/projects/' + x )
				project_names.append( x.replace('.preis_t', '').replace('_', ' ') )
		if len(project_files) > 0:
			print CL_TXT + 'Projects:' + CL_E
			print
			for y, x in enumerate(project_names):
				print CL_TXT + '(' + str(y) + ') ' + x + CL_E
			print
			user = raw_input(CL_TXT + 'Chose project [' + CL_DEF + 'none' + CL_TXT + '] : ' + CL_E)
			if user:
				load_it = True
				user2 = raw_input(CL_INF + 'Delete? [' + CL_DEF + 'no' + CL_INF + '] : ' + CL_E)
				if user2:
					if user2 == 'y' or user2 == 'yes':
						os.rename( project_files[int(user)], project_files[int(user)].replace(path_to_project + '/projects/', path_to_project + '/projects/_') )
						load_it = False
				if load_it:
					Loader = LoadObject( project_files[int(user)] )
					if len(Loader) > 0:
						Entries.project_client_name = Loader[0]
					if len(Loader) > 1:
						Entries.project_client_address = Loader[1]
					if len(Loader) > 2:
						Entries.project_client_city = Loader[2]
					if len(Loader) > 3:
						Entries.project_name = Loader[3]
					if len(Loader) > 4:
						Entries.project_offer_filename = Loader[4]
					if len(Loader) > 5:
						Entries.project_client_title = Loader[5]
					if len(Loader) > 6:
						Entries.list = Loader[6]
					if len(Loader) > 7:
						Entries.mods = Loader[7]
					if len(Loader) > 8:
						Entries.Wage = Loader[8]
					if len(Loader) > 9:
						Entries.project_round = Loader[9]
					if len(Loader) > 10:
						Entries.project_commodity = Loader[10]
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
			Saver.append( obj.project_client_name )
			Saver.append( obj.project_client_address )
			Saver.append( obj.project_client_city )
			Saver.append( obj.project_name )
			Saver.append( obj.project_offer_filename )
			Saver.append( obj.project_client_title )
			Saver.append( obj.list )
			Saver.append( obj.mods )
			Saver.append( obj.Wage )
			Saver.append( obj.project_round )
			Saver.append( obj.project_commodity )
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


def preset_choser(what, preset, title='', comment=''):
	print
	if preset.has_key('h'):
		if what == 'entry':
			title_tmp = raw_input(CL_TXT + 'Title [' + CL_DEF + title + CL_TXT + ']: ' + CL_E)
			if title_tmp:
				title = title_tmp
			comment_tmp = raw_input(CL_TXT + 'Comment [' + CL_DEF + comment + CL_TXT + ']: ' + CL_E)
			if comment_tmp:
				comment = comment_tmp
			amount = raw_input(CL_TXT + 'Amount [' + CL_DEF + '1' + CL_TXT + '] : ' + CL_E)
			try:
				amount = float(amount.replace(',', '.')) or 1.0
			except Exception, e:
				amount = 1.0
			Entries.add(what='entry', title=title, h=float(preset['h']), amount=amount, comment=comment)
		elif what == 'mod':
			title_tmp = raw_input(CL_TXT + 'Title [' + CL_DEF + title + CL_TXT + ']: ' + CL_E)
			if title_tmp:
				title = title_tmp
			comment_tmp = raw_input(CL_TXT + 'Comment [' + CL_DEF + comment + CL_TXT + ']: ' + CL_E)
			if comment_tmp:
				comment = comment_tmp
			amount = raw_input(CL_TXT + 'Amount [' + CL_DEF + '1' + CL_TXT + '] : ' + CL_E)
			try:
				amount = float(amount.replace(',', '.')) or 1.0
			except Exception, e:
				amount = 1.0
			entries = raw_input(CL_TXT + 'Entries: ' + CL_E)
			if entries:
				try:
					entries = tuple(entries.split(','))
				except Exception, e:
					entries = ()
				entries = Entries.index_to_entries(entries)
			else:
				entries = []
			Entries.add(what='mod', title=title, multi=float(preset['h']), time=bool(preset['t']), entries=entries, comment=comment, amount=amount)
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
		chose = raw_input(CL_TXT + 'Preset: ' + CL_E)
		try:
			chose = int(chose)
		except Exception, e:
			chose = 0
		if chose > i:
			chose = i
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
		self.project_round = True
		self.project_commodity = def_commodity
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

				delete = raw_input(CL_TXT + 'Delete [' + CL_DEF + 'no' + CL_TXT + ']: ' + CL_E)
				if delete == 'yes' or delete == 'y':
					self.list.pop(which)
					return

				which = int(which)

				title = raw_input(CL_TXT + 'Title [' + CL_DEF + self.list[which].title + CL_TXT + '] : ' + CL_E)
				title = title or self.list[which].title
				self.list[which].title = title

				comment = raw_input(CL_TXT + 'Comment [' + CL_DEF + self.list[which].comment + CL_TXT + '] : ' + CL_E)
				comment = comment or self.list[which].comment
				self.list[which].comment = comment

				h = raw_input(CL_TXT + 'H / Amount [' + CL_DEF + str(self.list[which].h) + CL_TXT + '] : ' + CL_E)
				if h == 'e':
					h = self.hCalc()
				else:
					try:
						h = float(h.replace(',', '.'))
					except Exception, e:
						h = self.list[which].h
				self.list[which].h = h

				amount = raw_input(CL_TXT + 'Amount [' + CL_DEF + str(self.list[which].amount) + CL_TXT + '] : ' + CL_E)
				try:
					amount = float(amount.replace(',', '.'))
				except Exception, e:
					amount = self.list[which].amount
				self.list[which].amount = amount

			# it's a modulator
			else:
				delete = raw_input(CL_TXT + 'Delete [' + CL_DEF + 'no' + CL_TXT + ']: ' + CL_E)
				if delete == 'yes' or delete == 'y':
					self.mods.pop(which - len(self.list))
					return

				which = int(which) - len(self.list)

				title = raw_input(CL_TXT + 'Title ['  + CL_DEF + self.mods[which].title + CL_TXT + '] : ' + CL_E)
				title = title or self.mods[which].title
				self.mods[which].title = title

				comment = raw_input(CL_TXT + 'Comment ['  + CL_DEF + self.mods[which].comment + CL_TXT + '] : ' + CL_E)
				comment = comment or self.mods[which].comment
				self.mods[which].comment = comment

				multi = raw_input(CL_TXT + 'Multiplicator [' + CL_DEF + str(self.mods[which].multi) + CL_TXT + '] : ' + CL_E)
				try:
					multi = float(multi.replace(',', '.'))
				except Exception, e:
					multi = self.mods[which].multi
				self.mods[which].multi = multi

				amount = raw_input(CL_TXT + 'Amount [' + CL_DEF + str(self.mods[which].amount) + CL_TXT + '] : ' + CL_E)
				try:
					amount = float(amount.replace(',', '.'))
				except Exception, e:
					amount = self.mods[which].amount
				self.mods[which].amount = amount

				entries = raw_input(CL_TXT + 'Entries [' + CL_DEF + self.entries_to_index(self.mods[which].entries) + CL_TXT + '] : ' + CL_E)
				if entries:
					try:
						entries = tuple(entries.split(','))
					except Exception, e:
						entries = ()
					entries = self.index_to_entries(entries)
				else:
					entries = self.mods[which].entries
				self.mods[which].entries = entries

				time = raw_input(CL_TXT + 'Time [' + CL_DEF + self.mods[which].getTime_status() + CL_TXT + '] : ' + CL_E)
				if time:
					if time.lower() == 'y' or time.lower() == 'yes':
						time = True
					else:
						time = False
				else:
					time = self.mods[which].time
				self.mods[which].time = time

	def add(self, what='entry', title='Music', h=1.6, amount=1, multi=0.2, entries=[], time=True, comment=''):
		if what == 'entry':
			self.list.append( Single_Entry_Class(title=title, h=h, amount=amount, comment=comment) )
		elif what == 'mod':
			self.mods.append( Single_Mod_Class(title=title, multi=multi, entries=entries, time=time, comment=comment, amount=amount) )

	def hCalc(self):
		h_unit = raw_input(CL_TXT + '-- H / unit [' + CL_DEF + '0.4' + CL_TXT + '] : ' + CL_E)
		try:
			h_unit = float(h_unit.replace(',', '.'))
		except Exception, e:
			h_unit = 0.4
		units = raw_input(CL_TXT + '-- units [' + CL_DEF + '1' + CL_TXT + '] : ' + CL_E)
		try:
			unit = float(unit.replace(',', '.'))
		except Exception, e:
			unit = 1.0
		out = h_unit * units
		print CL_TXT + '-- H / Amount : ' + CL_DEF + str(out) + CL_E
		return out

	def add_edit(self, what):
		if what == 'entry':
			title = raw_input(CL_TXT + 'Title [' + CL_DEF + 'Music' + CL_TXT + '] : ' + CL_E)
			title = title or 'Music'

			comment = raw_input(CL_TXT + 'Comment [] : ' + CL_E)

			h = raw_input(CL_TXT + 'H / Amount [' + CL_DEF + '1.6' + CL_TXT + '] : ' + CL_E)
			if h == 'e':
				h = self.hCalc()
			else:
				try:
					h = float(h.replace(',', '.'))
				except Exception, e:
					h = 1.6

			amount = raw_input(CL_TXT + 'Amount [' + CL_DEF + '1' + CL_TXT + '] : ' + CL_E)
			try:
				amount = float(amount.replace(',', '.'))
			except Exception, e:
				amount = 1.0

			self.add(what=what, title=title, h=h, amount=amount, comment=comment)
		elif what == 'mod':
			title = raw_input(CL_TXT + 'Title [' + CL_DEF + 'Exclusive' + CL_TXT + '] : ' + CL_E)
			title = title or 'Exclusive'

			comment = raw_input(CL_TXT + 'Comment [] : ' + CL_E)

			multi = raw_input(CL_TXT + 'Multiplicator [' + CL_DEF + '3.0' + CL_TXT + '] : ' + CL_E)
			try:
				multi = float(multi.replace(',', '.'))
			except Exception, e:
				multi = 3

			amount = raw_input(CL_TXT + 'Amount [' + CL_DEF + '1' + CL_TXT + '] : ' + CL_E)
			try:
				amount = float(amount.replace(',', '.'))
			except Exception, e:
				amount = 1.0

			entries = raw_input(CL_TXT + 'Entries [] : ' + CL_E)
			if entries:
				try:
					entries = tuple(entries.split(','))
				except Exception, e:
					entries = ()
				entries = self.index_to_entries(entries)
			else:
				entries = []

			time = raw_input(CL_TXT + 'Time [' + CL_DEF + 'False' + CL_TXT + '] : ' + CL_E)
			if time:
				if time.lower() == 'y' or time.lower() == 'yes':
					time = True
				else:
					time = False
			else:
				time = False

			self.add(what=what, title=title, multi=multi, entries=entries, time=time, comment=comment, amount=amount)

	def index_to_entries(self, entries):
		out = []
		for x in entries:
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

	def sum(self, round_it=False):
		out_h = 0
		out_p = 0
		for x in self.list:
			out_h += x.getTime()
			out_p += x.getPrice(self.Wage, round_it)
		for x in self.mods:
			out_h += x.getTime(self.list)
			out_p += x.getPrice(self.Wage, self.list, round_it)
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
			show.append( [CL_OUT + str(i) + CL_E, CL_OUT + unicode(x.title, 'utf-8') + CL_E, CL_OUT + str(x.amount) + ' *' + CL_E, CL_OUT + str(self.return_time( x.getTime(self.list) )) + CL_E, CL_OUT + str(x.getPrice(self.Wage, self.list)) + CL_E] )
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
		wager = raw_input(CL_TXT + '# ' + CL_E)
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
		global loaded_project

		print CL_TXT + 'Enter clients information:' + CL_E

		user = raw_input(CL_TXT + 'Client title [' + CL_DEF + self.project_client_title + CL_TXT + '] : ' + CL_E)
		if user:
			self.project_client_title = user

		user = raw_input(CL_TXT + 'Client name [' + CL_DEF + self.project_client_name + CL_TXT + '] : ' + CL_E)
		if user:
			self.project_client_name = user

		user = raw_input(CL_TXT + 'Client address [' + CL_DEF + self.project_client_address + CL_TXT + '] : ' + CL_E)
		if user:
			self.project_client_address = user

		user = raw_input(CL_TXT + 'Client city [' + CL_DEF + self.project_client_city + CL_TXT + '] : ' + CL_E)
		if user:
			self.project_client_city = user

		user = raw_input(CL_TXT + 'Project name [' + CL_DEF + self.project_name + CL_TXT + '] : ' + CL_E)
		if user:
			self.project_name = user
			loaded_project = user


		self.project_offer_filename = self.project_offer_filename.replace('{YEAR}', datetime.datetime.now().strftime('%Y')).replace('{PROJECT_NAME}', self.project_name.replace(' ', '_'))
		user = raw_input(CL_TXT + 'Offer output file [' + CL_DEF + self.project_offer_filename + CL_TXT + '] : ' + CL_E)
		if user and check_file_exists(user):
			self.project_offer_filename = user

		tmp_round = 'yes' if self.project_round else 'no'
		user = raw_input(CL_TXT + 'Round exported output? [' + CL_DEF + tmp_round + CL_TXT + '] :' + CL_E)
		if user:
			if user == 'y' or user == 'yes':
				self.project_round = True
			else:
				self.project_round = False
		else:
			self.project_round = False

		user = raw_input(CL_TXT + 'Commodity [' + CL_DEF + self.project_commodity + CL_TXT + '] :' + CL_E)
		if user:
			self.project_commodity = user

		print

	def export_to_odt(self):
		if secretary_available:
			self.project_offer_filename = self.project_offer_filename.replace('{YEAR}', datetime.datetime.now().strftime('%Y')).replace('{PROJECT_NAME}', self.project_name.replace(' ', '_'))
			user = raw_input(CL_TXT + 'Filename for export [' + CL_DEF + self.project_offer_filename + CL_TXT + '] : ' + CL_E)
			if not user == '.':
				if not user:
					user = self.project_offer_filename
				if check_file_exists(user):
					self.project_offer_filename = user

					print CL_TXT + 'Exporting to file ...' + CL_E


					# generate content for output
					client = {}
					client['title'] = unicode(self.project_client_title, 'utf-8')
					client['name'] = unicode(self.project_client_name, 'utf-8')
					client['address'] = unicode(self.project_client_address, 'utf-8')
					client['city'] = unicode(self.project_client_city, 'utf-8')
					client['project'] = unicode(self.project_name, 'utf-8')
					client['date'] = unicode(datetime.datetime.now().strftime(date_format), 'utf-8')
					client['sum'] = unicode(str(self.sum(self.project_round)[1]).replace('.', decimal).replace(',0', '') + ' ' + self.project_commodity, 'utf-8')

					entries = []
					for x in self.list:
						entries.append( [unicode(x.title, 'utf-8'), unicode(str(x.amount).replace('.', decimal).replace(',0', ''), 'utf-8'), unicode(str(x.getPrice(self.Wage, self.project_round)).replace('.', decimal).replace(',0', '') + ' ' + self.project_commodity, 'utf-8'), unicode(x.comment or '-', 'utf-8') ] )

					for x in self.mods:
						entries.append( [unicode(x.title, 'utf-8'), unicode(str(x.amount).replace('.', decimal).replace(',0', ''), 'utf-8'), unicode(str(x.getPrice(self.Wage, self.list, self.project_round)).replace('.', decimal).replace(',0', '') + ' ' + self.project_commodity, 'utf-8'), unicode(x.comment or '-', 'utf-8') ] )

					# final endering
					engine = secretary.Renderer()
					result = engine.render(offer_template_filename, entries=entries, client=client)

					output = open(self.project_offer_filename, 'wb')
					output.write(result)
					output.close()


					print CL_TXT + 'Done!' + CL_E

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

	def getPrice(self, wage, round_it=False):
		if round_it:
			return int(round(self.getTime() * wage))
		else:
			return round(self.getTime() * wage, 2)


class Single_Mod_Class(object):
	def __init__(self, title='Exclusive', multi=3, time=False, entries=(), comment='', amount=1):
		self.title = title
		self.comment = comment
		self.multi = multi
		self.time = time
		self.amount = amount
		self.entries = entries

	def getTime_status(self):
		if not self.time:
			return 'no'
		else:
			return 'yes'

	def has_entry(self, list_entry):
		if list_entry.id in self.entries:
			return True
		else:
			return False

	def getTime(self, list):
		out = 0.0
		for x in list:
			if self.has_entry(x) and self.time:
				out += x.getTime() * self.multi * self.amount
		return round(out, 2)

	def getPrice(self, wage, list, round_it=False):
		if round_it:
			out = 0
			for x in list:
				if self.has_entry(x):
					out += x.getPrice(wage) * self.multi
			return int(round(out))
		else:
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
	user = raw_input(CL_TXT + '# ' + CL_E)


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