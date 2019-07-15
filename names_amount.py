import pandas as pd
import glob, os
import csv 

def if_contains(txt, lst):
	for row in lst:
		if row == txt or row.endswith(" " + txt) or row.startswith(txt + " ") or " " + txt + " " in row:
			return 1
	return 0

os.chdir("C:\\Users\\DELL\\Downloads\\New folder")
files = [] 
for file in glob.glob("*.txt"):
    files.append("C:\\Users\\DELL\\Downloads\\New folder\\"+file)


names = []
with open(files[0], 'r') as content_file:
	content = content_file.readlines()
	for row in content:
		if len(row.split(",")[0]) > 2:
			names.append(row.split(",")[0])
		
names = list(set(names))

file_errors_location = 'C:\\Users\\DELL\\Downloads\\status_frequency.xlsx'
df = pd.read_excel(file_errors_location, sheet_name='liechtenstein')

counter = 0
total_perc = 0
for index, row in df.iterrows():
	try:
		if (if_contains(row['status'], names) == 1):
			print(row['status'], row['perc'])
			counter += 1
			total_perc += row['perc']
	except:
		print("ERROR:", row['status'])
print(counter)
print(total_perc)