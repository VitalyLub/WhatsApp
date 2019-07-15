import requests
import base64
from os import listdir
from os.path import isfile, join
import sys
import json

URL = "https://vision.googleapis.com/v1/images:annotate?key=AIzaSyD6c1lDKWSF6xnK9u_Hu3Lv7KUFU2G1fwI"
image = "/cs/usr/vitaly92/Desktop/faulkner.jpg"

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read())




def image_request(image_path):
    data = {
            "requests":[
                        {
                        "image":{
                            "content":encode_image(image_path)
                                },
                        "features":[
                                    {
                                     # LABEL_DETECTION FACE_DETECTION LOGO_DETECTION CROP_HINTS
                                    "type":"WEB_DETECTION",
                                    "maxResults": 10
                                    }
                                   ]
                        }
                    ]
}
    r = requests.post(URL, json = data)
    # print(r.status_code)
    return r.text

def main(argv):
    images = [f for f in listdir(argv[1]) if isfile(join(argv[1], f))]
    
    i = 0
    while i < len(images):
        images[i] = argv[1] + "/" + images[i]
        i += 1
    
    for image in images:
        print(image)
        api_answer = json.loads(image_request(image))
        
        print(api_answer)
        """
        rows = api_answer['responses'][0]['labelAnnotations']        
        for item in rows:
            print(item)
        """
if __name__ == "__main__":
    main(sys.argv)
