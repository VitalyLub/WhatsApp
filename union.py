import random
import datetime
import requests
import base64
import os
from os import listdir, utime
from os.path import isfile, join
import sys
import json
import csv

BASIC_PATH = "/cs/usr/vitaly92/.++/to_work/"

def main(argv):
    
    folder_path = BASIC_PATH + argv[1] + "_images/"
    all_files = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]
    
    
    for file_path in all_files:
        print(file_path)
        data = []        
        phone_number = file_path.split(".")[0]
        for line in open(folder_path + file_path):
            line_with_phone_number = [phone_number]
            splitted = line.split(",")
            for i in range(len(splitted)): 
                line_with_phone_number.append(splitted[i].replace('"', '').replace("\n", ""))
            data.append(line_with_phone_number)
        with open(folder_path + "out.csv", 'a', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerows(data)
    
    
            
    
if __name__ == "__main__":
    main(sys.argv)
