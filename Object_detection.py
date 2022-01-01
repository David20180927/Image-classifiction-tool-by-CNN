import cv2
import numpy as np
import os
from PIL import Image # For handling the images
"""AI"""
from keras.models import model_from_json#
from tensorflow.keras.models import load_model
dirmodel = 'model/'
dirdata = 'dataset/'
label = {}
text_font = cv2.FONT_HERSHEY_COMPLEX
def find_label(predictions, label):
    p = predictions[0]
    for i in range(len(label)):
        if p[i]: # if p[i] = 1, then the i is the location in the array
            return label[i] #return the location dict
        
def import_label(label): 
    count = 0
    for i in os.listdir(dirdata):
        label[count] = i
        count += 1
    return label

def preprocess_bf_handover(img):
    img = Image.fromarray(img).convert('L')
    img = img.resize((320, 120))    
    x = [np.array(img)]
    x = np.array(x, dtype = 'float32')
    x = x.reshape((1, 120, 320, 1))
    x /= 255
    return x
    

if __name__ == "__main__":
    print("Loading pretrained model\n")
    json_file = open(dirmodel+'model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)   
    loaded_model.load_weights(dirmodel+"model.h5")
    label = import_label(label) #import all the label as a dictionary for indexing
    print("Loaded model from disk\nOpening camera\n")
    cap = cv2.VideoCapture(0)
    while True:
        success, raw_img = cap.read()
        img = raw_img #raw_img is for model processing, we only add text at img to prevent misreading
        x = preprocess_bf_handover(raw_img)
        ges = find_label((loaded_model.predict(x) > 0.5).astype("int32"),label) #predict the label, and index it to get the str
        cv2.putText(img,'Label: '+str(ges),(80,40),text_font,1.2,(255,255,0),3)
        cv2.imshow("img", img)#show everythings
        if cv2.waitKey(1) & 0xFF == ord("q"): #press q to exit
            break
    cap.release()
    cv2.destroyAllWindows()