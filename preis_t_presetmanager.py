# coding=utf-8

import os, imp


### ### ###
### ### ### load configurarion file for variables
### ### ###

# !!!!! SET YOUR INDIVIDUAL SETTINGS FILE HERE
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



# functions

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






def preset_choser(preset):
	print
	if preset.has_key('time'):
		print 'DA'
	else:
		i = 0
		c = []
		t = []
		print CL_TXT + '(' + str(i) + ') _New_' + CL_E
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
		if chose == 0 or not chose:
			add_preset(preset)
		else:
			preset_choser(preset[c[chose]])


def project_choser(preset):
	print
	if preset.has_key('task'):
		print 'DA'
	else:
		i = 0
		c = []
		t = []
		print CL_TXT + '(' + str(i) + ') _New_' + CL_E
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
		if chose == 0 or not chose:
			add_project()
		else:
			preset_choser(preset[c[chose]])


def add_preset(preset):
	tmp_preset = preset
	add_preset_recursive(tmp_preset)

	user = raw_input('DEBUG EDIT: ')
	preset = user
	print 'add_preset():', preset

def add_preset_recursive(dic):
	pass


def add_project():
	pass






# presets

presets = {}
if os.path.isfile(path_to_project + '/presets.preis_presets'):
	with open (path_to_project + '/presets.preis_presets', 'r') as myfile:
		presets_file = myfile.read().splitlines()
		pre_presets = []
		for x in presets_file:
			pre_presets.append( x.split('>') )
		myfile.close()

		presets = array_of_paths_to_dict(pre_presets)

projects = {}
if os.path.isfile(path_to_project + '/projects.preis_presets'):
	with open (path_to_project + '/projects.preis_presets', 'r') as myfile:
		presets_file = myfile.read().splitlines()
		pre_presets = []
		for x in presets_file:
			pre_presets.append( x.split('>') )
		myfile.close()

		projects = array_of_paths_to_dict(pre_presets)






# START

print
print CL_INF + 'Preis terminal preset manager' + CL_E
print
user= ''

while user != 'exit' and user != 'e' and user != '.':
	user = raw_input(CL_TXT + '> ' + CL_E)

	# show help
	if user == 'help' or user == 'h' or user == '?':
		print CL_TXT
		print 'help / h / ?\n   this helptext'
		print 'a\n   add/edit presets'
		print 'p\n   add/edit projects'
		print CL_E

	# add/edit presets
	if user == 'a':
		print
		preset_choser(presets)
		print 'from menu:', presets

	# add/edit projects
	elif user == 'p':
		print
		project_choser(projects)