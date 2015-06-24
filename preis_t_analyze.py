import os
import sys
from tabulate import tabulate
import codecs
import datetime


# row settings - fits to the export csv of Gleeo Time Track App for Android
row_project      	= 0
row_task         	= 1
row_details      	= 2
row_start_date   	= 3
row_start_time   	= 4
row_end_date     	= 5
row_end_time     	= 6
row_duration     	= 7
row_duration_dec 	= 8
row_project_xtra1	= 9
row_project_xtra2	= 10
row_task_xtra1   	= 11
row_task_xtra2   	= 12

row_caps = [	'Project',
            	'Task',
            	'Details',
            	'Start date',
            	'Start Time',
            	'End date',
            	'End time',
            	'Duration',
            	'Duration (dec)',
            	'Client',
            	'Project Xtra 2',
            	'Task Xtra 1',
            	'Task Xtra 2']

# getting arguments and loading file

arguments = sys.argv

if len(arguments) <= 1:
	exit()




# functions

def return_time(floaty):
	hours = int(floaty)
	minutes = int( (floaty - hours) * 60 )
	hours = str(hours) if hours > 9 else '0' + str(hours)
	minutes = str(minutes) if minutes > 9 else '0' + str(minutes)
	return hours + ':' + minutes if floaty > 0.0 else '00:00'

def filter_it(array_data):
	# filter contains client, project or task?
	out_str = False
	for x in array_data:
		if x in filt['str'] or len(filt['str']) == 0:
			out_str = True

	# checking date range, default Gleeo Time Tracker export: start-date=3, start-time=4, end-date=5, end-time=6
	out_dat = False
	start = datetime.datetime.strptime(array_data[3] + ' ' + array_data[4], '%Y-%m-%d %H:%M')
	end = datetime.datetime.strptime(array_data[5] + ' ' + array_data[6], '%Y-%m-%d %H:%M')
	if start > filt['from'] and end < filt['to']:
		out_dat = True

	return out_str and out_dat



# classes

class times_class(object):
	def __init__(self, the_file):
		self.var = self.init_variable(the_file)[1:]
		self.filt = {}
		self.filt['clients'] = []
		self.filt['projects'] = []
		self.filt['tasks'] = []
		self.filt['from'] = datetime.datetime(1900, 1, 1)
		self.filt['to'] = datetime.datetime(datetime.MAXYEAR, 12, 31)
		self.filt['year_long'] = False
		self.filt['show_time'] = False

		self.clients = self.getClients()
		self.projects = self.getProjects()
		self.tasks = self.getTasks()


	def init_variable(self, the_file, seperator=','):
		if os.path.isfile(os.getcwd() + '/' + the_file):
			f = codecs.open(os.getcwd() + '/' + the_file, 'r', 'utf-8')
			self.csv_file = f.readlines()
			f.close()
		else:
			print 'No file found, sorry!'
			exit()
		
		if type(self.csv_file) is list:
			out = []
			for x in self.csv_file:
				tmp = x.rstrip().split(seperator)
				if len(tmp) > 1:
					out.append( tmp )
				else:
					print 'File is no CSV or maybe seperater is no \',\'?'
					print 'Ctrl+C for cancelling the program otherwise.'
					new_sep = raw_input('New seperator: ')
					return self.init_variable(self.csv_file, new_sep)
			return out
		else:
			print 'Error with the filetype, sorry.'
			exit()


	def inFilter(self, array):
		out_clients		= False
		out_projects	= False
		out_tasks		= False
		out_from		= False
		out_to  		= False

		# filter contains client, project or task?
		if array[row_project_xtra1] in self.filt['clients'] or len(self.filt['clients']) == 0:
			out_clients = True
		if array[row_project] in self.filt['projects'] or len(self.filt['projects']) == 0:
			out_projects = True
		if array[row_task] in self.filt['tasks'] or len(self.filt['tasks']) == 0:
			out_tasks = True

		# checking date range
		start = datetime.datetime.strptime(array[row_start_date] + ' ' + array[row_start_time], '%Y-%m-%d %H:%M')
		end = datetime.datetime.strptime(array[row_end_date] + ' ' + array[row_end_time], '%Y-%m-%d %H:%M')
		if start > self.filt['from']:
			out_from = True
		if end < self.filt['to']:
			out_to = True

		return out_clients and out_projects and out_tasks and out_from and out_to


	def show_menu(self):
		print
		print '(1) show clients'
		print '(2) show clients with their projects'
		print '(3) show clients with their projects with their tasks'
		print '(4) show projects'
		print '(5) show projects with their tasks'
		print
		user = raw_input('show > ')
		if user == '1':
			self.show('clients')
		elif user == '2':
			self.show('clientsp')
		elif user == '3':
			self.show('clientspt')
		elif user == '4':
			self.show('projects')
		elif user == '5':
			self.show('projectst')


	def getTasks(self, project='*', client='*'):
		out = {}
		for c, x in enumerate(self.var):
			if x[row_task] not in out:
				if (x[row_project] == project or project == '*') and (x[row_project_xtra1] == client or client == '*'):
					out[x[row_task]] = c
		return out

	
	def getProjects(self, client='*'):
		out = {}
		for c, x in enumerate(self.var):
			if x[row_project] not in out:
				if x[row_project_xtra1] == client or client == '*':
					out[x[row_project]] = c
		return out


	def getClients(self):
		out = {}
		for c, x in enumerate(self.var):
			if x[row_project_xtra1] not in out:
				out[x[row_project_xtra1]] = c
		return out
	

	def show(self, what):
		if what == 'clients':
			print
			for c, x in enumerate(sorted(self.clients)):
				print str(c+1) + ': ' + x
		elif what == 'clientsp':
			print
			for c, x in enumerate(sorted(self.clients)):
				print str(c+1) + ': ' + x
				for cc, y in enumerate(sorted(self.getProjects(x))):
					print '   -> ' + str(cc+1) + ': ' + y
		elif what == 'clientspt':
			print
			for c, x in enumerate(sorted(self.clients)):
				print str(c+1) + ': ' + x
				for cc, y in enumerate(sorted(self.getProjects(x))):
					print '   -> ' + str(cc+1) + ': ' + y
					for ccc, z in enumerate(sorted(self.getTasks(y).keys())):
						print '      -> ' + str(ccc+1) + ': ' + z
		elif what == 'projects':
			print
			for c, x in enumerate(sorted(self.projects)):
				print str(c+1) + ': ' + x
		elif what == 'projectst':
			print
			for c, x in enumerate(sorted(self.projects)):
				print str(c+1) + ': ' + x
				for cc, y in enumerate(sorted(self.getTasks(x).keys())):
					print '   -> ' + str(cc+1) + ': ' + y


	def filter_set(self, date):
		if date[0:1] == 's':
			try:
				self.filt['from'] = datetime.datetime.strptime(date[2:], '%Y-%m-%d %H:%M')
			except Exception, e:
				try:
					self.filt['from'] = datetime.datetime.strptime(date[2:], '%Y-%m-%d')
				except Exception, e:
					pass
			if len(date) < 5:
				self.filt['from'] = datetime.datetime(1900, 1, 1)
		elif date[0:1] == 'e':
			try:
				self.filt['to'] = datetime.datetime.strptime(date[2:], '%Y-%m-%d %H:%M')
			except Exception, e:
				try:
					self.filt['to'] = datetime.datetime.strptime(date[2:] + ' 23:59', '%Y-%m-%d %H:%M')
				except Exception, e:
					pass
			if len(date) < 5:
				self.filt['to'] = datetime.datetime(datetime.MAXYEAR, 12, 31)
	

	def filter_menu(self):
		clients_txt = 'ALL' if len(self.filt['clients']) == 0 else ', '.join(self.filt['clients'])
		projects_txt = 'ALL' if len(self.filt['projects']) == 0 else ', '.join(self.filt['projects'])
		tasks_txt = 'ALL' if len(self.filt['tasks']) == 0 else ', '.join(self.filt['tasks'])
		print
		print '(1) Show only clients:  ' + clients_txt
		print '(2) Show only projects: ' + projects_txt
		print '(3) Show only tasks:    ' + tasks_txt
		print '(4) Start:              ' + self.filt['from'].strftime('%Y-%m-%d, %H:%M')
		print '(5) End:                ' + self.filt['to'].strftime('%Y-%m-%d, %H:%M')
		print '(6) Back'
		print
		user = raw_input('filter > ')

		if user == '1':
			print
			for c, x in enumerate(self.clients):
				print str(c) + ': ' + x
			print
			userr = raw_input('filter > clients > ')
			if userr == '':
				self.filt['clients'] = []
			else:
				try:
					for x in userr.split(','):
							if self.clients.keys()[int(x)] not in self.filt['clients']:
								self.filt['clients'].append( self.clients.keys()[int(x)] )
				except Exception, e:
					pass
			self.filter_menu()
		elif user == '2':
			print
			iter_me = []
			if len(self.filt['clients']) > 0:
				for x in self.filt['clients']:
					iter_me.extend(self.getProjects(x))
			else:
				iter_me = self.projects.keys()
			for c, x in enumerate(iter_me):
				print str(c) + ': ' + x
			print
			userr = raw_input('filter > projects > ')
			if userr == '':
				self.filt['projects'] = []
			else:
				try:
					for x in userr.split(','):
							if iter_me[int(x)] not in self.filt['projects']:
								self.filt['projects'].append( iter_me[int(x)] )
				except Exception, e:
					pass
			self.filter_menu()
		elif user == '3':
			print
			iter_me = []
			if len(self.filt['clients']) > 0 and len(self.filt['projects']) == 0:
				for x in self.filt['clients']:
					iter_me.extend(self.getTasks(client=x))
			elif len(self.filt['projects']) > 0:
					for x in self.filt['projects']:
						iter_me.extend(self.getTasks(x))
			else:
				iter_me = self.tasks.keys()
			for c, x in enumerate(iter_me):
				print str(c) + ': ' + x
			print
			userr = raw_input('filter > tasks > ')
			if userr == '':
				self.filt['tasks'] = []
			else:
				try:
					for x in userr.split(','):
							if iter_me[int(x)] not in self.filt['tasks']:
								self.filt['tasks'].append( iter_me[int(x)] )
				except Exception, e:
					pass
			self.filter_menu()
		elif user == '4':
			print
			print 'Format: YEAR-MONTH-DAY [HH:MM]'
			user = raw_input('filter > start > ')
			if user == '':
				self.filt['from'] = datetime.datetime(1900, 1, 1)
			else:
				self.filter_set('s ' + user)
			self.filter_menu()
		elif user == '5':
			print
			print 'Format: YEAR-MONTH-DAY [HH:MM]'
			user = raw_input('filter > end > ')
			if user == '':
				self.filt['to'] = datetime.datetime(datetime.MAXYEAR, 12, 31)
			else:
				self.filter_set('e ' + user)
			self.filter_menu()
		elif user == '6':
			pass


	def calculate(self, client=True, project=True):
		if client and project:
			head = ['Client', 'Project', 'Task', 'Start', 'End', 'Duration']
			s = ['','','','','']
		elif not client and project:
			head = ['Project', 'Task', 'Start', 'End', 'Duration']
			s = ['','','','']
		elif not client and not project:
			head = ['Task', 'Start', 'End', 'Duration']
			s = ['','','']

		out = []
		out.append( head )
		out.append( [] )
		out.append( 0.0 )
		out.append( [] )
		for x in self.var:
			if self.inFilter(x):
				tmp = []
				if client:
					tmp.append( x[row_project_xtra1] )
				if project:
					tmp.append( x[row_project] )
				tmp.append( x[row_task] + ' (' + x[row_details] + ')' )
				if self.filt['year_long']:
					tmp_date_s = x[row_start_date]
					tmp_date_e = x[row_end_date]
				else:
					tmp_date_s = x[row_start_date][2:]
					tmp_date_e = x[row_end_date][2:]
				if self.filt['show_time']:
					tmp_time_s = ', ' + x[row_start_time]
					tmp_time_e = ', ' + x[row_end_time]
				else:
					tmp_time_s = ''
					tmp_time_e = ''
				tmp.append( tmp_date_s + tmp_time_s )
				tmp.append( tmp_date_e + tmp_time_e )
				tmp.append( x[row_duration] )
				out[1].append( tmp )
				out[2] += float(x[row_duration_dec])
				this_day = datetime.datetime.strptime( x[row_start_date], '%Y-%m-%d' )
				if this_day not in out[3]:
					out[3].append( this_day )
		s.append( return_time(out[2]) )
		out[1].append( s )
		return out
	

	def table(self):
		print
		if len(self.filt['clients']) == 1:
			print 'Table for: ' + self.filt['clients'][0]
			if len(self.filt['projects']) == 1:
				print '   -> ' + self.filt['projects'][0]
				p = self.calculate(False, False)
				print
				print tabulate( p[1], p[0] )
			else:
				p = self.calculate(False, True)
				print
				print tabulate( p[1], p[0] )
		else:
			p = self.calculate(True, True)
			print
			print tabulate( p[1], p[0] )


	def settings_menu(self):
		print
		print '(1) Show long year:', self.filt['year_long']
		print '(2) Show time:     ', self.filt['show_time']
		print '(3) Back'
		print
		user = raw_input('settings > ')
		if user == '1':
			userr = raw_input('settings > long year > ')
			try:
				self.filt['year_long'] = bool(userr)
			except Exception, e:
				pass
			self.settings_menu()
		elif user == '2':
			userr = raw_input('settings > show time > ')
			try:
				self.filt['show_time'] = bool(userr)
			except Exception, e:
				pass
			self.settings_menu()
		elif user == '3':
			pass


	def math(self, calc):
		out = self.calculate(False, False)[2]
		if calc[0:1] == 'm':
			elem = calc.split(' ')
			c = len(elem)
			for x in xrange(0,c):
				try:
					out = out * float(elem[x+1].replace(',', '.'))
				except Exception, e:
					pass
			print
			print 'Multiplication: ' + str(round(out,2)) + ', ' + return_time(out)
		elif calc[0:1] == 'd':
			elem = calc.split(' ')
			c = len(elem)
			for x in xrange(0,c):
				try:
					out = out / float(elem[x+1].replace(',', '.'))
				except Exception, e:
					pass
			print
			print 'Division: ' + str(round(out,2)) + ', ' + return_time(out)


	def days(self):
		print
		print 'Days worked:', len(self.calculate(False, False)[3])






# start analyzer

times = times_class(arguments[1])
run = True

print
print 'Preis Terminal - Analyzer module'
print 'h / help for help'
while run:
	print
	user = raw_input('> ')
	
	# show menu
	if user == 'show' or user == 's':
		times.show_menu()

	# table stuff
	if user == 'table' or user == 't':
		times.table()

	# filter menu
	if user == 'filter' or user == 'f':
		times.filter_menu()
	elif user[0:1] == 'f' and len(user) > 1:
		times.filter_set(user[2:])

	# math stuff
	if user[0:2] == 'm ' or user[0:2] == 'd ':
		times.math(user)

	# show days
	if user == 'days' or user == 'da':
		times.days()

	# settings menu
	if user == 'settings' or user == 'se':
		times.settings_menu()

	# exit this program
	if user == 'exit' or user == 'e':
		run = False

	# show the help
	if user == 'help' or user == 'h':
		print
		head = ['command', 'result']
		content = [
			['show / s', 'opens the show menu'],
			['table / t', 'shows stuff in a table'],
			['filter / f', 'opens the filter menu'],
			['f s/e *', 'immediately sets the filter start / end'],
			['m *', 'multiplicates the total amount by *'],
			['d *', 'divides the total amount by *'],
			['days/ da', 'shows the number of days'],
			['settings / se', 'opens the settings menu'],
			['help / h', 'this help text'],
			['exit / e', 'end the program']
			]
		print tabulate(content, head)

print