import time as t
import os
from firebase import firebase
from datetime import datetime, timedelta
import pymysql
import json

farmID = ""
farmName = ""
volumeFarm = ""
ecT = ""
phT = ""
ecI = ""
phI = ""
ecA = ""
phA = ""

def dataStd():
    global farmID, farmName, volumeFarm, ecT, phT, ecI, phI, ecA, phA

    db = pymysql.connect("localhost","root","009564","Status" )
    cursor = db.cursor()
    sql= "SELECT * FROM farmConfig"
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        farmID = result[0]
        farmName = result[1]
        volumeFarm = result[2]
        ecT = result[3]
        phT = result[4]
        ecI = result[5]
        phI = result[6]
        ecA = result[7]
        phA = result[8]
        print(result)#
    except:
        farmID = ""
        farmName = ""
        volumeFarm = ""
        ecT = ""
        phT = ""
        ecI = ""
        phI = ""
        ecA = ""
        phA = ""
    db.close()

def getFromFB():
    global farmID, farmName, volumeFarm, ecT, phT, ecI, phI, ecA, phA
    print(farmID)
    fb = firebase.FirebaseApplication('https://thesmartfarm-7f3a5.firebaseio.com', None)
    res = fb.get(str(farmID), None)
    
    getName = res['name']
    getECThreshold = res['ecTreshold']
    getPHThreshold = res['phTreshold']
    getECIntensity = res['EcIntensity']
    getPHIntensity = res['pHIntensity']
    getHighECAlert = res['highECAlert']
    getLowPHAlert = res['lowpHAlert']
    getVolume = res['volume']
    print(res)
    theECA = 0
    thePHA = 0

    if(getHighECAlert):
        theECA = 1
    else:
        theECA = 0
    if(getLowPHAlert):
        thePHA = 1
    else:
        thePHA = 0
    
    if(getName !=farmName):
        farmName = getName
    if(getECThreshold !=ecT):
        ecT = getECThreshold
    if(getPHThreshold !=phT):
        phT = getPHThreshold
    if(getECIntensity !=ecI):
        ecI = getECIntensity
    if(getPHIntensity !=phI):
        phI = getPHIntensity
    if(theECA !=ecA):
        ecA = theECA
    if(thePHA !=phA):
        phA = thePHA
    if(getVolume !=volumeFarm):
        volumeFarm = getVolume

    print(farmName)
    print(ecT)
    db = pymysql.connect("localhost","root","009564","Status" )
    cursor = db.cursor()
    sql = "UPDATE farmConfig SET name=\""+str(farmName)+"\",volume=\""+str(volumeFarm)+"\",ec=\""+str(ecT)+"\",ph=\""+str(phT)+"\",ecIntensity=\""+str(ecI)+"\",phIntensity=\""+str(phI)+"\",ecAlert=\""+str(ecA)+"\",phAlert=\""+str(phA)+"\" WHERE 1"
    print(sql)
    
    try:
        cursor.execute(sql)
        db.commit()
        print("success update")
    except:
        db.rollback()
        print("fail update")
    db.close()
    

def sendFirebase():
    global farmID
    fb = firebase.FirebaseApplication('https://thesmartfarm-7f3a5.firebaseio.com/')
    theList = 0
    ec = 0.0
    ph = 0.0
    timenow = datetime.now()
    lasthour = datetime.now() - timedelta(hours = 1)

    database = str(farmID) + 'Data/value'
    print(database)
    db = pymysql.connect("localhost","root","009564","Status" )
    cursor = db.cursor()
    sql= "SELECT * FROM ecphHistory WHERE time > \'"+str(lasthour)+"\' AND time < \'"+str(timenow)+"\'"
    print(sql)

    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        theList = len(result)
        print(theList)
        for row in result:
            ec += row[2]
            ph += row[3]
        finalEC = ec/theList
        finalPH = ph/theList
        result = fb.post(database,{'ec':str(finalEC), 'ph': str(finalPH), 'time': str(timenow.strftime('%a %b %d %H:%M:%S %Y'))})
        print(result)
    except:
        print('error')

def doitthen():
    dataStd()
    getFromFB()

def senditthen():
    dataStd()
    sendFirebase()

