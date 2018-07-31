import urllib2
import time as t
import Adafruit_ADS1x15
import os
from firebase import firebase
import RPi.GPIO as GPIO
import datetime

########################################################################

config = open('/home/pi/Desktop/farmconfig', 'r')
farmID = config.readline().rstrip('\n')
farmName = config.readline().rstrip('\n')
farmECThreshold = config.readline().rstrip('\n')
farmPHThreshold = config.readline().rstrip('\n')
farmECIntensity = config.readline().rstrip('\n')
farmPHIntensity = config.readline().rstrip('\n')
farmHighECAlert = config.readline().rstrip('\n')
farmLowPHAlert = config.readline().rstrip('\n')
farmVolume = config.readline().rstrip('\n')
print('finish config')
config.close()

GPIO.setmode(GPIO.BCM)
pinList = [4, 17, 18, 22, 23, 27]
for i in pinList:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.HIGH)


GPIO.output(22, GPIO.LOW)
t.sleep(3)
GPIO.output(22, GPIO.HIGH)

########################################################################

internetFlag = False
internetIndex = 0
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1

size = 100
reading = [0] * size
index = 0
warehouseLen = 10
warehouse = [0.0] * warehouseLen

arrayLength = 40
phArray = [0.0] * arrayLength
phIndex = 0
storageLen = 10
storage = [0.0] * storageLen

########################################################################

def internet():
    global internetFlag, internetIndex
    try:
        x = urllib2.urlopen('http://www.google.com/', timeout=20)
        print('peanut')
        internetFlag = True
        internetIndex = 0
        return
    except urllib2.URLError as err: pass
    print('butter')
    if internetIndex == 0:
        os.system('sudo wifi-connect -d 192.168.42.2,192.168.42.254')
        internetIndex == 1
    internetFlag = False

def ec():
    global warehouse, index
    analogSampleTime = int(round(t.time() * 1000))
    printTime = int(round(t.time() * 1000))
    analogSampleInterval = 25
    printInterval = 700
    analogValueTotal = 0
    analogAverage = 0
    averageVoltage = 0
    ecCurrent = 0
    temperature = 25.0
    counter = 0
    for i in range(len(reading)):#
        reading[i] = 0.0
    for i in range(len(warehouse)):
        warehouse[i] = 0.0
    while counter < len(warehouse):
        if (int(round(t.time() * 1000)) - analogSampleTime >= analogSampleInterval):
            analogSampleTime = int(round(t.time() * 1000))
            analogValueTotal = analogValueTotal - reading[index]
            reading[index] = adc.read_adc(3, gain = GAIN)
            analogValueTotal += reading[index]
            index += 1
            if index >= size:
                index = 0
            analogAverage = analogValueTotal / size
        if (int(round(t.time() * 1000)) - printTime >= printInterval):
            printTime = int(round(t.time() * 1000))
            averageVoltage = analogAverage * float(5000/1024)       
            coefficientVoltage = float(averageVoltage / temperature)
            if(coefficientVoltage <= 448):
                ecCurrent = 6.84 * coefficientVoltage - 64.32
            if(coefficientVoltage <= 1457):
                ecCurrent = 6.98 * coefficientVoltage -127
            else:
                ecCurrent = 5.3 * coefficientVoltage  + 2278
            ecCurrent /= 1000
            warehouse[counter] = ecCurrent
            counter += 1
    summation = sum(warehouse)/len(warehouse)
    return(summation)

def ph():
    global phArray, arrayLength,phIndex
    summation = 0.0
    for i in range(len(storage)):
        storage[i] = 0.0
    counter = 0
    thesamplingTime = int(round(t.time() * 1000))
    theprintTime = int(round(t.time() * 1000))
    while counter < len(storage):
        if(int(round(t.time() * 1000)) - thesamplingTime >= 20):
            phArray[phIndex] = adc.read_adc(2, gain = GAIN)
            if(phIndex == arrayLength):
                phIndex = 0
            voltage = (sum(phArray)/arrayLength) * (5.0/1024)
            phValue = 3.5 * voltage
            thesamplingTime = int(round(t.time() * 1000))          
        if(int(round(t.time() * 1000)) - theprintTime >= 800):
            storage[counter] = phValue
            counter += 1
            theprintTime = int(round(t.time() * 1000))
    summation = sum(storage)/len(storage)
    return (summation)

def firebaseConfig():
    global farmID, farmName, farmECThreshold, farmPHThreshold, farmECIntensity, farmPHIntensity, farmHighECAlert, farmLowPHAlert, farmVolume
    fb = firebase.FirebaseApplication('https://thesmartfarm-7f3a5.firebaseio.com', None)
    res = fb.get(farmID, None)
    #print (res)
    
    getName = res['name']
    getECThreshold = res['ecTreshold']
    getPHThreshold = res['phTreshold']
    getECIntensity = res['EcIntensity']
    getPHIntensity = res['pHIntensity']
    getHighECAlert = res['highECAlert']
    getLowPHAlert = res['lowpHAlert']
    getVolume = res['volume'] 
    if(getName !=farmName):
        farmName = getName
    if(getECThreshold !=farmECThreshold):
        farmECThreshold = getECThreshold
    if(getPHThreshold !=farmPHThreshold):
        farmPHThreshold = getPHThreshold
    if(getECIntensity !=farmECIntensity):
        farmECIntensity = getECIntensity
    if(getPHIntensity !=farmPHIntensity):
        farmPHIntensity = getPHIntensity
    if(getHighECAlert !=farmHighECAlert):
        farmHighECAlert = getHighECAlert
    if(getLowPHAlert !=farmLowPHAlert):
        farmLowPHAlert = getLowPHAlert
    if(getVolume !=farmVolume):
        farmVolume = getVolume
    rewrite = open('/home/pi/Desktop/farmconfig', 'w')
    rewrite.write(farmID + '\n')
    rewrite.write(farmName + '\n')
    rewrite.write(str(farmECThreshold) + '\n')
    rewrite.write(str(farmPHThreshold) + '\n')
    rewrite.write(str(farmECIntensity) + '\n')
    rewrite.write(str(farmPHIntensity) + '\n')
    rewrite.write(str(farmHighECAlert) + '\n')
    rewrite.write(str(farmLowPHAlert) + '\n')
    rewrite.write(str(farmVolume))
    rewrite.close()

def sendFirebase(ecVal, phVal):
    global farmID
    fb = firebase.FirebaseApplication('https://thesmartfarm-7f3a5.firebaseio.com', None)
    database = farmID + 'Data'
    print(database)
    result = fb.post('/' + database + '/value', {'ec': ecVal, 'ph': phVal, 'time': datetime.datetime.now().strftime('%a %b %d %H:%M:%S %Y')})

def fixEC(ecVal):
    global farmECThreshold, farmECIntensity, farmVolume
    volumeNeed = ((float(farmECThreshold) - ecVal)/float(farmECIntensity)) * float(farmVolume)
    print('volumeNeed = ' , volumeNeed)
    GPIO.output(4, GPIO.LOW)
    t.sleep(int(volumeNeed))
    GPIO.output(4, GPIO.HIGH)
    t.sleep(float(farmVolume))
    GPIO.output(17, GPIO.LOW)
    t.sleep(int(volumeNeed))
    GPIO.output(17, GPIO.HIGH)

def fixPH(phVal):
    global farmPHThreshold, farmPHIntensity, farmVolume
    volumeNeed = ((float(farmPHThreshold) - phVal)/float(farmPHIntensity)) * float(farmVolume)
    GPIO.output(18, GPIO.LOW)
    t.sleep(int(volumeNeed))
    GPIO.output(18, GPIO.HIGH)

def ecHigh(ecVal):
    global farmECThreshold, internetFlag, farmID
    fb = firebase.FirebaseApplication('https://thesmartfarm-7f3a5.firebaseio.com', None)
    print('inside ecHigh function')
    print('ecVal = ', ecVal)
    print('farmECThreshold', farmECThreshold)
    if(float(ecVal) > (float(farmECThreshold) + 0.2)):
        print('in first if')
        internet()
        print('finish check internet')
        if (internetFlag == True):
            result = fb.put(farmID, 'highECAlert', True)
        print('send data to firebase')
        GPIO.output(22, GPIO.LOW)
        print('light up warning at the box')
        farmHighECAlert = True
        with open('/home/pi/Desktop/farmconfig', 'r') as file:
            data = file.readlines()
        data[6] = str(True) + '\n'
        with open('/home/pi/Desktop/farmconfig', 'w') as file:
            file.writelines(data)
    if((float(ecVal) + 0.2) < float(farmECThreshold)):
        GPIO.output(22, GPIO.HIGH)
        farmHighECAlert = False
        with open('/home/pi/Desktop/farmconfig', 'r') as file:
            data = file.readlines()
        data[6] = str(False) + '\n'
        with open('/home/pi/Desktop/farmconfig', 'w') as file:
            file.writelines(data)
        internet()
        if(internetFlag == True):
            result = fb.put(farmID, 'highECAlert', False)
        print('calling fixEC')
        fixEC(ecVal)

def phLow(phVal):
    global farmPHThreshold, internetFlag, farmID
    fb = firebase.FirebaseApplication('https://thesmartfarm-7f3a5.firebaseio.com', None)
    if(float(phVal) < float(farmPHThreshold)):
        internet()
        if(internetFlag == True):
            result = fb.put(farmID, 'lowpHAlert', True)
        GPIO.output(22, GPIO.LOW)
        farmLowPHAlert = True
        with open('/home/pi/Desktop/farmconfig', 'r') as file:
            data = file.readlines()
        data[7] = str(True) + '\n'
        with open('/home/pi/Desktop/farmconfig', 'w') as file:
            file.writelines(data)
    else:
        GPIO.output(22, GPIO.HIGH)
        farmLowPHAlert = False
        with open('/home/pi/Desktop/farmconfig', 'r') as file:
            data = file.readlines()
        data[7] = str(False) + '\n'
        with open('/home/pi/Desktop/farmconfig', 'w') as file:
            file.writelines(data)
        internet()
        if(internetFlag == True):
            result = fb.put(farmID, 'lowpHAlert', False)
        fixPH(phVal)

########################################################################

def peanut():
    while internetFlag==False:
        internet()

########################################################################

timeFlag = 0
timeStart = int(round(t.time() * 1000))
peanut()

while True:
    firebaseConfig()
    GPIO.output(23, GPIO.LOW)
    t.sleep(5)
    tempEC = ec()
    GPIO.output(23, GPIO.HIGH)
    GPIO.output(27, GPIO.LOW)
    t.sleep(5)
    tempPH = ph()
    GPIO.output(27, GPIO.HIGH)
    while tempEC < 0:
        tempEC = ec()
        print(tempEC)
    print('finish taking samples')
    ecFile = open('/home/pi/Desktop/ecFile', 'a')
    ecFile.write(str(tempEC) + '\n')
    ecFile.close()
    phFile = open('/home/pi/Desktop/phFile', 'a')
    phFile.write(str(tempPH) + '\n')
    phFile.close()
    print('finish saving samples')
    phLow(tempPH)
    print('pass phlow')
    ecHigh(tempEC)
    print('pass echigh')
    print('finish validating')
    timeFlag = int(round(t.time() * 1000))
    print('timeFlag - timeStart = ' , timeFlag - timeStart)
    if(timeFlag - timeStart > 60000):
        timeStart = int(round(t.time() * 1000))
        with open('/home/pi/Desktop/ecFile', 'r') as file:
            sendEC = file.readlines()
        with open('/home/pi/Desktop/phFile', 'r') as file:
            sendPH = file.readlines()
        print(sendEC)
        print(sendPH)
        sendECAVG = sum(map(float,sendEC))/len(sendEC)
        sendPHAVG = sum(map(float,sendPH))/len(sendPH)
        sendFirebase(sendECAVG, sendPHAVG)
        cleanEC = open('/home/pi/Desktop/ecFile', 'w')
        cleanEC.write('')
        cleanEC.close()
        cleanPH = open('/home/pi/Desktop/phFile', 'w')
        cleanPH.write('')
        cleanPH.close()




    
