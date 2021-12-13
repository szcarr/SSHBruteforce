import os
import platform
import time

'''
-------------------------------------------------------MYIMPORTS-------------------------------------------------------
'''

import SSHScanNetwork

'''
-------------------------------------------------------PROGRAMS-------------------------------------------------------
'''

#def archiveTXTfilesInknownIPs():

#def deleteTXTfilesInknownIPs():

def detectOS():
    #os detection
    splitBy = "\\"
    if str(platform.system()) == "Linux":
        splitBy = '/'
    elif str(platform.system()) == "Windows":
        splitBy = '\\'
    elif str(platform.system()) == "Darwin":
        #Darwin is macOS
        #I dont know what it is files is separeted by
        splitBy = '/'
    return splitBy

'''
-------------------------------------------------------FILES-------------------------------------------------------
'''

def getPathToCurrentDir():
    #nameOfParentFolder & fileToFind should be a string with the raw name of the file
    #Example:
    #nameOfParentFolder = 'foo'
    #fileToFind = 'bar.txt'
    #fileToFind needs to have its name with file extension

    #splitBy is used to define what the file path should be split by
    #Windows uses \\
    #Linux uses /

    pathInList = os.path.abspath(".")

    listWithPossiblePlaces = []
    fileToFind = os.path.basename(__file__)
    nameOfParentFolder = "src"

    for r,d,f in os.walk(pathInList): 
        #Gets all the places where the about.txt file could be located
        for files in f:
            if files == fileToFind:
                listWithPossiblePlaces.append(str(os.path.join(r,files)))

    splitBy = detectOS()

    actualPath = ""
    for i in range(len(listWithPossiblePlaces)):
        pathSplitted = listWithPossiblePlaces[i].split(splitBy)
        if pathSplitted[len(pathSplitted) - 1] == fileToFind and pathSplitted[len(pathSplitted) - 2] == nameOfParentFolder:
            stringConstruction = listWithPossiblePlaces[i].split(splitBy)
            for i in range(len(stringConstruction)):
                if stringConstruction[i] == fileToFind:
                    break
                actualPath = actualPath + stringConstruction[i] + splitBy

    return actualPath

def getAmountOfLinesInFile(nameOfFile):
    #nameOfFile needs to include the file extension and needs the entire path to the file
    #Example of string that can be passed as an argument
    #/home/scp092/Documents/Program/SSHBruteforce/src/usernames.txt

    file = open(nameOfFile, "r")
    line_count = 0

    for line in file:
        if line != "\n":
            line_count += 1
    file.close()

    return line_count

def removeFile(pathAndFilename):
    if os.path.exists(pathAndFilename):
        os.remove(pathAndFilename)
        print("Removing file named: " + pathAndFilename)
    else:
        print("File: " + pathAndFilename + " does not exist.")
    

'''
-------------------------------------------------------TXT HANDLING-------------------------------------------------------
'''

def createTXTFileInSpecifiedDir(nameOfFile, path):
    #Creates a txt file at specified location
    #nameOfFile can not have .txt at end of name
    filePath = os.path.join(path, nameOfFile)
    if not os.path.isfile(filePath):
        #File does not exist, then creates the file
        f = open(filePath + ".txt", "x")
    else:    
        return -1
        #Else file already exists

def addTextToSpecifiedFile(nameOfFile, path, lineToAdd):
    filePath = os.path.join(path, nameOfFile)
    if os.path.isfile(filePath):
        file_object = open(filePath, 'a')
        # Append 'hello' at the end of file
        file_object.write(lineToAdd)
        # Close the file
        file_object.close()
    else:
        print("File does not exist")

def addIPsToListOfIPs():
    for ip in SSHScanNetwork.getListWithIpsOfOpenSSHPorts():
        addTextToSpecifiedFile('listOfIPs.txt', getPathToCurrentDir(), ip + "\n")

'''
-------------------------------------------------------MAIN-------------------------------------------------------
'''

#print(getAmountOfLinesInFile(getPathToCurrentDir() + "rockyou2.txt"))
removeFile(getPathToCurrentDir() + 'listOfIPs.txt')
#time.sleep(2)
createTXTFileInSpecifiedDir('listOfIPs', getPathToCurrentDir())
addIPsToListOfIPs()