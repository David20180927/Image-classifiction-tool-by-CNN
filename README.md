# Image-classifiction-tool-by-CNN
An easy-to-use tool for real time image classification

Information: 1- This program run on window and linux, but you have to manualy install all the requirement python package.\n
             2- This program is just basic function and you are free to add or remove any code.

The example of directory of this tool is




![tree](https://user-images.githubusercontent.com/43640535/147842942-37afb7ab-7db6-435b-b54f-83a9ba75a43c.PNG)

STEP 0
Make sure you have python 3++ install in your PC, and all the package is downloaded (For Window users, you may run "Run_this_to_install_all_requirement.bat" to auto install all requirement

STEP 1
Input your source of data. You may manualy drag your image into dataset, or use my lovely data collecting tool "data_img_collect.py" to automatically capturing it through camera. If your choose former, you may put all image of a certain category to one folder, and name the folder as the category name, and put all of them into /dataset/. Example is given on top.

If you choose later, the collecting tool is very easy to use. Just follow the instruction. Mua~

STEP 2
Once you finished the data preparation, you can now run "CNN_train.py" to train your model. You can also change the model and layer setting if you wish.

STEP 3
Wait till the training process finish

STEP 4
Run "Object_detection.py" to see the result. 


