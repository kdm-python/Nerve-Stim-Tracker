"""
Classes to be used by the stim tracking app.
Currently a day is a single class, am thinking of expanding into Hour record class and week/month to.
"""

import datetime as dt
from collections import Counter

def get_stats(key, records):
	"""Analyse a set of hour: {stats} records and return min, max and avg.
	Choose any key of the dictionary."""

	records = {k: v for k, v in records.items() if v != None}

	values = []  # values in dictionary for the specified stat
	results = {}

	for hour, val_dict in records.items():
		values.append(val_dict[key])

	if key == 'pain':
		values = [x for x in values if x != 0]

	results = {
		'min': min(values),
		'max': max(values),
		'avg': round(sum(values) / len(values), 2)
	}

	return results

def get_hr_count(key, hr_records):
	"""Extract each different program and the number of hours it occurs."""

	programs = []
	for k, v in hr_records.items():
		programs.append(v[key])

	c = dict(Counter(programs))
	return c

class Day:
	"""Represents a single day containing 24 hour dictionaries."""
	
	hours = [x for x in range(1, 25)]  # never changes, pain/prog/str scales could change

	def __init__(self, year, month, day):
		try:
			self.date_day = dt.date(year, month, day) 
		except ValueError:
			raise Exception('At least one of the numbers in day_date parameter is invalid.')
		self.pain_lvls = [x for x in range(0, 11)]  # 0 indicates asleep
		self.programs = [x for x in range(0, 6)]  # 0 indicates device off
		self.strengths = [x for x in range(0, 15)]
		self.records = dict(zip(Day.hours, [None]*len(Day.hours)))

	# NOTE: each record represents the hour AFTER that number i.e. 12 = pain at 12-13 time
	# e.g. change device at 1pm, then fill in record 13 at 2pm for the previous hour's results

	def add_record(self, hour, pain, program, strength):
		"""Set an existing hour record's value to a dictionary containing the supplied stats."""
		
		# PROGRAM 0 indicates DEVICE OFF
		# PAIN 0 indicates ASLEEP

		# check all values are within correct ranges. Allows for program and strength scales to be altered.
		# ERROR: Exceptions not working properly: Tells me 0 is incorrect but 0 is in the lists above... 

		if hour not in Day.hours:
			raise Exception('Hour must be between 0 and 23.')
		if pain not in self.pain_lvl:
			raise Exception(f'Pain level must be between {min(self.pain_lvls)} and {max(self.pain_lvls)}')
		if program not in self.programs::
			raise Exception(f'Program must be between {min(self.programs)} and {max(self.programs)}')
		if strength not in self.strengths:
			raise Exception(f'Strength must be between {min(self.strengths)} and {max(self.strengths)}')

		self.records[hour] = {'pain': pain, 'program': program, 'strength': strength}

	def continue_record(self, hour, num_hours):
		"""Copy an hour's record for a specified number of hours afterwards."""
		
		hours_copy = [x for x in range(hour, hour + num_hours + 1) if x != hour]
		for hr in hours_copy:
			self.records[hr] = self.records[hour]
		print(f'Copied hour {hour} to hours {hours_copy}.')

	def get_record(self, hour):
		"""Return a single record dictionary"""
		return self.records[hour]

	def get_all_records(self, inc_none=True):
		"""Return dictionary of hours and stats dictionaries."""
		return self.records

	def get_hour_range(self, start_hr, end_hr):
		"""Return hour dictionaries where hour key is between specified hours."""
		
		print(f'Records between hours {start_hr} and {end_hr} including None values:')
		return {k: v for k, v in self.records.items() if k >= start_hr and k <= end_hr}

	def get_day_date(self):
		"""Return the date of this day as a datetime object."""
		return self.date_day

	def empty_record(self, hour):
		"""Set one record value to None."""
		
		print(f'Hour {hour} record is now empty.')
		self.records[hour] = None

	def empty_all(self):
		"""Set all hour records to None."""

		print(f'All {self.date_day} records are now empty.')
		self.records = {k: None for k, v in self.records.items()}

	# NOTE: Combine the below functions, reduce repetition
	def analyse_all_data(self, key):
		"""Return min, max and avg pain, program or strength levels for this day.
		Asleep values are removed if pain key is chosen."""

		results = get_stats(key, self.records)
		print(f'* {key} levels on {self.date_day} *')
		for k, v in results.items():
			print(f'{k.title()}: {v}')

		return results

	def analyse_hour_data(self, key, start_hr, end_hr):
		"""Return min, max and avg value for pain, program or strength key."""
		
		records = self.get_hour_range(start_hr, end_hr)
		results = get_stats(key, records)
		print(f'* {key} levels on {self.date_day} between {start_hr} and {end_hr}*')
		
		for k, v in results.items():
			print(f'{k.title()}: {v}')

		return results

	def program_count(self, key):
		"""Return dictionary with each program and how many hours it was on for."""
		
		c = get_hr_count(key, self.records)
		for k, v in c.items():
			if v == 0:
				v = 'OFF'

		return c

	def prog_str_count(self):
		"""Return tuples: (pain, (prog, str))"""
		pass

	def __str__(self):
		print(f'* Records for {self.date_day} *')
		record_str = ''
		for hour, values in self.records.items():
			if values != None:
				if values['program'] == 0 and values['pain'] == 0:
					record_str += f'{hour - 1} - {hour} | DEVICE OFF & SLEEP\n'
				elif values['program'] == 0: 
					record_str += f'{hour - 1} - {hour} | Pain: {values["pain"]} | DEVICE OFF\n'
				elif values['pain'] == 0:
					record_str += f'{hour - 1} - {hour} | ASLEEP | Program: {values["program"]} Strength: {values["strength"]}\n'
				else:
					record_str += f'{hour - 1} - {hour} | Pain: {values["pain"]} Program: {values["program"]} Strength: {values["strength"]}\n'
			else:
				record_str += f'{hour} - {hour + 1} | NO RECORD\n'
		
		return record_str

class Hour:
	"""Represents a single hour record containing pain level & program and strength settings."""
	pass

def testing():
	jul_4 = Day(2022, 7, 4)
	jul_4.add_record(hour=1, pain=0, program=0, strength=0)
	jul_4.continue_record(1, 5)

if __name__ == '__main__':
	testing()