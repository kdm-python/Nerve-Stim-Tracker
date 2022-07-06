"""

*** Nerve Stimulator Tracker ***

Program to keep track of pain levels, device progrsm, device strength for each hour of each day.
Auto generate a week, month or year, referring to the calendar module.
Then analyse data and plot graphs.

"""

import matplotlib
import datetime as dt
import shelve
import calendar
from classes import Day

# read/write files, add FNF exceptions:
def read_data(file_name):

	with shelve.open(file_name) as shelve_file:
		return dict(shelve_file)

def write_data(file_name, *days):
	
	with shelve.open(file_name) as shelve_file:
		for day in days:
			shelve_file[str(day.date_day)] = day

# functions to generate a number of empty days
# aim to make use of the calendar module
def new_day():
	pass

def new_week():
	pass

def new_month():
	pass

### INPUT MENU ###

def add_menu():
	pass

def continue_menu():
	pass

def display_single():
	pass

def display_all():
	pass

# NOTE: get average pain & average program, plot graph