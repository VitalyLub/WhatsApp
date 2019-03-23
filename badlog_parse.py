import csv
import pandas as pd
from datetime import datetime
import re

def column(matrix, i):
    return [row[i] for row in matrix]

def parse_line(line):
    end_time_index = line.rfind(",") + 1
    found_index = line[0 : end_time_index].rfind(",") - 1
    start_time_index  = line.find(",")
    phone_number_index = line[start_time_index : ].find(",") + start_time_index + 1
    name_index = line[phone_number_index : ].find(",") + phone_number_index + 1
    status_index = line[name_index : ].find(",") + name_index + 1
    
    # print("end time:")
    end_time = datetime.strptime(line[end_time_index : ].strip(), '%Y-%m-%d %H:%M:%S')
    # print("found:")    
    is_found = int(line[found_index : end_time_index - 1])
    # print("start time:")    
    start_time  = datetime.strptime (line[ 0 : start_time_index], '%Y-%m-%d %H:%M:%S')
    # print("phone_number:")
    phone_number = int(line[ phone_number_index : name_index - 1])
    # print("name:")
    contact_name = line[ name_index : status_index - 1]
    # print("status:")
    status = line[status_index : found_index - 1]
    return [start_time, phone_number, contact_name, status, is_found, end_time]


path_log = "/cs/usr/vitaly92/Desktop/badlog.txt"
path_data = "/cs/usr/vitaly92/Desktop/rowdata.csv"

with open(path_log, 'r') as myfile:
    text=myfile.read().replace('\n', '')

phone_numbers = re.findall(r'376\d{6}', text)
phone_numbers = list(map(int, phone_numbers))

print(len(phone_numbers))

with open(path_data, 'r', encoding="ISO-8859-1") as f:
    mess_data = f.readlines()
 
print(len(mess_data))

clean_data = []
for line in mess_data:
    clean_data.append(parse_line(line))
good_phone_numbers = column(clean_data, 1)


phone_numbers_to_check = [item for item in phone_numbers if item not in good_phone_numbers]
print(len(phone_numbers_to_check))

with open("/cs/usr/vitaly92/Desktop/output.txt", 'w', newline='') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     wr.writerow(phone_numbers_to_check)


