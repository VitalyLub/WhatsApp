import sys
import csv
import pandas as pd
from datetime import datetime
import ntpath

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def header(msg):
    print("*" * 50)
    print(msg)
    print("*" * 50)

def parse_line(line):
    end_time_index = line.rfind(",") + 1
    found_index = line[0 : end_time_index].rfind(",")
    is_found = 99999999999999999999
    if line[-23:-20] == ',1,':
        is_found = 1
        found_index = len(line) - 23
    elif line[-23:-20] == ',0,':
        is_found = 0
        found_index = len(line) - 23
    elif line[-23:-20] == '-1,':
        is_found = -1
        found_index = len(line) - 24
    
    
    start_time_index  = line.find(",")
    phone_number_index = line[start_time_index : ].find(",") + start_time_index + 1
    name_index = line[phone_number_index : ].find(",") + phone_number_index + 1
    status_index = line[name_index : ].find(",") + name_index + 1
    
    # print("end time:")
    end_time = datetime.strptime(line[end_time_index : ].strip(), '%Y-%m-%d %H:%M:%S')
    # print("found:")    
    
    # print("start time:")    
    start_time  = datetime.strptime (line[ 0 : start_time_index], '%Y-%m-%d %H:%M:%S')
    # print("phone_number:")
    phone_number = int(line[ phone_number_index : name_index - 1])
    # print("name:")
    contact_name = line[ name_index : status_index - 1]
    # print("status:")
    status = line[status_index : found_index]
    return [start_time, phone_number, contact_name, status, is_found, end_time]
    

def main(argv):
    # reading the file
    with open(argv[1], 'r', encoding="ISO-8859-1") as f:
        mess_data = f.readlines()
 
    print(len(mess_data))

    clean_data = []
    for line in mess_data:
        clean_data.append(parse_line(line))
        
    header("load")
    df = pd.DataFrame(clean_data, 
                  columns = ["start_time", "phone_number", "contact_name", "status", "is_found", "end_time"])
    # get the last row per each phone number
    df1 = df.loc[df.groupby('phone_number', sort=False)['start_time'].idxmax()]

    print("Clean data amount rows:", len(df1))
    
    # statistics about amount of users:
    filtered_by_isfound = df1.groupby(['is_found'])['phone_number'].agg('count')
    print(filtered_by_isfound)
    
    # most populat status
    by_status = df1[df1.is_found > -1]
    by_status = by_status[by_status['status'].str.len() >= 1]
    founded_contacts_amount = len(by_status)
    by_status = by_status.groupby(['status']).size().reset_index(name='count')
    by_status = by_status.sort_values(['count','status'], ascending=[False, True])
    by_status['perc'] = (by_status['count'] / founded_contacts_amount) * 100
    by_status.to_csv("/cs/usr/vitaly92/Desktop/by_status_" + path_leaf(argv[1]), sep='\t', encoding="utf-8")
    

if __name__ == "__main__":
    main(sys.argv)
