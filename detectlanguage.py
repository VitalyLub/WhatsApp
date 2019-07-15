import sys
import csv
import pandas as pd
from datetime import datetime
import ntpath
import re
import requests
import io
import json
from time import gmtime, strftime


URL = "https://translation.googleapis.com/language/translate/v2/detect/?q={0}&key=AIzaSyDl1xTJIY-fTf8RZz2Eta4ASzIbVfsXYU4"

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def main(argv):
    # reading the file
    with open(argv[1], 'r', encoding="utf-8") as f:
        data = f.readlines()
    data = data[1:]    
    print(len(data))
    
    splitted_data = []
    for row in data:      
        splitted_data.extend([re.split(r'\t+', row.replace('\n',''))])
    
    i = 0
    while i < len(splitted_data):
        if (i % 100 == 0):
            print(i, strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        status = splitted_data[i][1]      
        language = 'None'        
        if (len(status) > 1):
            api_answer = json.loads(requests.get(URL.format(status)).content)
            try:            
                language = api_answer['data']['detections'][0][0]['language']
            except:
                language = 'ERROR'
        splitted_data[i].append(language)
        i += 1
    
    print("****************")
    
    with open("/cs/usr/vitaly92/Desktop/langs_" + path_leaf(argv[1]), "w") as f:
        writer = csv.writer(f)
        writer.writerows(splitted_data)

if __name__ == "__main__":
    main(sys.argv)
