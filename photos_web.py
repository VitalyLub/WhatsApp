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

URL = "https://vision.googleapis.com/v1/images:annotate?key=AIzaSyD6c1lDKWSF6xnK9u_Hu3Lv7KUFU2G1fwI"

#image to base64, which is a long long text
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read())

# delete the .jpeg or .csv from the filesnames
def delete_extensions_from_files_list(lst):
    i = 0
    while i < len(lst):
        lst[i] = lst[i].split(".")[0]
        i += 1
    return lst

#choose random image
def get_random_image_to_proccess(all_files, exist_files):
    exist_files = delete_extensions_from_files_list([f for f in listdir(exist_files) if isfile(join(exist_files, f))])

    files_to_proccess = list(set(all_files) - set(exist_files))
    
    if len(files_to_proccess) == 0:
        return False
    else:
        return random.choice(files_to_proccess)
    


#make api call
def image_request(image_path):
    data = {
            "requests":[
                        {
                        "image":{
                            "content":encode_image(image_path)
                                },
                        "features":[
                                    {
                                     # LABEL_DETECTION FACE_DETECTION LOGO_DETECTION CROP_HINTS WEB_DETECTION
                                    "type":"WEB_DETECTION",
                                    "maxResults": 10
                                    }
                                   ]
                        }
                    ]
}
    r = requests.post(URL, json = data)
    return r.text

#arg = path of folder which unclude a lot of images
def main(argv):
    
    folder_path = '/cs/usr/vitaly92/.++/to_work/camden'
    f = open(folder_path + '_images/out.csv', 'r')
    reader = csv.reader(f)
    phone_numbers = []
    total_counter = 0
    for row in reader:
        total_counter += 1
        if row[2] == 'Face':
            phone_numbers.append(row[0])
    f.close()
    
    
    output_folder_path = "/cs/usr/vitaly92/.++/to_work/camden_web/"    
    #random a image to proccess
    file_to_proccess = get_random_image_to_proccess(phone_numbers, output_folder_path)
    
    
    j = 0
    while(file_to_proccess != False):
        #open an empty file, just because we don't want that another proccess will random this image        
        
        output_path = output_folder_path + str(file_to_proccess) + ".csv" 
        data = []        
        with open(output_path, 'w', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerows(data)
        
        # make API call        
        api_answer = json.loads(image_request(folder_path + '/' + str(file_to_proccess) + ".jpeg"))
        
        #parse api answer        
        try:
            rows = api_answer['responses'][0]['webDetection']['visuallySimilarImages']
            for item in rows:
                data.append([item['url']])
        except:
            print("ERROR:", file_to_proccess)
            print("ERROR:", api_answer)
        
        
        #save real results
        with open(output_path, 'a', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerows(data)
        
        #print the progress        
        if j % 10 == 0:
            print(j)
        j += 1
        file_to_proccess = get_random_image_to_proccess(phone_numbers, output_folder_path)      
        

if __name__ == "__main__":
    main(sys.argv)
