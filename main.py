"""

Nerve Stimulator Tracker by Kyle Marden

Enter and store device settings (program & strength) and pain level for each hour of each day and generate statistics such as average pain 
level. Each month is persisted in a pickled shelve dictionary with the date as the key and a Day class object as the value. Each hour's record
is represented by a separate Hour object stored within the Day object.
Includes a simple command-line input menu to create a new file, update existing an file, display current data, and see statistics for each day.
This will be expanded to analysing the relationship between settings and pain levels over weeks or months. Example existing data is included called
'july-data'. Enter this as the file path when prompted to access this data. This will be changed to generate file path from user entering a month.

"""

from os.path import exists
import shelve
from datetime import date
from pathlib import Path

from main_classes_ import Hour, Day

# File read/write

def make_new_file(file_name, dates):
	"""dates = list of lists [year, month, day]. Create new file with string rep of the dates
	as key, and a newly created Day object as the value. Return as dictionary."""
	
	with shelve.open(file_name) as shelve_file:
		for d in days:
			# create a date object from each string provided
			dt_obj = date(*[int(x) for x in d.split('-')])
			new = Day(dt_obj)
			shelve_file[d] = new

def open_file(file_path):
	"""Read a shelve file and return it as a dictionary."""

	assert exists(f'{file_path}.dat'), 'Specified file path not found.'
	with shelve.open(file_path) as shelve_file:
		return dict(shelve_file)

def edit_file(file_path, date_, day_obj):
	"""Replace existing object value for the date_ key with the new day_obj."""
	
	with shelve.open(file_path) as shelve_file:
		shelve_file[date_] = day_obj

# Display data

def print_day(day_obj):
	"""Print the date and hour records of a given day."""

	print(day_obj)
	print(type(day_obj))
	for k, v in day_obj.get_all_hours().items():
		print(f'{k}: {v}')

def print_dates(data):
	"""Print on separate lines the dates within this file for user to choose."""

	for key in data.keys():
		print(key)

def print_pain_stats(data):
	"""Display pain statistics on separate lines."""
	for k, v in data.items():
		print(f'{k}: {v}')

def print_prog_stats(data):
	"""Display program statistics on separate lines."""

	# need to reformat named tuple values to readable format
	for k, v in data.items():
		print(f'{k}: {type(v)}: {v}')

# Input validation

def check_val_range(start, end, input_txt):
	"""Confirm the input called stat is an integer value between start and end."""
	
	# WARNING: possible bug: if the max val range isn't right, then stuck in the check_val_range_loop with no way out
	while True:
		try:
			i = int(input(input_txt))
		except (ValueError, TypeError):
			print('Not an integer value.')
		else:
			if i < start or i > end:
				print(f'Number entered not within correct range.')
			else:
				return i 

# Input new hour data

def stat_input():
	"""Take input of three integer values for program, strength and pain levels. 
	Check numbers are within correct ranges, then return Hour object once user confirms."""

	while True:
		try:
			prog, stren, pain = [int(x) for x in input('Enter program, strength and pain level separated by spaces\n-> ').split()]
		except (TypeError, ValueError):
			print('Invalid entry format.')
		else:
			return prog, stren, pain

def add_hr_to_day(day):
	"""User input to select hour record and enter new info, repeat as desired, then return edited object."""

	while True:
		print_day(day)
		# hr = check_val_range(0, 23, 'Choose start time of 0-23 or e to go back\n-> ')
		hr = input('Choose start time of 0-23 or e to go back\n-> ')
		if hr == 'e':
			return day  # replaces day object with same out outside, maybe inefficient but works for now
		else:
			hr = int(hr)

		stats = None
		while True:
			try:
				stats = stat_input()
				day.add_hour(hr, *stats)
				# Check values are in correct ranges from assertion statements in Hour obj method set_stats()
			except AssertionError as error:
				print(error)
			else:
				break
			
		day.add_hour(hr, *stats)
		print_day(day)

		another = check_val_range(1, 3, '1) Copy to next hour 2) Choose new hour 3) Exit\n-> ')
		if another == 1:
			while True:
				day.add_hour(hr + 1, *stats)
				print_day(day)
				hr += 1
				again = input('Press enter to add to next, anything else to go back\n-> ')
				if again == '':
					continue  # stay within this loop
				else:
					break  # back to outer loop
		elif another == 2:
			continue  # back to outer loop
		elif another == 3:
			return day  # return edited day object

# User menus

def select_month_year():
	"""Not implemented yet, but will validate a month and year entry, which will be used to create a file
	path in outer functions. """
	
	month, year = [x for x in input('Enter month and year (sep by space)\n-> ').split()]
	month = month.title()
	assert month in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 
	'August', 'September', 'October', 'November', 'December'], 'Not a valid month!'
	return month, year

def select_date(data):
	"""Open file, display the dates, take user input and return the date after checks."""
	
	print_dates(data)
	date_ = input('Enter date in format above\n-> ')
	assert date_ in data.keys(), 'Invalid date.'
	
	return date_

def day_menu(file_path, day, date):

	# Also add below the day of the week
	while True:
		print(f'''
{day}
1) Display data
2) Add/edit hour records
3) Pain stats
4) Program stats
5) Go back
	''')

		select = check_val_range(1, 5, 'Select option\n-> ')
		if select == 1:
			print_day(day)
		elif select == 2:
			day = add_hr_to_day(day)  # get edited day object
			edit_file(file_path, date, day)  # replace current day object with updated one
		elif select == 3:
			print_pain_stats(day.pain_stats())
		elif select == 4:
			print_prog_stats(day.program_stats())
		else:
			break

def main_menu():

	while True:
		print('''
################################
### Nerve Stimulator Tracker ###
################################
		
Welcome Kyle.
1) Enter existing file name
2) Create new file
3) Exit
		''')

		select = check_val_range(1, 3, 'Make your selection\n-> ')
		if select == 1:

			while True:
				# month, year = select_month()  # return month and year to create file path
				# expand to access year and month directories later
				# look up how to create file paths
				
				file_path = input('Enter file name\n-> ')  # temporarily enter just the file path
				try:
					data = open_file(file_path)  # return dict of month's shelve file
					date_ = select_date(data)  # return date key to access
				except AssertionError as error:
					print(error)
				else:
					day = data[date_]  # return the Day object matching the date key
					day_menu(file_path, day, date_)  # edit Day object and then replace old one in file
					# WARNING: this exits entire program, need to fix to stay in the menu loop
					break

		if select == 2:
			print('Coming soon.')
		else:
			print('Goodbye Kyle. Have a nice day.')
			break

main_menu()
