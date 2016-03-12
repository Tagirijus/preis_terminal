# coding=utf-8

import os
path_to_project = os.path.dirname(os.path.realpath(__file__))

# some default values

def_project_company			= 'Company'
def_project_client_title 	= 'Herr'
def_project_client_name 	= 'Max Mustermann'
def_project_client_address 	= 'Straße 5b'
def_project_client_city 	= '47209 Stadt'

def_project_name		 	= 'Projekt X'
def_project_about		 	= 'Auflistung der Arbeitsabschnitte im Bereich Musik- und Tonproduktion für genanntes Projekt:'
def_project_offer_filename 	= 'Angebot_{YEAR}_-_{PROJECT_NAME}.odt'
offer_template_filename		= path_to_project + '/template.odt'
def_project_save_name		= '{COMPANY}_{DATE}_{PROJECT_NAME}'

date_format					= '%d.%m.%Y'
decimal						= ','
def_commodity				= '€'
def_hoursday				= 6
							# monday=0, ... , sunday=6
def_workdays				= [0,1,2,3,4]
def_minimumdays				= 2

old_filetype_save			= False
old_filetype_load			= False


# visual stuff

small_table = False
colorize = True

WHITE = '\033[97m'
PURPLE = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
BOLD = '\033[1m'
DIM = '\033[2m'
GREY = '\033[90m'
UNDERLINE = '\033[4m'

# customize the colors here !!!

# normal text
CL_TXT = PURPLE if colorize else ''
# info, error and warning text
CL_INF = BOLD + RED if colorize else ''
# default values
CL_DEF = YELLOW if colorize else ''
# dimmed output
CL_DIM = GREY if colorize else ''
# final output
CL_OUT = BOLD + YELLOW if colorize else ''

# don't change this- it's the ending string for the coloring strings
CL_E = '\033[0m' if colorize else ''