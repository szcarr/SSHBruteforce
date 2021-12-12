import os
import subprocess

#localIp = ["1", "9", "2", ".", "1", "6", "8", ".", "1", "."]

#nmap -p 22 192.168.1.0/24 --open | grep "report for" | awk -F' ' '{print $5}'

def filterNmapOutput():
    #Returns list with ips that have an open SSH port

    ip = str(getMyIp())
    subnett = [char for char in ip]
    subnettMask = subnett[len(subnett) - 3] + subnett[len(subnett) - 2] + subnett[len(subnett) - 1]
    counter = 0
    baseIP = ""
    for i in range(len(subnett)):
        baseIP = baseIP + subnett[i]
        if subnett[i] == ".":
            counter = counter + 1
            print(counter)
        if counter == 3:
            break
    
    baseIP = baseIP + "0" + subnettMask

#    nmapOutput = os.popen("nmap -p 22 192.168.1.0/24 --open | grep 'report for' | awk -F' ' '{print $5}'").read()
    nmapOutput = os.popen("nmap -p 22 " + baseIP + " --open | grep 'report for' | awk -F' ' '{print $5}'").read()
    ipSingleString = ""
    listWithIpsOfOpenSSHPorts = []
    counter = 0
    for char in nmapOutput: #Makes it to a single string
        counter = counter + 1
        if counter > 15 and char == "\n": #Too large to be an Ipv4 Address then it is discarded
            ipSingleString = "" 
            counter = 0
            continue
        if char == "\n":
            listWithIpsOfOpenSSHPorts.append(ipSingleString)
            ipSingleString = ""
            counter = 0
            continue
        ipSingleString = ipSingleString + char #Constructing string

    return listWithIpsOfOpenSSHPorts

def getMyIp():
    #Dynamically returns my IP
    output = os.popen("ip a | grep 'inet ...' | awk -F' ' '{print $2'}").read()
    ipSingleString = ""
    ipList = []
    for c in output: #Makes it to a single string
        if c == "\n":
            ipList.append(ipSingleString)
            ipSingleString = ""
            continue
        ipSingleString = ipSingleString + c

    return ipList[1]