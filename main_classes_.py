"""
Classes for the nerve stimulator app to represent days and hours of date, pain level and device settings.
"""

from datetime import date
from collections import namedtuple, Counter

# named tuple for easier referencing
Settings = namedtuple('Settings', 'program strength')

class Hour:
	"""
	Represents a single hour time period's noted stats.
	A program value of 0 indicates the device is off.
	A pain value of 0 indicates patient is asleep.
	"""

	# maybe can take out init function, always created without these attributes anyway
	def __init__(self):
		"""Initialise empty hour."""
		self.settings = None
		self.pain = None

	def get_settings(self):
		"""Return the named tuple of program and strength levels."""
		return self.settings

	def get_pain(self):
		"""Return integer pain value."""
		return self.pain

	def set_stats(self, program, strength, pain):
		"""Set stats for this hour."""

		# catch AssertionError in main program and print the corresponding message
		assert program >= 0 and program <= 5, 'Program value must be between 0 and 5.'
		assert strength >= 0 and strength <= 14, 'Strength value must be between 0 and 14.'
		assert pain >= 0 and pain <= 10, 'Pain value must be between 1 and 10.'
		
		self.settings = Settings(program, strength)
		self.pain = pain

	def __str__(self):
		"""Different str reps depending on whether the device is off or patient is asleep."""
		
		if self.settings is not None:
			prog_str = 'DEVICE OFF' if self.settings.program == 0 else f'Program: {self.settings.program}'
			stren_str = '' if self.settings.strength == 0 else f'Strength: {self.settings.strength}'
			pain_str = 'ASLEEP' if self.pain == 0 else f'Pain: {self.pain}'
			return f'{prog_str} {stren_str} | {pain_str}'
		else:
			return 'No record'

class Day:
	"""
	Represents a single day composed of a datetime object and 24 hour objects.
	Hour indexes work like this: 0 = 0000-0100, 14 = 1400-1500 and so forth.
	"""
	
	def __init__(self, date_):
		self.date = date_  # datetime object

		# generate dict with 0-23 as keys each with a value of empty Hour object
		self.hours = dict(zip([x for x in range(0,24)], [Hour() for x in range(0, 24)]))

	def get_date(self):
		"""Return datetime object."""
		return self.date

	def get_all_hours(self):
		"""Return dictionary of hour ids and hour objects."""
		return self.hours

	def get_hour(self, hr_id):
		"""Return the hour object at the specified key."""
		return self.hours(hr_id)

	def add_hour(self, hour, program, strength, pain):
		"""Fill empty hour record or replace existing. This is better I think."""
		self.hours[hour].set_stats(program, strength, pain)

	def pain_stats(self):
		"""Return dict of min, max, avg pain and hours asleep/awake."""

		if len(self.hours) != 24:
			print(f'NOTE: only {len(self.hours)} hours found for the day.')

		awake_hrs = [x.pain for x in self.hours.values() if x.pain != 0]
		asleep_hrs = [x.pain for x in self.hours.values() if x.pain == 0]

		return {
			'hours awake': len(awake_hrs),
			'hours asleep': len(asleep_hrs),
			'min pain': min(awake_hrs),
			'max pain': max(awake_hrs),
			'average pain': sum(awake_hrs) / len(awake_hrs)
		}

	def program_stats(self):
		"""Return dict containing info about programs used today and how many hours they were on."""

		all_settings = [x.settings for x in self.hours.values()]
		all_progs = [x.settings.program for x in self.hours.values()]

		# needs work to represent the named tuples and counts more readably
		return {
			'settings': set(all_settings),  # set of named tuples
			'programs': set(all_progs),  # set of ints
			'setting counts': Counter(all_settings),  # Counter obj for settings named tuples
			'program counts': Counter(all_progs)  # Counter obj for program ints
		}

	def __repr__(self):  # add day of the week here
		return f'Day {self.date.day}/{self.date.month}/{self.date.year}'

def make_time(hour_ind):
	"""Convert the hour index number into 24hr time period string."""
	
	# not implemented yet, need to replace hour index with the time period when printing a day/hour
	# NOTE: need to account for index 9 which is 0900 - 1000, 1 digit then 2 digit
	if len(str(hour_ind)) == 1:
		time_str = f'0{hour_ind}00 - 0{hour_ind + 1}00'
	else:
		time_str = f'{hour_ind}00 - {hour_ind + 1}00'
	
	return time_str
