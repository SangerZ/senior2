'''
import time
import Adafruit_ADS1x15
import pymysql

adc = Adafruit_ADS1x15.ADS1115()

arrayLength = 100
phArray = [0.0] * arrayLength
index = 0

ecArray = [0.0] * arrayLength

phValue = 0.0
ecValue = 0.0
compensation = 1
GAIN = 1

db = pymysql.connect("localhost", "root", "009564", "Status")
cursor = db.cursor()
        #sql = "UPDATE ecphCurrent SET ec={}, ph={} WHERE id=1".format(ecValue, phValue)
sql = "UPDATE ecphCurrent SET ec=2, ph=3 WHERE id=1"
print(sql)
try:
    cursor.commit(sql)
    db.commit()
    print("commit")
except:
    db.rollback()
    print("fail")
    db.close()

while True:
    phArray[index] = adc.read_adc(0, gain = GAIN)
    #print(phArray[index])
    ecArray[index] = adc.read_adc(1, gain = GAIN)
    index += 1
    time.sleep(0.02)
    if index == arrayLength:
        index = 0
        
        voltagePH = (sum(phArray)/arrayLength) * (5.0/1024)
        phValue = 3.5 * voltagePH
        #phValue = voltagePH

        voltageEC = (sum(ecArray)/arrayLength) * (5.0/1024)
        
        coefficientVol = float(voltageEC/25.0)
        if coefficientVol < 150:
            #no solution
            print("no solution")
        elif coefficientVol > 3300:
            #out of range
            print("out of range")
        elif coefficientVol <= 448 and coefficientVol > 150:
            ecValue = 6.84 * coefficientVol - 64.32
        elif coefficientVol <= 1457 and coefficientVol > 448:
            ecValue = 6.98 * coefficientVol - 127
        else:
            ecValue = 5.3 * coefficientVol + 2278
        ecValue /= 1000
        ecValue = ecValue / compensation / 1000.0
        
        #ecValue = voltageEC
        print(ecValue)
        print(phValue)
        db = pymysql.connect("localhost", "root", "009564", "Status")
        cursor = db.cursor()
        #sql = "UPDATE ecphCurrent SET ec={}, ph={} WHERE id=1".format(ecValue, phValue)
        sql = "UPDATE ecphCurrent SET ec=2, ph=3 WHERE id=1"
        print(sql)
        try:
            cursor.commit(sql)
            db.commit()
            print("commit")
        except:
            db.rollback()
            print("fail")
        db.close()
'''
import pymysql
import time
import Adafruit_ADS1x15


def mapping(val, valmin, valmax, newvalmin, newvalmax):
    return (val-valmin) * (newvalmax - newvalmin) / (valmax - valmin) + newvalmin


adc = Adafruit_ADS1x15.ADS1115()
arrayLength = 100
phArray = [0.0] * arrayLength
index = 0

ecArray = [0.0] * arrayLength

phValue = 0.0
ecValue = 0.0
compensation = 1
GAIN = 1

while True:
    phArray[index] = adc.read_adc(1, gain = GAIN)
    ecArray[index] = adc.read_adc(0, gain = GAIN)
    #print("pre")
    #print(phArray[index])
    phArray[index] = mapping(phArray[index], 0, 32767, 0, 4096)
    ecArray[index] = mapping(ecArray[index], 0, 32767, 0, 4096)
    #print("post")
    #print(phArray[index])
    index += 1
    if index == arrayLength:
        index = 0
        
        voltagePH = (sum(phArray)/arrayLength)/1000
        phValue = 3.5 * voltagePH

        voltageEC = (sum(ecArray)/arrayLength)
        #print("voltage")
        #print(voltagePH)
        #print("coefficient")
        coefficientVol = float(voltageEC/1.0)
        #print(coefficientVol)
        if coefficientVol < 150:
            #no solution
            print("no solution")
        elif coefficientVol > 3300:
            #out of range
            print("out of range")
        elif coefficientVol <= 448 and coefficientVol > 150:
            ecValue = 6.84 * coefficientVol - 64.32
        elif coefficientVol <= 1457 and coefficientVol > 448:
            ecValue = 6.98 * coefficientVol - 127
        else:
            ecValue = 5.3 * coefficientVol + 2278
        #ecValue /= 1000
        ecValue = ecValue / compensation / 1000.0
        print(phValue)
        print(ecValue)
        phStr = str(phValue)
        ecStr = str(ecValue)
        
        db = pymysql.connect("localhost","root","009564","Status" )
        cursor = db.cursor()

        sql = "UPDATE ecphCurrent SET ec = " + ecStr + ", ph = " + phStr + " WHERE ID > 0"

        try:
           cursor.execute(sql)
           db.commit()
           print("finish")

        except:
           db.rollback()
           print("fail")

        db.close()
        


    
