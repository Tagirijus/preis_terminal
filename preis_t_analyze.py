import os
import sys
from tabulate import tabulate
import codecs
import datetime


# getting arguments and loading file

arguments = sys.argv

if len(arguments) <= 1:
	exit()


# getting file into a variable

if os.path.isfile(os.getcwd() + '/' + arguments[1]):
	f = codecs.open(os.getcwd() + '/' + arguments[1], 'r', 'utf-8')
	csv_file = f.readlines()
	f.close()
else:
	print 'No file found, sorry!'
	exit()



# getting the file_variable into a usable vars for the program

def init_variable(variable, seperator=','):
	if type(variable) is list:
		out = []
		for x in variable:
			tmp = x.rstrip().split(seperator)
			if len(tmp) > 1:
				out.append( tmp )
			else:
				print 'File is no CSV or maybe seperater is no \',\'?'
				print 'Ctrl+C for cancelling the program otherwise.'
				new_sep = raw_input('New seperator: ')
				return init_variable(variable, new_sep)
		return out
	else:
		print 'Error with the filetype, sorry.'
		exit()

VAR_tmp = init_variable(csv_file)
VAR = VAR_tmp[1:]

# cols from default Gleeo Time Tracker export: 9, 0, 1, 3 and 4 and 5 and 6(date = start/end date and time here), 8 (deciaml duration)
VAR_head = ['Client', 'Project', 'Task', 'Date', 'Duration']

# the filter
filt = {}
filt['str'] = []
filt['from'] = datetime.datetime(datetime.MINYEAR, 1, 1)
filt['to'] = datetime.datetime(datetime.MAXYEAR, 12, 31)



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



# start analyze

# show clients

clients = []
print 'Available clients:'
for x in VAR:
	if not x[9] in clients:
		clients.append(x[9])

for y, x in enumerate(clients):
	print '(' + str(y) + ') ' + x
print '(' + str(len(clients)) + ') All'

user_client = raw_input('> ')
try:
	user_client = int(user_client)
except Exception, e:
	print 'Out of range'
	exit()
if not user_client > len(clients)+1:
	filt['str'].append(clients[user_client])


# show projects

show = []
total_time = 0.0
for x in VAR:
	if filter_it(x):
		total_time += float(x[8])
		show.append( [ x[9], x[0], x[1], 'TIME', return_time(float(x[8])) ] )
show.append( [ '---', '---', '---', '---', return_time(total_time) ] )

print tabulate(show, VAR_head)