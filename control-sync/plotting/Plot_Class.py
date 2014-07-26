################################################################################
""" File: Plot_Class.py

This file contains the plotting class and driver to test the class. """
################################################################################

########## Import proper Libraries ##########
import csv
import numpy
import operator
import datetime
import itertools
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

########## Plotting Class using Matplotlib ##########
class Plotting(object):

	### Initialize objects ###
	def __init__(self, filename, BeginDateIn, EndDateIn, field, PlotAll):
		# Name of datafile
		self.PlotAll = PlotAll
		self.openfile = open(filename, 'r')
		self.filename = filename
		self.dataorganized = csv.DictReader(self.openfile)
		self.ChosenData = []	# Holds data for specific field
		self.ConvertedTime = []	# Holds converted datetime objects
		self.BeginDate = 0	# Begin date for data plotted
		self.EndDate = 0	# End date for data plotted
		self.BeginIndex = 0	# Begin index of data plotted
		self.EndIndex = 0	# End index of data plotted
		self.field = field	# Fields for data to plot
		self.x = []		# Time data for x-axis
		self.input_time(filename, BeginDateIn, EndDateIn)
		self.y = []		# Field data for y-axis
		self.i = 0		# Index to go through fields
		self.color = 'b'	# Color of data for specific field
		self.colors = itertools.cycle(['r','g','y','c','m','k','0.75','#663300','#660066','#ff6600','#996600','#800000','b'])
	
	### Input time interval ###
	# Using begin and end date, finds time data for x-axis of graph
	def input_time(self, filename, BeginDateIn, EndDateIn):

		# Convert input dates
		self.BeginDate = datetime.datetime.strptime(BeginDateIn + "00", "%Y-%m-%d %H:%M:%S.%f%z")
		self.EndDate = datetime.datetime.strptime(EndDateIn + "00", "%Y-%m-%d %H:%M:%S.%f%z")

		# Convert time
		self.ConvertedTime = self.convert_date(self.dataorganized)

		# Find index for time
		self.BeginIndex = self.find_index(self.BeginDate, self.ConvertedTime)
		self.EndIndex = self.find_index(self.EndDate, self.ConvertedTime)

		# Obtain the dates for plotting
		self.x = self.gather_dates(self.ConvertedTime, self.BeginIndex, self.EndIndex)


	### Input data field to plot ###
	# Finds data over a time range for a certain field to plot on the y-axis
	def input_field(self, filename, field, i):

		# Get chosen data
		self.dataorganized = csv.DictReader(self.openfile)
		self.openfile.seek(0) #Reset iterator
		self.ChosenData = self.get_data(self.dataorganized, field[i])

		# Obtain the chosen data in the specified range
		self.y = self.gather_chosen(self.ChosenData, self.BeginIndex, self.EndIndex)
		# Increment index
		self.i += 1

	### Convert Data String  -> Float ###
	# Converts data in a specified field to a float
	def convert_to_float(self, row, field):

		# Check if there is data
		if(row[field] == ''):
			# No data is not a number
			row[field] = float('nan')
			return row[field]

		else:
			# Convert value and return
			row[field] = float(row[field])
			return row[field]


	### Pull out the non-date data ###
	# Extracts the data from a specified field (not time)
	def get_data(self, data, field):

		# Establish a Variable
		value = []

		# Loop through the data
		for row in data:
		
			# Store the seeked data
			value.append(self.convert_to_float(row, field))

		# Return the desired data
		return value


	### Convert the date String -> Datetime ###
	# Converts the date string into a Datetime object
	def convert_date(self, data):
	
		# Establish a Variable
		t = []
		field = "db_time"

		# Loop through the data
		for row in data:	

			# Store the date
			t.append(datetime.datetime.strptime(row[field]+"00", "%Y-%m-%d %H:%M:%S.%f%z"))

		# Return
		return t


	### Find the index of data ###
	# Using input date, return index
	def find_index(self, InputDate, ConvertedSet):

		# Establish a variable
		index = 0

		# Begin looping
		for row in ConvertedSet:
		
			# Check for a match
			if(InputDate.year == row.year):
				if(InputDate.month == row.month):
					if(InputDate.day == row.day):
						if(InputDate.hour == row.hour):
							if(InputDate.minute == row.minute):
								if(InputDate.second == row.second):
									return index
								else:
									index += 1
							else:
								index += 1
						else:
							index += 1
					else:
						index += 1
				else:
					index += 1
			else:
				index += 1


	### Gather the chosen data in the range ###
	# Using the beginning index and end index, returns chosen data in range
	def gather_chosen(self, ChosenData, BeginIndex, EndIndex):
	
		# Establish a storing variable
		chosen = []

		# Establish a while Loop
		while(BeginIndex >= EndIndex):
	
			# Begin gathering
			chosen.append(ChosenData[BeginIndex])

			# Decrement
			BeginIndex -= 1

		# Return the data
		return chosen


	### Gather the Dates for plotting ###
	# Using the beginning index and end index, returns range of dates
	def gather_dates(self, ConvertedTime, BeginIndex, EndIndex):
	
		# Establish variables
		range = []
	
		# Establish while loop
		while(BeginIndex >= EndIndex):
		
			# Gather the dates
			range.append(ConvertedTime[BeginIndex])

			# Decrement
			BeginIndex -= 1
	
		# Return the dates
		return range


	### Plot Data ###
	"""Plots the data as a scatter plot using times and data,
	formats and saves plot"""
	def plot_data(self):

		#Plot All?
		if(self.PlotAll == True):
			
			#Array to hold fields
			ChosenFields = []

			#Obtain all Field titles
			self.openfile.seek(0) #Reset iterator
			for row in self.openfile:
				allfields = row
				break

			#Split the fields
			allfields = allfields.split(',')
	
			#Store all fields, EXCEPT address and db_time
			for info in allfields:

				if(info != 'address' and info != 'db_time'):
					
					ChosenFields.append(info)

			#Check for any extra characters
			i = 0
			while(i < len(ChosenFields)):
			
				if(ChosenFields[i].endswith('\n')):

					#Remove the error
					error = ChosenFields[i]
					error = error[:-1]
					ChosenFields[i] = error

				#Increment
				i += 1

			#Return all 
			self.field = ChosenFields

		# Find number of fields to plot
		num_fields = len(self.field)

		# While there are still fields to plot
		while(self.i < num_fields):

			# Getting y-axis data for field
			self.input_field(self.filename, self.field, self.i)

			# Plot data as a scatter plot
			plt.scatter(self.x, self.y, c = self.color, marker='.', edgecolors='none')

			# Change color for next plot
			self.color = next(self.colors)

		# Plot Format
		plt.xlabel('Time')
		plt.title('Weather Box Data')
		plt.xlim(self.BeginDate, self.EndDate)
		plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y\n%H:%M:%S'))
		plt.ylim(-1000, 9000)
		plt.gcf().autofmt_xdate()

		#Legend Format
		plt.legend(self.field, loc='upper center', scatterpoints=1, fontsize=8, bbox_to_anchor = (0.5, 1.0), fancybox = True, ncol = 4)

		# Save plot as .png
		plt.savefig('WeatherboxData_Graph.png')

		# Display plot
		plt.show()


########## Main ##########

# Create class
weatherbox = Plotting('215_data.csv', '2014-05-26 00:00:00.000000-10', '2014-05-29 21:56:14.000000-10', ['apogee_w_m2','panel_mv','batt_mv','bmp085_temp_decic'], True)

# Plot data and save as a .png
weatherbox.plot_data()

# Close file
weatherbox.openfile.close()
