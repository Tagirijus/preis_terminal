# coding=utf-8

import os
path_to_project = os.path.dirname(os.path.realpath(__file__))

# some default values

def_project_client_title 	= 'Herr'
def_project_client_name 	= 'Max Mustermann'
def_project_client_address 	= 'Straße 5b'
def_project_client_city 	= '47209 Stadt'

def_project_name		 	= 'Projekt X'
def_project_offer_filename 	= 'Angebot_-_Projekt_X.odt'
offer_template_filename		= path_to_project + '/template.odt'


date_format			= '%d.%m.%Y'
placeholde_date 	= '{DATE}'

placeholde_title 	= '{TITLE}'
placeholde_name 	= '{NAME}'
placeholde_address 	= '{ADDRESS}'
placeholde_city 	= '{CITY}'

placeholde_project 	= '{PROJECT}'

placeholde_option 	= '{OPTION}'
placeholde_task 	= '{TASK}'
placeholde_amount 	= '{AMOUNT}'
placeholde_price 	= '{PRICE}'
placeholde_SUM	 	= '{SUM}'

# coor stuff

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