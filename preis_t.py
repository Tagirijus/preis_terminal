# coding=utf-8

import os, sys, uuid, imp, datetime
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

def_project_company			= configuration.def_project_company
def_project_client_title 	= configuration.def_project_client_title
def_project_client_name 	= configuration.def_project_client_name
def_project_client_address 	= configuration.def_project_client_address
def_project_client_city 	= configuration.def_project_client_city

def_project_name		 	= configuration.def_project_name
def_project_offer_filename 	= configuration.def_project_offer_filename
offer_template_filename	 	= configuration.offer_template_filename
def_project_save_name		= configuration.def_project_save_name

date_format		 			= configuration.date_format
decimal			 			= configuration.decimal
def_commodity	 			= configuration.def_commodity

old_filetype_save			= configuration.old_filetype_save
old_filetype_load			= configuration.old_filetype_load

if old_filetype_load or old_filetype_save:
	import pickle

small_table = configuration.small_table
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

def str2bool(str):
	return str.lower() in ('true', '1')

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
	global loaded_project, Entries

	if os.path.isdir(path_to_project + '/projects'):
		all_in_dir = os.listdir(path_to_project + '/projects')
		project_files = []
		project_names = []
		for x in all_in_dir:
			if '.preis_t' in x and not x[0:1] == '_':
				project_files.append( path_to_project + '/projects/' + x )
				project_names.append( x.replace('.preis_t', '').replace('_', ' ') )
		project_files = sorted(project_files)
		project_names = sorted(project_names)
		if len(project_files) > 0:
			print CL_TXT + 'Projects:' + CL_E
			print
			for y, x in enumerate(project_names):
				print CL_TXT + '(' + str(y) + ') ' + x + CL_E
			print
			user = raw_input(CL_TXT + 'Chose project [' + CL_DEF + 'none' + CL_TXT + ']: ' + CL_E)
			if user:
				load_it = True
				user2 = raw_input(CL_INF + 'Delete? [' + CL_DEF + 'no' + CL_INF + ']: ' + CL_E)
				if user2:
					if user2 == 'y' or user2 == 'yes':
						os.rename( project_files[int(user)], project_files[int(user)].replace(path_to_project + '/projects/', path_to_project + '/projects/_') )
						load_it = False
				if load_it:
					Entries = Entries_Class()
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
					if len(Loader) > 11:
						Entries.project_company = Loader[11]
					if len(Loader) > 12:
						Entries.fixed = Loader[12]
					loaded_project = project_names[int(user)]
		else:
			print CL_INF + 'No projects exists.' + CL_E
			print
	else:
		print CL_INF + 'No projects exists.' + CL_E
		print


def Loader_New():
	global loaded_project, Entries

	if os.path.isdir(path_to_project + '/projects'):
		all_in_dir = os.listdir(path_to_project + '/projects')
		project_files = []
		project_names = []
		for x in all_in_dir:
			if '.preis_t' in x and not x[0:1] == '_':
				project_files.append( path_to_project + '/projects/' + x )
				project_names.append( x.replace('.preis_t', '').replace('_', ' ') )
		project_files = sorted(project_files)
		project_names = sorted(project_names)
		if len(project_files) > 0:
			print CL_TXT + 'Projects:' + CL_E
			print
			for y, x in enumerate(project_names):
				print CL_TXT + '(' + str(y) + ') ' + x + CL_E
			print
			user = raw_input(CL_TXT + 'Chose project [' + CL_DEF + 'none' + CL_TXT + ']: ' + CL_E)
			if user:
				load_it = True
				user2 = raw_input(CL_INF + 'Delete? [' + CL_DEF + 'no' + CL_INF + ']: ' + CL_E)
				if user2:
					if user2 == 'y' or user2 == 'yes':
						os.rename( project_files[int(user)], project_files[int(user)].replace(path_to_project + '/projects/', path_to_project + '/projects/_') )
						load_it = False

				if load_it:
					Entries = Entries_Class()

					f = open(project_files[int(user)], 'r')
					loaded_content = f.read().splitlines()
					f.close()

					loaded_project = []
					loaded_entries = []
					loaded_mods = []
					loaded_fixed = []
					for y, x in enumerate(loaded_content):
						if x == '[PROJECT]':
							load_project_start = y+1
						elif x == '[ENTRIES]':
							load_project_end = y
							load_entries_start = y+1
						elif x == '[MODIFIER]':
							load_entries_end = y
							load_mods_start = y+1
						elif x == '[FIXED]':
							load_mods_end = y
							load_fixed_start = y+1
						elif x == '[END]':
							load_fixed_end = y

					loaded_project.extend( loaded_content[ load_project_start : load_project_end ] )
					loaded_entries.extend( loaded_content[ load_entries_start : load_entries_end ] )
					loaded_mods.extend( loaded_content[ load_mods_start : load_mods_end ] )
					loaded_fixed.extend( loaded_content[ load_fixed_start : load_fixed_end ] )


					# load project settings
					# company, client title, name, address, city, project name, offer filename, round, commodity, wage
					if len(loaded_project) > 0:
						Entries.project_company = loaded_project[0]
					if len(loaded_project) > 1:
						Entries.project_client_title = loaded_project[1]
					if len(loaded_project) > 2:
						Entries.project_client_name = loaded_project[2]
					if len(loaded_project) > 3:
						Entries.project_client_address = loaded_project[3]
					if len(loaded_project) > 4:
						Entries.project_client_city = loaded_project[4]
					if len(loaded_project) > 5:
						Entries.project_name = loaded_project[5]
					if len(loaded_project) > 6:
						Entries.project_offer_filename = loaded_project[6]
					if len(loaded_project) > 7:
						Entries.project_round = str2bool(loaded_project[7])
					if len(loaded_project) > 8:
						Entries.project_commodity = loaded_project[8]
					if len(loaded_project) > 9:
						try:
							Entries.Wage = float(loaded_project[9])
						except Exception, e:
							pass

					# load entries
					for x in loaded_entries:
						Entries.list.append( Single_Entry_Class(order=Entries.count()) )
						y = x.split('´')
						if len(y) > 0:
							Entries.list[ len( Entries.list ) - 1 ].title = y[0]
						if len(y) > 1:
							Entries.list[ len( Entries.list ) - 1 ].comment = y[1]
						if len(y) > 2:
							try:
								Entries.list[ len( Entries.list ) - 1 ].h = float(y[2])
							except Exception, e:
								pass
						if len(y) > 3:
							try:
								Entries.list[ len( Entries.list ) - 1 ].amount = float(y[3])
							except Exception, e:
								pass
						if len(y) > 4:
							Entries.list[ len( Entries.list ) - 1 ].id = y[4]
						if len(y) > 5:
							try:
								Entries.list[ len( Entries.list ) - 1 ].order = int(y[5])
							except Exception, e:
								pass

					# load modifier
					for x in loaded_mods:
						Entries.mods.append( Single_Mod_Class(order=Entries.count()) )
						y = x.split('´')
						if len(y) > 0:
							Entries.mods[ len( Entries.mods ) - 1 ].title = y[0]
						if len(y) > 1:
							Entries.mods[ len( Entries.mods ) - 1 ].comment = y[1]
						if len(y) > 2:
							try:
								Entries.mods[ len( Entries.mods ) - 1 ].multi = float(y[2])
							except Exception, e:
								pass
						if len(y) > 3:
							try:
								Entries.mods[ len( Entries.mods ) - 1 ].time = float(y[3])
							except Exception, e:
								pass
						if len(y) > 4:
							try:
								Entries.mods[ len( Entries.mods ) - 1 ].amount = float(y[4])
							except Exception, e:
								pass
						if len(y) > 5:
							try:
								Entries.mods[ len( Entries.mods ) - 1 ].entries = eval(y[5])
							except Exception, e:
								pass
						if len(y) > 6:
							Entries.mods[ len( Entries.mods ) - 1 ].id = y[6]
						if len(y) > 7:
							try:
								Entries.mods[ len( Entries.mods ) - 1 ].order = int(y[7])
							except Exception, e:
								pass

					# load fixed
					for x in loaded_fixed:
						Entries.fixed.append( Single_Fixed_Class(order=Entries.count()) )
						y = x.split('´')
						if len(y) > 0:
							Entries.fixed[ len( Entries.fixed ) - 1 ].title = y[0]
						if len(y) > 1:
							Entries.fixed[ len( Entries.fixed ) - 1 ].comment = y[1]
						if len(y) > 2:
							try:
								Entries.fixed[ len( Entries.fixed ) - 1 ].time = float(y[2])
							except Exception, e:
								pass
						if len(y) > 3:
							try:
								Entries.fixed[ len( Entries.fixed ) - 1 ].price = float(y[3])
							except Exception, e:
								pass
						if len(y) > 4:
							try:
								Entries.fixed[ len( Entries.fixed ) - 1 ].amount = float(y[4])
							except Exception, e:
								pass
						if len(y) > 5:
							Entries.fixed[ len( Entries.fixed ) - 1 ].id = y[5]
						if len(y) > 6:
							try:
								Entries.fixed[ len( Entries.fixed ) - 1 ].order = int(y[6])
							except Exception, e:
								pass

					loaded_project = project_names[int(user)]

		else:
			print CL_INF + 'No projects exists.' + CL_E
			print
	else:
		print CL_INF + 'No projects exists.' + CL_E
		print


def Saver_New(obj):
	global loaded_project

	user = raw_input( CL_TXT + 'Project name or \'.\' to cancel (g=generate) [' + CL_DEF + loaded_project + CL_TXT + ']: ' + CL_E)
	if user == 'g':
		gen_company_name = (obj.project_company + ' ') if obj.project_company else ''
		gen_date = datetime.datetime.now().strftime('%Y-%m-%d ')
		gen_project_name = obj.project_name
		gen_filename = gen_company_name + gen_date + gen_project_name
		user = raw_input( CL_TXT + 'Project name \'.\' to cancel [' + CL_DEF + gen_filename + CL_TXT + ']: ' + CL_E)
		if not user:
			user = gen_filename
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
			save_output = ''

			# save project settings
			# company, client title, name, address, city, project name, offer filename, round, commodity, wage
			save_output += '[PROJECT]\n'
			save_output += obj.project_company + '\n'
			save_output += obj.project_client_title + '\n'
			save_output += obj.project_client_name + '\n'
			save_output += obj.project_client_address + '\n'
			save_output += obj.project_client_city + '\n'
			save_output += obj.project_name + '\n'
			save_output += obj.project_offer_filename + '\n'
			save_output += str(obj.project_round) + '\n'
			save_output += obj.project_commodity + '\n'
			save_output += str(obj.Wage) + '\n'

			# save list
			save_output += '[ENTRIES]\n'
			for x in obj.list:
				save_output += x.title + '´'
				save_output += x.comment + '´'
				save_output += str(x.h) + '´'
				save_output += str(x.amount) + '´'
				save_output += x.id + '´'
				save_output += str(x.order) + '\n'

			# save mods
			save_output += '[MODIFIER]\n'
			for x in obj.mods:
				save_output += x.title + '´'
				save_output += x.comment + '´'
				save_output += str(x.multi) + '´'
				save_output += str(x.time) + '´'
				save_output += str(x.amount) + '´'
				save_output += str(x.entries) + '´'
				save_output += x.id + '´'
				save_output += str(x.order) + '\n'

			# save fixed
			save_output += '[FIXED]\n'
			for x in obj.fixed:
				save_output += x.title + '´'
				save_output += x.comment + '´'
				save_output += str(x.time) + '´'
				save_output += str(x.price) + '´'
				save_output += str(x.amount) + '´'
				save_output += x.id + '´'
				save_output += str(x.order) + '\n'

			# end of save file
			save_output += '[END]'

			f = open(file_name, 'w')
			f.write(save_output)
			f.close()

			loaded_project = loaded_project_tmp


def SaveObject(obj, file):
	with open(file, 'wb') as f:
		pickle.dump(obj, f)


def Saver(obj):
	global loaded_project

	user = raw_input( CL_TXT + 'Project name or \'.\' to cancel (g=generate) [' + CL_DEF + loaded_project + CL_TXT + ']: ' + CL_E)
	if user == 'g':
		gen_company_name = (obj.project_company + ' ') if obj.project_company else ''
		gen_date = datetime.datetime.now().strftime('%Y-%m-%d ')
		gen_project_name = obj.project_name
		gen_filename = gen_company_name + gen_date + gen_project_name
		user = raw_input( CL_TXT + 'Project name \'.\' to cancel [' + CL_DEF + gen_filename + CL_TXT + ']: ' + CL_E)
		if not user:
			user = gen_filename
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
			Saver.append( obj.project_company )
			Saver.append( obj.fixed )
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
		if what == 'fix':
			title_tmp = raw_input(CL_TXT + 'Title [' + CL_DEF + title + CL_TXT + ']: ' + CL_E)
			if title_tmp:
				title = title_tmp
			comment_tmp = raw_input(CL_TXT + 'Comment [' + CL_DEF + comment + CL_TXT + ']: ' + CL_E)
			if comment_tmp:
				comment = comment_tmp
			amount = raw_input(CL_TXT + 'Amount [' + CL_DEF + '1' + CL_TXT + ']: ' + CL_E)
			try:
				amount = float(amount.replace(',', '.')) or 1.0
			except Exception, e:
				amount = 1.0
			Entries.add(what='fix', title=title, h=float(preset['h']), price=float(preset['p']), amount=amount, comment=comment, order=Entries.count())
		elif what == 'entry':
			title_tmp = raw_input(CL_TXT + 'Title [' + CL_DEF + title + CL_TXT + ']: ' + CL_E)
			if title_tmp:
				title = title_tmp
			comment_tmp = raw_input(CL_TXT + 'Comment [' + CL_DEF + comment + CL_TXT + ']: ' + CL_E)
			if comment_tmp:
				comment = comment_tmp
			amount = raw_input(CL_TXT + 'Amount [' + CL_DEF + '1' + CL_TXT + ']: ' + CL_E)
			try:
				amount = float(amount.replace(',', '.')) or 1.0
			except Exception, e:
				amount = 1.0
			Entries.add(what='entry', title=title, h=float(preset['h']), amount=amount, comment=comment, order=Entries.count())
		elif what == 'mod':
			title_tmp = raw_input(CL_TXT + 'Title [' + CL_DEF + title + CL_TXT + ']: ' + CL_E)
			if title_tmp:
				title = title_tmp
			comment_tmp = raw_input(CL_TXT + 'Comment [' + CL_DEF + comment + CL_TXT + ']: ' + CL_E)
			if comment_tmp:
				comment = comment_tmp
			amount = raw_input(CL_TXT + 'Amount [' + CL_DEF + '1' + CL_TXT + ']: ' + CL_E)
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
			Entries.add(what='mod', title=title, multi=float(preset['h']), time=bool(preset['t']), entries=entries, comment=comment, amount=amount, order=Entries.count())
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
			if preset[c[chose]].has_key('c'):
				tmp_comment = preset[c[chose]]['c']
			else:
				tmp_comment = ''
			preset_choser(what, preset[c[chose]], next_title_pre + c[chose], tmp_comment)


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
		self.project_company = def_project_company
		self.project_client_title = def_project_client_title
		self.project_client_name = def_project_client_name
		self.project_client_address = def_project_client_address
		self.project_client_city = def_project_client_city
		self.project_name = def_project_name
		self.project_offer_filename = def_project_offer_filename
		self.project_round = True
		self.project_commodity = def_commodity
		self.Wage = 40
		self.Wage_Pro = 40
		self.Wage_Edu = 33
		self.Wage_Low = 25
		self.list = []
		self.mods = []
		self.fixed = []

	def count(self):
		return len(self.fixed) + len(self.list) + len(self.mods)

	def is_this_type(self, what='fixed', where=0):
		if what == 'fixed':
			for y, x in enumerate(self.fixed):
				if x.order == where:
					return (True, y)

		elif what == 'entry':
			for y, x in enumerate(self.list):
				if x.order == where:
					return (True, y)

		elif what == 'mod':
			for y, x in enumerate(self.mods):
				if x.order == where:
					return (True, y)

		return (False, 0)

	def switch_order(self, from_order, to_order):
		from_fixed = self.is_this_type('fixed', from_order)
		from_entry = self.is_this_type('entry', from_order)
		from_mod   = self.is_this_type('mod', from_order)
		to_fixed = self.is_this_type('fixed', to_order)
		to_entry = self.is_this_type('entry', to_order)
		to_mod   = self.is_this_type('mod', to_order)

		if from_fixed[0]:
			self.fixed[from_fixed[1]].order = to_order
		elif from_entry[0]:
			self.list[from_entry[1]].order = to_order
		elif from_mod[0]:
			self.mods[from_mod[1]].order = to_order

		if to_fixed[0]:
			self.fixed[to_fixed[1]].order = from_order
		elif to_entry[0]:
			self.list[to_entry[1]].order = from_order
		elif to_mod[0]:
			self.mods[to_mod[1]].order = from_order

	def reorder(self, from_order, to_order):
		if from_order == to_order:
			return
		elif from_order < to_order:
			start_order = from_order
			while not start_order == to_order:
				self.switch_order(start_order, start_order+1)
				start_order += 1
		elif from_order > to_order:
			start_order = from_order
			while not start_order == to_order:
				self.switch_order(start_order, start_order-1)
				start_order -= 1

	def delete_it(self, delete):
		is_fixed = self.is_this_type('fixed', delete)
		is_entry = self.is_this_type('entry', delete)
		is_mod   = self.is_this_type('mod', delete)

		if delete == self.count()-1:
			if is_fixed[0]:
				self.fixed.pop(is_fixed[1])
			elif is_entry[0]:
				self.list.pop(is_entry[1])
			elif is_mod[0]:
				self.mods.pop(is_mod[1])
		else:
			self.reorder(delete, self.count()-1)
			self.delete_it(self.count()-1)

	def edit(self, which):
		if type(which) is int:

			is_fixed = self.is_this_type('fixed', which)
			is_entry = self.is_this_type('entry', which)
			is_mod   = self.is_this_type('mod', which)

			# it's a fixed
			if is_fixed[0]:
				old_which = which
				which = is_fixed[1]

				delete = raw_input(CL_TXT + 'Delete [' + CL_DEF + 'no' + CL_TXT + ']: ' + CL_E)
				if delete == 'yes' or delete == 'y':
					#self.fixed.pop(which)
					self.delete_it(old_which)
					return

				order = raw_input(CL_TXT + 'Order [' + CL_DEF + str(old_which) + CL_TXT + ']: ' + CL_E)
				if order:
					try:
						order = int(order)
						self.reorder(old_which, order)
					except Exception, e:
						print CL_INF + 'Order not changed. Need integer.' + CL_E

				title = raw_input(CL_TXT + 'Title [' + CL_DEF + self.fixed[which].title + CL_TXT + ']: ' + CL_E)
				title = title or self.fixed[which].title
				self.fixed[which].title = title

				comment = raw_input(CL_TXT + 'Comment [' + CL_DEF + self.fixed[which].comment + CL_TXT + ']: ' + CL_E)
				comment = comment or self.fixed[which].comment
				self.fixed[which].comment = comment

				time = raw_input(CL_TXT + 'Time (0=is no time) [' + CL_DEF + str(self.fixed[which].time) + CL_TXT + ']: ' + CL_E)
				try:
					time = float(time.replace(',', '.'))
				except Exception, e:
					time = self.fixed[which].time
				self.fixed[which].time = time

				price = raw_input(CL_TXT + 'Price [' + CL_DEF + str(self.fixed[which].price) + CL_TXT + ']: ' + CL_E)
				try:
					price = float(price.replace(',', '.'))
				except Exception, e:
					price = self.fixed[which].price
				self.fixed[which].price = price

				amount = raw_input(CL_TXT + 'Amount [' + CL_DEF + str(self.fixed[which].amount) + CL_TXT + ']: ' + CL_E)
				try:
					amount = float(amount.replace(',', '.'))
				except Exception, e:
					amount = self.fixed[which].amount
				self.fixed[which].amount = amount

			# it's an entry
			elif is_entry[0]:
				old_which = which
				which = is_entry[1]

				delete = raw_input(CL_TXT + 'Delete [' + CL_DEF + 'no' + CL_TXT + ']: ' + CL_E)
				if delete == 'yes' or delete == 'y':
					#self.list.pop(which)
					self.delete_it(old_which)
					return

				order = raw_input(CL_TXT + 'Order [' + CL_DEF + str(old_which) + CL_TXT + ']: ' + CL_E)
				if order:
					try:
						order = int(order)
						self.reorder(old_which, order)
					except Exception, e:
						print CL_INF + 'Order not changed. Need integer.' + CL_E

				title = raw_input(CL_TXT + 'Title [' + CL_DEF + self.list[which].title + CL_TXT + ']: ' + CL_E)
				title = title or self.list[which].title
				self.list[which].title = title

				comment = raw_input(CL_TXT + 'Comment [' + CL_DEF + self.list[which].comment + CL_TXT + ']: ' + CL_E)
				comment = comment or self.list[which].comment
				self.list[which].comment = comment

				h = raw_input(CL_TXT + 'H / Amount [' + CL_DEF + str(self.list[which].h) + CL_TXT + ']: ' + CL_E)
				if h == 'e':
					h = self.hCalc()
				else:
					try:
						h = float(h.replace(',', '.'))
					except Exception, e:
						h = self.list[which].h
				self.list[which].h = h

				amount = raw_input(CL_TXT + 'Amount [' + CL_DEF + str(self.list[which].amount) + CL_TXT + ']: ' + CL_E)
				try:
					amount = float(amount.replace(',', '.'))
				except Exception, e:
					amount = self.list[which].amount
				self.list[which].amount = amount

			# it's a modulator
			elif is_mod[0]:
				old_which = which
				which = is_mod[1]

				delete = raw_input(CL_TXT + 'Delete [' + CL_DEF + 'no' + CL_TXT + ']: ' + CL_E)
				if delete == 'yes' or delete == 'y':
					#self.mods.pop(which)
					self.delete_it(old_which)
					return

				order = raw_input(CL_TXT + 'Order [' + CL_DEF + str(old_which) + CL_TXT + ']: ' + CL_E)
				if order:
					try:
						order = int(order)
						self.reorder(old_which, order)
					except Exception, e:
						print CL_INF + 'Order not changed. Need integer.' + CL_E

				title = raw_input(CL_TXT + 'Title ['  + CL_DEF + self.mods[which].title + CL_TXT + ']: ' + CL_E)
				title = title or self.mods[which].title
				self.mods[which].title = title

				comment = raw_input(CL_TXT + 'Comment ['  + CL_DEF + self.mods[which].comment + CL_TXT + ']: ' + CL_E)
				comment = comment or self.mods[which].comment
				self.mods[which].comment = comment

				multi = raw_input(CL_TXT + 'Multiplicator [' + CL_DEF + str(self.mods[which].multi) + CL_TXT + ']: ' + CL_E)
				try:
					multi = float(multi.replace(',', '.'))
				except Exception, e:
					multi = self.mods[which].multi
				self.mods[which].multi = multi

				amount = raw_input(CL_TXT + 'Amount [' + CL_DEF + str(self.mods[which].amount) + CL_TXT + ']: ' + CL_E)
				try:
					amount = float(amount.replace(',', '.'))
				except Exception, e:
					amount = self.mods[which].amount
				self.mods[which].amount = amount

				entries = raw_input(CL_TXT + 'Entries [' + CL_DEF + self.entries_to_index(self.mods[which].entries) + CL_TXT + ']: ' + CL_E)
				if entries:
					try:
						entries = tuple(entries.split(','))
					except Exception, e:
						entries = ()
					entries = self.index_to_entries(entries)
				else:
					entries = self.mods[which].entries
				self.mods[which].entries = entries

				time = raw_input(CL_TXT + 'Time [' + CL_DEF + self.mods[which].getTime_status() + CL_TXT + ']: ' + CL_E)
				if time:
					if time.lower() == 'y' or time.lower() == 'yes':
						time = True
					else:
						time = False
				else:
					time = self.mods[which].time
				self.mods[which].time = time

	def add(self, what='entry', title='Music', h=1.6, amount=1.0, multi=0.2, entries=[], time=True, comment='', price=0.0, order=0):
		if what == 'entry':
			self.list.append( Single_Entry_Class(title=title, h=h, amount=amount, comment=comment, order=order) )
		elif what == 'mod':
			self.mods.append( Single_Mod_Class(title=title, multi=multi, entries=entries, time=time, comment=comment, amount=amount, order=order) )
		elif what == 'fix':
			self.fixed.append( Single_Fixed_Class(title=title, time=h, comment=comment, amount=amount, price=price, order=order) )

	def hCalc(self):
		h_unit = raw_input(CL_TXT + '-- H / unit [' + CL_DEF + '0.4' + CL_TXT + ']: ' + CL_E)
		try:
			h_unit = float(h_unit.replace(',', '.'))
		except Exception, e:
			h_unit = 0.4
		units = raw_input(CL_TXT + '-- units [' + CL_DEF + '1' + CL_TXT + ']: ' + CL_E)
		try:
			unit = float(unit.replace(',', '.'))
		except Exception, e:
			unit = 1.0
		out = h_unit * units
		print CL_TXT + '-- H / Amount : ' + CL_DEF + str(out) + CL_E
		return out

	def add_edit(self, what):
		if what == 'fix':
			title = raw_input(CL_TXT + 'Title [' + CL_DEF + 'Baseprice' + CL_TXT + ']: ' + CL_E)
			title = title or 'Baseprice'

			comment = raw_input(CL_TXT + 'Comment []: ' + CL_E)

			time = raw_input(CL_TXT + 'Time (0=is no time) []: ' + CL_E)
			try:
				time = float(time.replace(',', '.'))
			except Exception, e:
				time = 0

			price = raw_input(CL_TXT + 'Price [' + CL_DEF + '0.0' + CL_TXT + ']: ' + CL_E)
			try:
				price = float(price.replace(',', '.'))
			except Exception, e:
				price = 0.0

			amount = raw_input(CL_TXT + 'Amount [' + CL_DEF + '1' + CL_TXT + ']: ' + CL_E)
			try:
				amount = float(amount.replace(',', '.'))
			except Exception, e:
				amount = 1.0

			self.add(what=what, title=title, h=time, amount=amount, comment=comment, price=price, order=self.count())

		elif what == 'entry':
			title = raw_input(CL_TXT + 'Title [' + CL_DEF + 'Music' + CL_TXT + ']: ' + CL_E)
			title = title or 'Music'

			comment = raw_input(CL_TXT + 'Comment []: ' + CL_E)

			h = raw_input(CL_TXT + 'H / Amount [' + CL_DEF + '1.6' + CL_TXT + ']: ' + CL_E)
			if h == 'e':
				h = self.hCalc()
			else:
				try:
					h = float(h.replace(',', '.'))
				except Exception, e:
					h = 1.6

			amount = raw_input(CL_TXT + 'Amount [' + CL_DEF + '1' + CL_TXT + ']: ' + CL_E)
			try:
				amount = float(amount.replace(',', '.'))
			except Exception, e:
				amount = 1.0

			self.add(what=what, title=title, h=h, amount=amount, comment=comment, order=self.count())

		elif what == 'mod':
			title = raw_input(CL_TXT + 'Title [' + CL_DEF + 'Exclusive' + CL_TXT + ']: ' + CL_E)
			title = title or 'Exclusive'

			comment = raw_input(CL_TXT + 'Comment []: ' + CL_E)

			multi = raw_input(CL_TXT + 'Multiplicator [' + CL_DEF + '3.0' + CL_TXT + ']: ' + CL_E)
			try:
				multi = float(multi.replace(',', '.'))
			except Exception, e:
				multi = 3

			amount = raw_input(CL_TXT + 'Amount [' + CL_DEF + '1' + CL_TXT + ']: ' + CL_E)
			try:
				amount = float(amount.replace(',', '.'))
			except Exception, e:
				amount = 1.0

			entries = raw_input(CL_TXT + 'Entries []: ' + CL_E)
			if entries:
				try:
					entries = tuple(entries.split(','))
				except Exception, e:
					entries = ()
				entries = self.index_to_entries(entries)
			else:
				entries = []

			time = raw_input(CL_TXT + 'Time [' + CL_DEF + 'no' + CL_TXT + ']: ' + CL_E)
			if time:
				if time.lower() == 'y' or time.lower() == 'yes':
					time = True
				else:
					time = False
			else:
				time = False

			self.add(what=what, title=title, multi=multi, entries=entries, time=time, comment=comment, amount=amount, order=self.count())

	def index_to_entries(self, entries):
		out = []
		for x in entries:
			is_fixed = self.is_this_type('fixed', int(x))
			is_entry = self.is_this_type('entry', int(x))
			is_mod   = self.is_this_type('mod', int(x))

			if is_fixed[0]:
				out.append( self.fixed[ is_fixed[1] ].id )
			elif is_entry[0]:
				out.append( self.list[ is_entry[1] ].id )
			elif is_mod[0]:
				out.append( self.mods[ is_mod[1] ].id )
		return out

	def entries_to_index(self, entries):
		out = ''
		for y, x in enumerate(self.fixed):
			if x.id in entries:
				if out == '':
					out = str(self.fixed[y].order)
				else:
					out = out + ', ' + str(self.fixed[y].order)
		for y, x in enumerate(self.list):
			if x.id in entries:
				if out == '':
					out = str(self.list[y].order)
				else:
					out = out + ', ' + str(self.list[y].order)
		for y, x in enumerate(self.mods):
			if x.id in entries:
				if out == '':
					out = str(self.mods[y].order)
				else:
					out = out + ', ' + str(self.mods[y].order)
		return out

	def sum(self, round_it=False):
		out_h = 0
		out_p = 0
		for x in self.fixed:
			out_h += x.time
			out_p += x.getPrice()
		for x in self.list:
			out_h += x.getTime()
			out_p += x.getPrice(self.Wage, round_it)
		for x in self.mods:
			out_h += x.getTime(self.fixed, self.list, self.mods)
			out_p += x.getPrice(self.Wage, self.fixed, self.list, self.mods, round_it)
		return [out_h, out_p]

	def return_time(self, floaty):
		hours = int(floaty)
		minutes = int( (floaty - hours) * 60 )
		hours = str(hours) if hours > 9 else '0' + str(hours)
		minutes = str(minutes) if minutes > 9 else '0' + str(minutes)
		return hours + ':' + minutes if floaty > 0.0 else '*'

	def show_as_table(self, head=[CL_TXT + 'ID' + CL_E, CL_TXT + 'Title' + CL_E, CL_TXT + 'Amount' + CL_E, CL_TXT + 'H' + CL_E, CL_TXT + 'Price']):
		show = []

		i = 0
		for x in xrange(0,self.count()):
			is_fixed = self.is_this_type('fixed', x)
			is_entry = self.is_this_type('entry', x)
			is_mod   = self.is_this_type('mod', x)

			if is_fixed[0]:
				show.append( [CL_OUT + str(x) + CL_E, CL_OUT + unicode(self.fixed[ is_fixed[1] ].title, 'utf-8') + CL_E, CL_OUT + str(self.fixed[ is_fixed[1] ].amount) + CL_E, CL_OUT + str(self.return_time( self.fixed[ is_fixed[1] ].time )) + CL_E, CL_OUT + str(self.fixed[ is_fixed[1] ].getPrice()) + CL_E] )
			elif is_entry[0]:
				show.append( [CL_OUT + str(x) + CL_E, CL_OUT + unicode(self.list[ is_entry[1] ].title, 'utf-8') + CL_E, CL_OUT + str(self.list[ is_entry[1] ].amount) + CL_E, CL_OUT + str(self.return_time( self.list[ is_entry[1] ].getTime() )) + CL_E, CL_OUT + str(self.list[ is_entry[1] ].getPrice(self.Wage)) + CL_E] )
			elif is_mod[0]:
				show.append( [CL_OUT + str(x) + CL_E, CL_OUT + unicode(self.mods[ is_mod[1] ].title, 'utf-8') + CL_E, CL_OUT + str(self.mods[ is_mod[1] ].amount) + ' *' + CL_E, CL_OUT + str(self.return_time( self.mods[ is_mod[1] ].getTime(self.fixed, self.list, self.mods) )) + CL_E, CL_OUT + str(self.mods[ is_mod[1] ].getPrice(self.Wage, self.fixed, self.list, self.mods)) + CL_E] )

		if not small_table:
			show.append( [CL_TXT + 'f' + CL_E, CL_TXT + '[New fixed]' + CL_E, CL_TXT + '...' + CL_E, CL_TXT + '?' + CL_E, CL_TXT + '?' + CL_E] )
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

		user = raw_input(CL_TXT + 'Company name [' + CL_DEF + self.project_company + CL_TXT + ']: ' + CL_E)
		if user:
			if user == '-':
				self.project_company = ''
			else:
				self.project_company = user

		user = raw_input(CL_TXT + 'Client title [' + CL_DEF + self.project_client_title + CL_TXT + ']: ' + CL_E)
		if user:
			self.project_client_title = user

		user = raw_input(CL_TXT + 'Client name [' + CL_DEF + self.project_client_name + CL_TXT + ']: ' + CL_E)
		if user:
			self.project_client_name = user

		user = raw_input(CL_TXT + 'Client address [' + CL_DEF + self.project_client_address + CL_TXT + ']: ' + CL_E)
		if user:
			self.project_client_address = user

		user = raw_input(CL_TXT + 'Client city [' + CL_DEF + self.project_client_city + CL_TXT + ']: ' + CL_E)
		if user:
			self.project_client_city = user

		user = raw_input(CL_TXT + 'Project name [' + CL_DEF + self.project_name + CL_TXT + ']: ' + CL_E)
		if user:
			self.project_name = user
			loaded_project = user


		self.project_offer_filename = self.project_offer_filename.replace('{YEAR}', datetime.datetime.now().strftime('%Y')).replace('{PROJECT_NAME}', self.project_name.replace(' ', '_'))
		def_choice = False
		user = raw_input(CL_TXT + 'Offer output file (g=generate) [' + CL_DEF + self.project_offer_filename + CL_TXT + ']: ' + CL_E)
		if user == 'g':
			def_generated_filename = def_project_offer_filename.replace('{YEAR}', datetime.datetime.now().strftime('%Y')).replace('{PROJECT_NAME}', self.project_name.replace(' ', '_'))
			user2 = raw_input(CL_TXT + 'Offer output file [' + CL_DEF + def_generated_filename + CL_TXT + ']: ' + CL_E)
			if user2 and check_file_exists(user2):
				self.project_offer_filename = user2
			else:
				self.project_offer_filename = def_generated_filename
		else:
			if user and check_file_exists(user):
				self.project_offer_filename = user

		tmp_round = 'yes' if self.project_round else 'no'
		user = raw_input(CL_TXT + 'Round exported output? [' + CL_DEF + tmp_round + CL_TXT + ']: ' + CL_E)
		if user:
			if user == 'y' or user == 'yes':
				self.project_round = True
			else:
				self.project_round = False

		user = raw_input(CL_TXT + 'Commodity [' + CL_DEF + self.project_commodity + CL_TXT + ']:' + CL_E)
		if user:
			self.project_commodity = user

		print

	def export_to_odt(self):
		if secretary_available:
			self.project_offer_filename = self.project_offer_filename.replace('{YEAR}', datetime.datetime.now().strftime('%Y')).replace('{PROJECT_NAME}', self.project_name.replace(' ', '_'))
			user = raw_input(CL_TXT + 'Filename for export [' + CL_DEF + self.project_offer_filename + CL_TXT + ']: ' + CL_E)
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
					for x in xrange(0,self.count()):
						is_fixed = self.is_this_type('fixed', x)
						is_entry = self.is_this_type('entry', x)
						is_mod   = self.is_this_type('mod', x)

						if is_fixed[0]:
							entries.append( [unicode(self.fixed[ is_fixed[1] ].title, 'utf-8'), unicode(str(self.fixed[ is_fixed[1] ].amount).replace('.', decimal).replace(',0', ''), 'utf-8'), unicode(str(self.fixed[ is_fixed[1] ].getPrice()).replace('.', decimal).replace(',0', '') + ' ' + self.project_commodity, 'utf-8'), unicode(self.fixed[ is_fixed[1] ].comment or '-', 'utf-8') ] )
						elif is_entry[0]:
							entries.append( [unicode(self.list[ is_entry[1] ].title, 'utf-8'), unicode(str(self.list[ is_entry[1] ].amount).replace('.', decimal).replace(',0', ''), 'utf-8'), unicode(str(self.list[ is_entry[1] ].getPrice(self.Wage, self.project_round)).replace('.', decimal).replace(',0', '') + ' ' + self.project_commodity, 'utf-8'), unicode(self.list[ is_entry[1] ].comment or '-', 'utf-8') ] )
						elif is_mod[0]:
							entries.append( [unicode(self.mods[ is_mod[1] ].title, 'utf-8'), unicode(str(self.mods[ is_mod[1] ].amount).replace('.', decimal).replace(',0', ''), 'utf-8'), unicode(str(self.mods[ is_mod[1] ].getPrice(self.Wage, self.fixed, self.list, self.mods, self.project_round)).replace('.', decimal).replace(',0', '') + ' ' + self.project_commodity, 'utf-8'), unicode(self.mods[ is_mod[1] ].comment or '-', 'utf-8') ] )


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
	def __init__(self, title='Music', h=1.6, amount=1, comment='', order=0):
		self.title = title
		self.comment = comment
		self.h = h
		self.amount = amount
		self.id = str(uuid.uuid1())
		self.order = order

	def getTime(self):
		return round(self.amount * self.h, 2)

	def getPrice(self, wage, round_it=False):
		if round_it:
			return int(round(self.getTime() * wage))
		else:
			return round(self.getTime() * wage, 2)


class Single_Mod_Class(object):
	def __init__(self, title='Exclusive', multi=3, time=False, entries=[], comment='', amount=1, order=0):
		self.title = title
		self.comment = comment
		self.multi = multi
		self.time = time
		self.amount = amount
		self.entries = entries
		self.id = str(uuid.uuid1())
		self.order = order

	def getTime_status(self):
		if not self.time:
			return 'no'
		else:
			return 'yes'

	def has_entry(self, list_entry):
		is_not_in_others_entries = True
		if type(list_entry) == Single_Mod_Class:
			is_not_in_others_entries = not self.id in list_entry.entries
		if list_entry.id in self.entries and not list_entry.id == self.id and is_not_in_others_entries:
			return True
		else:
			return False

	def getTime(self, list_fixed, list_entry, list_mod):
		out = 0.0
		for x in list_fixed:
			if self.has_entry(x) and self.time:
				out += x.getTime() * self.multi * self.amount
		for x in list_entry:
			if self.has_entry(x) and self.time:
				out += x.getTime() * self.multi * self.amount
		for x in list_mod:
			if self.has_entry(x) and self.time:
				out += x.getTime(list_fixed, list_entry, list_mod) * self.multi * self.amount
		return round(out, 2)

	def getPrice(self, wage, list_fixed, list_entry, list_mod, round_it=False):
		out = 0.0
		for x in list_fixed:
			if self.has_entry(x):
				out += x.getPrice(wage) * self.multi * self.amount
		for x in list_entry:
			if self.has_entry(x):
				out += x.getPrice(wage) * self.multi * self.amount
		for x in list_mod:
			if self.has_entry(x):
				out += x.getPrice(wage, list_fixed, list_entry, list_mod, round_it) * self.multi * self.amount

		if round_it:
			return int(round(out))
		else:
			return round(out, 2)


class Single_Fixed_Class(object):
	def __init__(self, title='Baseprice', comment='', time=0, price=0.0, amount=1.0, order=0):
		self.title = title
		self.comment = comment
		self.time = time
		self.price = price
		self.amount = amount
		self.id = str(uuid.uuid1())
		self.order = order

	def getTime(self):
		return self.time

	def getPrice(self, *arg):
		return self.amount * self.price

	def is_time(self):
		if self.time > 0:
			return True
		else:
			return False






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
			[CL_TXT + 'fix / f' + CL_E, CL_TXT + 'adds a fixed value' + CL_E],
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
	elif user == 'fix' or user == 'f':
		print
		if presets.has_key('F'):
			preset_choser('fix', presets['F'])
		else:
			Entries.add_edit('fix')

	# new  entry
	elif user == 'entry' or user == 'a':
		print
		if presets.has_key('E'):
			preset_choser('entry', presets['E'])
		else:
			Entries.add_edit('entry')

	# new modulator
	elif user == 'mod' or user == 'm':
		print
		if presets.has_key('M'):
			preset_choser('mod', presets['M'])
		else:
			Entries.add_edit('mod')

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
		if old_filetype_save:
			Saver(Entries)
		else:
			Saver_New(Entries)

	# load the project
	elif user == 'load' or user == 'l':
		print
		if old_filetype_load:
			Loader()
		else:
			Loader_New()

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

			# Edit stuff
			if user < Entries.count() and user >= 0:
				print
				Entries.edit(user)

		except Exception, e:
			pass

print