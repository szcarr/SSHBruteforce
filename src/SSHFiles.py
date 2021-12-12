import os

def findPathToCurrentDir():
    pathInList = os.path.abspath(".")
    
    listWithPossiblePlaces = []
    fileToFind = "bla.sh"
    nameOfParentFolder = "SSHBruteforce"

    for r,d,f in os.walk(pathInList): 
        #Gets all the places where the about.txt file could be located
        for files in f:
            if files == fileToFind:
                listWithPossiblePlaces.append(str(os.path.join(r,files)))

    actualPath = ""
    for i in range(len(listWithPossiblePlaces)):
        myString = listWithPossiblePlaces[i].split("\\")
        if myString[len(myString) - 1] == fileToFind and myString[len(myString) - 2] == nameOfParentFolder:
            stringConstruction = listWithPossiblePlaces[i].split("\\")
            for i in range(len(stringConstruction)):
                if stringConstruction[i] == fileToFind:
                    break
                actualPath = actualPath + stringConstruction[i] + "\\"

    return actualPath 

print(findPathToCurrentDir())