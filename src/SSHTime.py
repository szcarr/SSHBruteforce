'''
-------------------------------------------------------IMPORTS-------------------------------------------------------
'''

import datetime
from datetime import datetime
import time

'''
-------------------------------------------------------MYIMPORTS-------------------------------------------------------
'''

'''
-------------------------------------------------------PROGRAMS-------------------------------------------------------
'''

def getMyLocalTime():
    now = datetime.now().time()
    #Returns a time object
    return now

def getLocalTimeInHoursMinutesSeconds():
    time = str(getMyLocalTime())
    timeList = time.split(":")
    hours, minutes, seconds = int(timeList[0]), int(timeList[1]), float(timeList[2])
    return hours, minutes, seconds

def compareTimeVsStartTime(listWithHoursMinutesSeconds):
    #args passed in function is time right now
    #time right now is compared against time started
    nowSeconds, nowMinutes, nowHours = listWithHoursMinutesSeconds[0], listWithHoursMinutesSeconds[1], listWithHoursMinutesSeconds[2]
    startTimeList = list(startTime)
    #
    startHours, startMinutes, startSeconds = startTimeList[0], startTimeList[1], startTimeList[2]
    #
    actualRuntimeHours, actualRuntimeMinutes, actualRuntimeSeconds = 0, 0, 0
    actualRuntimeHours = nowHours - startHours
    actualRuntimeMinutes = nowMinutes - startMinutes
    actualRuntimeSeconds = nowSeconds - startSeconds
    actualRuntimeDays = 0

    #Seconds
    if nowSeconds < startSeconds:
        nowMinutes = nowMinutes - 1
        actualRuntimeSeconds = nowSeconds + 60 - startSeconds
    else:
        actualRuntimeSeconds = nowSeconds - startSeconds

    #Minutes
    if nowMinutes < startMinutes:
        nowHours = nowHours - 1
        actualRuntimeMinutes = nowMinutes + 60 - startMinutes
    else:
        actualRuntimeMinutes = nowMinutes - startMinutes

    #Hours
    if nowHours < startHours:
       nowHours = nowHours + 24 - startHours
       actualRuntimeDays = actualRuntimeDays - 1
    else:
        actualRuntimeHours = nowHours - startHours

    #Days
    if nowHours >= 24:
        nowHours = nowHours - 24
        actualRuntimeDays += 1

    #print(actualRuntimeDays, actualRuntimeHours, actualRuntimeMinutes, actualRuntimeSeconds)
    print("Start time: ", end="")
    print(round(startHours, 0), round(startMinutes, 0), round(startSeconds, 2))

    print("Time now: ", end="")
    print(round(actualRuntimeHours, 0), round(actualRuntimeMinutes, 0), round(actualRuntimeSeconds, 2))

def convertHoursToMinutes():
    pass

def setStarttime():
    global startTime
    startTime = getLocalTimeInHoursMinutesSeconds()

def getRuntime():
    startTime

'''
-------------------------------------------------------SETUP-------------------------------------------------------
'''

startTime = 0

'''
-------------------------------------------------------MAIN-------------------------------------------------------
'''

setStarttime()
while(True):
    #print(getLocalTimeInHoursMinutesSeconds())
    compareTimeVsStartTime(getLocalTimeInHoursMinutesSeconds())
    time.sleep(1)