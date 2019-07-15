import glob, os
import csv 

os.chdir("C:\\Users\\DELL\\Downloads\\New folder")
files = [] 
for file in glob.glob("*.txt"):
    files.append("C:\\Users\\DELL\\Downloads\\New folder\\"+file)


big_list = []
with open(files[0], 'r') as content_file:
	content = content_file.readlines()
	for row in content:
		big_list.append(row.split(",")[0])
		
data = list(set(big_list))

with open("C:\\Users\\DELL\\Downloads\\New folder\\out.csv", 'w', newline='') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     wr.writerow(data) 