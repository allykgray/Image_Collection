"""
Created on Wed Jul 09 18:20:45 2014

@author: agray
"""
import os
import sys
import urllib
import httplib
import urllib2
import shutil
import numpy as np
import random
from PIL import ImageFile
from PIL import Image
################################ Inputs #######################################
MainDirectory='E:/Ships' #This directory contains all of the ship directories - Imagenet and my homebrew
ImageCategories= MainDirectory+'/ImageNet_Categories/'
WorkingDirectory=MainDirectory+'/CreatingCategories/' # this is where the new category files have been saved and maybe where this *.py file is 
###############################################################################
NewDirectory='/ship_v7/'
NewPath=MainDirectory+NewDirectory
ValidationFolder='val/'
TrainingFolder='train/'
########################### Are you merging Categories? ########################
MERGECATEGORIES='yes' #yes to merge, 'no' to keep same categories and their respective titles 
NumberofMergedCategories=2 ###This requires input text files telling the program which ones to merge
########################### Resize Dimensions #################################
width=256
height=256
ImageFile.LOAD_TRUNCATED_IMAGES = True #allows partially corrupt images to still be processed
############## Creating a New Directory to store your images ##################
print 'Checking to see if your new directory already exists.....'
if os.path.isdir(NewPath):
    print ('Your directory '+NewPath+' already exists and will not be recreated')
#    x=str(raw_input("Where you planning to use this directory? (yes/no)"))
#    if x==str('no'):
#        print 'Program aborted. Change your NewDirectory Parameter. Line 16'
#        sys.exit()
else:
    os.mkdir(NewPath)
    print 'Created New Image Directory' + NewPath
    print NewPath
###############################################################################
###################### Keeping all Categories the Same ########################
    #####################################################################
if MERGECATEGORIES==str('no'):
##See if the new directories exist ---- if they don't create them
##################Create New Category Directoies in NewPath ################
###Get Image Categories###
    Categories=[]
    ListOriginalCategories=os.listdir(ImageCategories)
    for i in range(len(ListOriginalCategories)):
        Categories.append(ListOriginalCategories[i])
    for j in range(len(Categories)):
        if not os.path.exists(NewPath+Categories[j]):
            os.mkdir(NewPath+Categories[j])
################ Copy all of images to your new directories ##################
    Moved=[]
    for k in range(len(Categories)): 
        CatImages=[]
        for FilesInDir in os.listdir(ImageCategories+Categories[k]):
            if FilesInDir.endswith(".JPEG"):
                CatImages.append(Categories[k]+'/'+FilesInDir)
            elif FilesInDir.endswith(".jpg"):
                CatImages.append(Categories[k]+'/'+FilesInDir)
            elif FilesInDir.endswith(".PNG"):
                CatImages.append(Categories[k]+'/'+FilesInDir)
            elif FilesInDir.endswith(".JPG"):
                CatImages.append(Categories[k]+'/'+FilesInDir)
            elif FilesInDir.endswith(".gif"):
                CatImages.append(Categories[k]+'/'+FilesInDir)
            elif FilesInDir.endswith(".tif"):
                CatImages.append(Categories[i]+'/'+FilesInDir)
        for m in range(len(CatImages)):
            B=CatImages[m]
#           if str(B[0:8])!=str(B[10:18]):
#               print B
            try:                
                shutil.copyfile(ImageCategories+B,NewPath+B)
            except:
                print('Warning:'+CatImages[m]+' may not have been moved, you may want to check and see if '+ NewPath+CatImages[m]+
        'exists' )
                Moved.append(CatImages[k]) 
        print 'Done with  '+ Categories[k] + '. There are ' +str(len(CatImages))+ ' images.'
    #del CatImages
###############################################################################
############################# Merged Categories ###############################
elif MERGECATEGORIES==str('yes'):  
################### This requires input files read them in#####################
    NewCategories=[] 
    for NewCategoryFilesInDir in os.listdir(WorkingDirectory):
                if NewCategoryFilesInDir.endswith(".txt"):
                    NewCategories.append(NewCategoryFilesInDir)    
    if len(NewCategories)!=NumberofMergedCategories:
        print('WARNING:Catergory Merging Files (txt) and NumberofMergedCategories variable (line 26) do not match. Will generate new directories based on loaded *.txt files.')
        print(NewCategories)
######################## Create New Category Directories ######################
    for n in range(len(NewCategories)):
        if not os.path.exists(NewPath+NewCategories[n][0:len(NewCategories[n])-4]):
            #This make new directories based on the file names without the *.txt extension
            os.mkdir(NewPath+NewCategories[n][0:len(NewCategories[n])-4])
################ Copy Images to New Directories in New Path ###################
    for m in range(len(NewCategories)):
        DirSerach= open(NewCategories[m], 'r') 
        NewCategoryDirectory=NewPath+NewCategories[m][0:len(NewCategories[m])-4]+"/"
        lines=DirSerach.readlines()
        DirSerach.close()
        Splits=[] #category list
        for i in range(len(lines)):
            Splits.append(lines[i].split(' '))
        Categories=np.array(Splits)[:,0] #this will grab all of the categories 
        AllImages=[]
        for i in range(len(Categories)):
            for FilesInDir in os.listdir(ImageCategories+Categories[i]):
                if FilesInDir.endswith(".JPEG"):
                    AllImages.append(Categories[i]+'/'+FilesInDir)
                elif FilesInDir.endswith(".jpg"):
                    AllImages.append(Categories[i]+'/'+FilesInDir)
                elif FilesInDir.endswith(".PNG"):
                    AllImages.append(Categories[i]+'/'+FilesInDir)
                elif FilesInDir.endswith(".JPG"):
                    AllImages.append(Categories[i]+'/'+FilesInDir)
                elif FilesInDir.endswith(".gif"):
                    AllImages.append(Categories[i]+'/'+FilesInDir)
                elif FilesInDir.endswith(".tif"):
                    AllImages.append(Categories[i]+'/'+FilesInDir)
        for k in range(len(AllImages)):
            B=AllImages[k]
            #print B
#            if str(B[0:8])!=str(B[10:18]):
#                print B
                #mismatch.append(B)
            try:                #shutil.move(Path2ShipTrain+B[0:len(B)-1],Path2ShipVal+B[10:len(B)-1])
                shutil.copyfile(ImageCategories+B,NewCategoryDirectory+"/"+NewCategories[m][0:NewCategories[m].rfind('.')]+'_'+str(k+1)+".jpg")
                #print NewCategoryDirectory+"/"+NewCategories[m][0:len(NewCategories[m])-4]+"_"+str(k+1)+".jpg"
            except:
                print('Check Image'+NewCategoryDirectory+"/"+NewCategories[m][0:len(NewCategories[m])-4]+"_"+str(k+1)+".jpg")
                #Moved.append(AllImages[k]) 
        print 'Done with  '+ NewCategories[m][0:len(NewCategories[m])-4] + '. There are ' +str(len(AllImages))+ ' images.'
        del AllImages        
###############################################################################
##################### Create Train and Val Directories ########################
if os.path.exists(NewPath+TrainingFolder):
    print 'A Train directory already exists. It is being deleted and a new one will be created '+NewPath+TrainingFolder
    shutil.rmtree(NewPath+TrainingFolder, ignore_errors=True)
    os.mkdir(NewPath+TrainingFolder)
else:
    print 'Creating the Train Directory now....'+NewPath+TrainingFolder
    os.mkdir(NewPath+TrainingFolder)
if os.path.exists(NewPath+ValidationFolder):
    print 'A Val directory already exists. It is being deleted and a new one will be created '+NewPath+ValidationFolder
    shutil.rmtree(NewPath+ValidationFolder, ignore_errors=True)
    os.mkdir(NewPath+ValidationFolder)
else:
    print 'Creating the Val Directory now....'+NewPath+ValidationFolder
    os.mkdir(NewPath+ValidationFolder)
if MERGECATEGORIES==str('no'):
     DIRS=Categories
else:
    DIRS=[]
    for i in range(len(NewCategories)):
        DIRS.append(NewCategories[i][0:len(NewCategories[i])-4])
########################### Create Val set ####################################    
FileList=[]
for i in range(len(DIRS)):
    for FilesValDir in os.listdir(NewPath+DIRS[i]):
        if FilesValDir.endswith(".JPEG"):
            FileList.append(DIRS[i]+'/'+FilesValDir)
        elif FilesValDir.endswith(".jpg"):
            FileList.append(DIRS[i]+'/'+FilesValDir)
        elif FilesValDir.endswith(".PNG"):
            FileList.append(DIRS[i]+'/'+FilesValDir)
        elif FilesValDir.endswith(".JPG"):
            FileList.append(DIRS[i]+'/'+FilesValDir)
        elif FilesValDir.endswith(".gif"):
            FileList.append(DIRS[i]+'/'+FilesValDir)
        elif FilesValDir.endswith(".tif"):
            FileList.append(DIRS[i]+'/'+FilesValDir)
InitalNumberofFiles=len(FileList)
ValList=[]
ValChecks=[]
InitialNumofValImages=int((InitalNumberofFiles)*0.15)
ValFiles=len(os.listdir(NewPath+ValidationFolder))
#if InitialNumofValImages==ValFiles:
#    print 'ERROR: You already have a Val directory created with images!!! Delete the Val directory and run this program again.'
#    #os.exit()
Pull=InitialNumofValImages #Number of Val images to pull
while (ValFiles<InitialNumofValImages):    
    for i in range(Pull):
        ValList.append(int(random.uniform(1,len(FileList))))
    for j in range(len(ValList)):
        B=FileList[ValList[j]]
        try:
            shutil.move(NewPath+B,NewPath+ValidationFolder+B[0:B.rfind('/')]+'_'+str(ValList[j])+'.jpg')
            #B.rfind will find the / in the string and using all of the string after this
            #this will likely break if B is comprised of more than a parent directory and the name of an image
            #GOOD = /n50000000/Images.jpg
            #BAD = /n50000000/N555550sub/Images.jpg
            #The category name and its index are passed on to the image when it is moved to the Val folder
        except:
#            print('Possible Duplicate - You may want to make sure that image' +NewPath+B+' has been moved.')
            ValChecks.append(ValList[j])      
            #os.remove(content[i])
        ValFiles=len(os.listdir(NewPath+ValidationFolder))
    NeededVals=InitialNumofValImages-ValFiles
    Pull=NeededVals
    if Pull <=0:
        print 'You need ' +str(InitialNumofValImages)+ ' images in your val directory. You have ' +str(ValFiles)+'. Your Val Directory has been created.'
        break
    else:
        continue
        del FileList
        FileList=[]
        for i in range(len(DIRS)):
            for FilesInDir in os.listdir(NewPath+DIRS[i]):
                if FilesInDir.endswith(".JPEG"):
                    FileList.append(DIRS[i]+'/'+FilesInDir)
                elif FilesInDir.endswith(".jpg"):
                    FileList.append(DIRS[i]+'/'+FilesInDir)
                elif FilesInDir.endswith(".PNG"):
                    FileList.append(DIRS[i]+'/'+FilesInDir)
                elif FilesInDir.endswith(".JPG"):
                    FileList.append(DIRS[i]+'/'+FilesInDir)
                elif FilesInDir.endswith(".gif"):
                    FileList.append(DIRS[i]+'/'+FilesInDir)
                elif FilesInDir.endswith(".tif"):
                    FileList.append(DIRS[i]+'/'+FilesInDir)
        print 'We need to run this loop again, the random number generator used to decide which images to pull for the val set has ' +Pull+' duplicates.'
########### Now Let's Resize and Reorganized our Images ######################
##############################################################################
################## Let's start with the Val Images ###########################
ValResizeList=[]
for ValInDir in os.listdir(NewPath+ValidationFolder):
    if ValInDir.endswith(".jpg"): #Grab only files with *.jpg extenstions. We just added images with only this extension. We are OK :)
        ValResizeList.append(ValInDir)             
for k in range(len(ValResizeList)):
    #print('Resizing image ' + ValResizeList[k])
    img = Image.open(os.path.join(NewPath+ValidationFolder+ValResizeList[k])).convert('RGB')  # Open the image file.
    img_w,img_h=img.size             
    img = img.resize((width, height), Image.CUBIC)    # Resize it.
    img.save(os.path.join(NewPath+ValidationFolder+ValResizeList[k]))
print 'Resizing Val Images Complete.'
#        
################## Let's Resize and Reorganize the Train Set ####################
print 'Resizing and rotating images in train directory............'
## Create New Directories in train then copy, rotate, and save all images as jpg.
for b in range(len(DIRS)):
        if not os.path.exists(NewPath+TrainingFolder+DIRS[b]):
            os.mkdir(NewPath+TrainingFolder+DIRS[b])
#Let's Relist our train files.....I know we have done it a lot already.... 
TrainingSet=[]
for c in range(len(DIRS)):
    for FilesInDir in os.listdir(NewPath+DIRS[c]):
        if FilesInDir.endswith(".JPEG"):
            TrainingSet.append(DIRS[c]+'/'+FilesInDir)
        elif FilesInDir.endswith(".jpg"):
            TrainingSet.append(DIRS[c]+'/'+FilesInDir)
        elif FilesInDir.endswith(".PNG"):
            TrainingSet.append(DIRS[c]+'/'+FilesInDir)
        elif FilesInDir.endswith(".JPG"):
            TrainingSet.append(DIRS[c]+'/'+FilesInDir)
        elif FilesInDir.endswith(".gif"):
            TrainingSet.append(DIRS[c]+'/'+FilesInDir)
        elif FilesInDir.endswith(".tif"):
            TrainingSet.append(DIRS[c]+'/'+FilesInDir)            
for k in range(len(TrainingSet)):
    #print('Resizing image ' + TrainingSet[k])
        # Open the image file.
    img = Image.open(os.path.join(NewPath+TrainingSet[k])).convert('RGB')
    img_w,img_h=img.size             
    # Resize it.
    img = img.resize((width, height), Image.CUBIC)
###################    mirror images  #################################
    img2=img.transpose(Image.FLIP_LEFT_RIGHT)       
    img3=img.transpose(Image.FLIP_TOP_BOTTOM)
    img4=img2.transpose(Image.FLIP_TOP_BOTTOM)
    img.save(os.path.join(NewPath + TrainingFolder+TrainingSet[k][0:TrainingSet[k].rfind('_')]+"_"+str((k+0)+(k*3))+"_256.jpg")) 
    img2.save(os.path.join(NewPath +TrainingFolder+ TrainingSet[k][0:TrainingSet[k].rfind('_')]+"_"+str((k+1)+(k*3))+"_256.jpg"))      
    img3.save(os.path.join(NewPath +TrainingFolder+ TrainingSet[k][0:TrainingSet[k].rfind('_')]+"_"+str((k+2)+(k*3))+"_256.jpg"))   
    img4.save(os.path.join(NewPath +TrainingFolder+ TrainingSet[k][0:TrainingSet[k].rfind('_')]+"_"+str((k+3)+(k*3))+"_256.jpg"))        
print 'Resizing and Rotating of Training Images Complete.'
###############################################################################
######################## Create Val and Train Files ###########################
#################################TRAIN LIST ###################################
TrainImages=[]
train_file=open(NewPath + TrainingFolder+'train.txt','w')
#TrainCats=os.listdir(NewPath + TrainingFolder)
for p in range(len(DIRS)):
    for FilesInTrain in os.listdir(NewPath + TrainingFolder+DIRS[p]):
        if FilesInTrain.endswith(".JPEG"):
            #print p
            TrainImages.append(DIRS[p]+'/'+FilesInTrain+" "+str(p))
            train_file.write(DIRS[p]+'/'+FilesInTrain+" "+str(p)+'\n') 
        if FilesInTrain.endswith(".jpg"):
            #print i+1
            TrainImages.append(DIRS[p]+'/'+FilesInTrain+" "+str(p))
            train_file.write(DIRS[p]+'/'+FilesInTrain+" "+str(p)+'\n')
train_file.close()
################################ VAL LIST #####################################            
ValImageList=[]
val_file=open(NewPath+ValidationFolder+'val.txt','w')
ValImages=os.listdir(NewPath+ValidationFolder)
for k in range(len(ValImages)):
    if ValImages[k].endswith(".jpg"):
        for p in range(len(DIRS)):
            if ValImages[k].rfind(DIRS[p]) >= 0:
                #print p-1
                ValImageList.append(ValImages[k]+" "+str(p))
                val_file.write(ValImages[k]+" "+str(p)+'\n')

val_file.close()   
print 'Train.txt file has been created in ' +NewPath + TrainingFolder+'.'
print 'Val.txt file has been created in ' +NewPath + ValidationFolder+'.'
