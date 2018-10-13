import time as t
import os
from firebase import firebase
import datetime
import pymysql

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

    fb = firebase.FirebaseApplication('https://thesmartfarm-7f3a5.firebaseio.com', None)
    res = fb.get(farmID, None)
    
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
    if(getPHThreshold !=phT):
        phT = getPHThreshold
    if(getECIntensity !=ecT):
        ecT = getECIntensity
    if(getPHIntensity !=phI):
        phI = getPHIntensity
    if(getHighECAlert !=ecA):
        ecA = getHighECAlert
    if(getLowPHAlert !=phA):
        phA = getLowPHAlert
    if(getVolume !=volumeFarm):
        volumeFarm = getVolume

    db = pymysql.connect("localhost","root","009564","Status" )
    cursor = db.cursor()
    sql= "UPDATE farmConfig SET name="+farmName+",volume="+volumeFarm+",ec="+ecT+",ph="+phT+",ecIntensity="+ecI+",phIntensity="+phI+",ecAlert="+ecA+",phAlert="+phA+" WHERE 1"
    
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()

def sendFirebase():
    global farmID
    theList = 0
    ec = 0.0
    ph = 0.0
    timenow = datetime.now()
    lasthour = datetime.now() - timedelta(hours = 1)
    fb = firebase.FirebaseApplication('https://thesmartfarm-7f3a5.firebaseio.com', None)
    database = farmID + 'Data'
    print(database)
    db = pymysql.connect("localhost","root","009564","Status" )
    cursor = db.cursor()
    sql= "SELECT * FROM ecphHistory WHERE time > "+lasthour+" AND time < "+timenow
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        theList = len(result)
        for row in result:
            ec += row[2]
            ph += row[3]
            
        finalEC = ec/theList
        finalPH = ph/theList
    
        result = fb.post('/' + database + '/value', {'ec': finalEC, 'ph': finalPH, 'time': datetime.datetime.now().strftime('%a %b %d %H:%M:%S %Y')})
    except:
        print("error")

    db.close()



    

