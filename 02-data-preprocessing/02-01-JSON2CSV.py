# Python program to convert
# JSON file to CSV


import json
import csv


# Opening JSON file and loading the data
# into the variable data
with open('PATH TO JSON FILE') as json_file:
	data = json.load(json_file)

employee_data = data['id']

# now we will open a file for writing
data_file = open('TARGET PATH FOR CSV FILE', 'w')

# create the csv writer object
csv_writer = csv.writer(data_file)

# Counter variable used for writing
# headers to the CSV file
count = 0

for emp in employee_data:
	if count == 0:

		# Writing headers of CSV file
		header = emp.keys()
		csv_writer.writerow(header)
		count += 1

	# Writing data of CSV file
	csv_writer.writerow(emp.values())

data_file.close()



# import pandas as pd
# import json
# import os

# os.chdir('/Users/philippeprince/Downloads')

# # Reading the json as a dict
# with open('/Users/philippeprince/Downloads/5Kn29akl.json') as json_data:
#     data = json.load(json_data)


# # using the from_dict load function. Note that the 'orient' parameter 
# #is not using the default value (or it will give the same error that you got before)
# # We transpose the resulting df and set index column as its index to get this result
# pd.DataFrame.from_dict(data, orient='index').T.set_index('index')   

df = pd.read_json(r'/Users/philippeprince/Downloads/5Kn29akl.json')
df_json = globals()['df'].to_json(orient='split')
df_json = globals()['df'].to_json(orient='split')
# print(df)
# df2 = pd.DataFrame.from_dict(df, orient='index')
# df2 = df2.transpose()
# df2.to_csv (r'/Users/philippeprince/Downloads/5Kn29akl.csv', index = None)