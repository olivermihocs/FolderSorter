#!/usr/bin/env python3
import os
import sys
import json
import shutil

folder_path = ""
reload(sys)
sys.setdefaultencoding('utf-8')

def exitWithMsg(info):
    if len(info):
        print(info)
    print("Shutting down script. In case you want to change folders, modify the folder.json file, or call the script with the path as the first parameter.")
    exit()

def sortFolder(path):
    getUserConfirm(path)
    createDirs(path)

    fileTypes=getFileTypes()
    for e in fileTypes:
        for ex in fileTypes[e]:
            ext="."+ex
            for file in os.listdir(unicode(path)):
                try:
                    if file.lower().endswith(ext):
                        fullPathName=path+"/"
                        fullDestName=path+"/"+e+"/"
                        print("Moving" + file +" to " + fullDestName)
                        shutil.move(fullPathName+file,fullDestName+file)
                except:
                    print("Something happened, Skipping file.")
    print("All files with the defined filetypes in fileTypes.json have been moved.")

def getUserConfirm(path):
    choice=raw_input("Do you want to sort the current folder? ("+path+")\nY/N? ")
    if(choice.lower()!="y"):
        exitWithMsg("")

def getFileTypes():
    try:
        with open('fileTypes.json') as f:
            fileTypes = json.load(f)
            return fileTypes
    except:
        exitWithMsg("fileTypes.json file is missing from the .py file's directory!")
        
#Only getting called from sources that checked if the dir exists.
def createDirs(path):
    fileTypes=getFileTypes()
    print("Creating subfolders...")
    for e in fileTypes:
        dirTarget=path+"/"+e
        if not os.path.exists(dirTarget):
            print(e +  " Created ")
            os.mkdir(dirTarget)
        else:    
            print(e + " already exists")

def updateFolderJSONFile(path):
    data = {}
    data["Folder_path"]=path
    with open('folder.json', 'w') as f:
        json.dump(data, f)
    print("Successfully updated folder's JSON file.")

def getPathFromJSON():
    try:
        with open('folder.json') as f:
            data = json.load(f)
    except:
        exitWithMsg("folder.json file is missing from the .py file's directory!")
    return data["Folder_path"]

def runDefault():
    folder_path=getPathFromJSON()
    if not os.path.isdir(folder_path) or not len(folder_path):
        exitWithMsg("Specified path does not exists")
    else:
        sortFolder(folder_path)

def runChanged():
    folder_path=sys.argv[1]
    if not os.path.isdir(folder_path):
        exitWithMsg("Please enter a valid path. (Existing folder that you want to sort)")
    else:
        updateFolderJSONFile(folder_path)
        sortFolder(folder_path)


if(len(sys.argv)==1): runDefault()
elif(len(sys.argv)==2): runChanged()
else:
    exitWithMsg("Too many parameters given.")