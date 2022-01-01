import numpy as np
import cv2
import os
import shutil
from PIL import Image # For handling the images
import time
dirmodel = 'model/'
dirdata = 'dataset/'
choise = 0
label = {}
text_font = cv2.FONT_HERSHEY_COMPLEX

'''This program is not so polished, it might have some reduntant expression and not so robust'''
'''Well, as long as it works, right? hehe'''
def create_label():
    labelname = str(input("Enter new label name: "))
    for i in os.listdir(dirdata):
        if i:
            if (i == labelname):
                print('Label existed\n')
                return
    if labelname:
        os.mkdir(dirdata+labelname)
        print("\nLabel created\n")
    return
def check_label():
    print("The labels in database include:\n")
    for i in os.listdir(dirdata):
        count = 0
        if i:  
            for j in os.listdir(dirdata+str(i)):
                if j:
                    count += 1
                else:
                    count = 0
            print('Label name: '+str(i)+'   data_size: '+str(count))  
    return
def add_data():
    c,count,p,b = 0,0,0,0
    TIMER = int(5)
    labelname = str(input("Enter label name: "))
    for i in os.listdir(dirdata):
        if i:
            if (i == labelname):
                for j in os.listdir(dirdata+str(i)):
                    if j:
                        count += 1
                    else:
                        count = 0                
                direc = dirdata+labelname
                cap = cv2.VideoCapture(0) #capture video
                cap.set(3,1366) 
                cap.set(4,500)
                while True:
                    prev = time.time()
                    while TIMER >= 0:
                        success, img = cap.read()
                        raw_img = img
                        cv2.putText(img,'Timer: '+str(TIMER),(80,40),text_font,1.2,(255,255,0),3)
                        cv2.putText(img,'Stop : S',(80,120),text_font,1.2,(255,0,0),3)
                        cv2.putText(img,'Label: '+str(labelname),(900,40),text_font,1.2,(255,0,255),3)
                        cv2.putText(img,'img captured: '+str(c),(900,80),text_font,1.2,(0,0,255),3)
                        cv2.imshow("img", img)                                 
                        if cv2.waitKey(1) & 0xFF == ord("s"):
                            break
                        cur = time.time()
                        if cur-prev >= 1:
                            prev = cur
                            TIMER = TIMER-1                        
                    else:   
                        cv2.imwrite(direc+"/frame%d.png" % (count+c+1), raw_img)
                        c += 1
                        TIMER = int(1)
                return
    print('Error')
    return
def clear_data():
    labelname = str(input("Enter label name: "))
    for i in os.listdir(dirdata):
        if i:
            if (i == labelname):
                shutil.rmtree(dirdata+str(i))
                os.mkdir(dirdata+labelname)
                print('\n'+labelname+' data cleared\n')
                
                return
    print('Error')
    return

def delete_label():
    labelname = str(input("Enter label name: "))
    for i in os.listdir(dirdata):
        if i:
            if (i == labelname):
                try:
                    os.rmdir(dirdata+str(i))
                except:
                    print('it is not empty, clear it first')
                else:
                    print('\n'+labelname+' removed\n')
                return
    print('Error')
    return

options1 = {1 : create_label,
           2 : check_label,
           3 : add_data,
           4 : clear_data,
           5 : delete_label,
}
if __name__ == "__main__":

    while(choise is not 1):
        try:
            choise = int(input("\nChoose action by entering interger:\n1-Create a new label\n2-See current label list\n3-Add data into an existed label\n4-Clear data of an label\n5-Delete a label\n"))
            options1[choise]()            
        except:
            print("\n...Again mate, something is not right")
            continue
        cv2.destroyAllWindows()  
