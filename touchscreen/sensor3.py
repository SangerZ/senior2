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
        print("ph = %.2f" % phValue)
        print("ec = %.2f" % ecValue)
        phStr = str(round(phValue,2))
        ecStr = str(round(ecValue,2))
        
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

        #history db
        hdb = pymysql.connect("localhost","root","009564","Status" )
        cursor2 = hdb.cursor()
        sql = "INSERT INTO ecphHistory (id, time, ec, ph) VALUES (NULL, CURRENT_TIMESTAMP, "+ ecStr +", "+ phStr +")"
        try:
           cursor2.execute(sql)
           hdb.commit()
           print("finish2")

        except:
           hdb.rollback()
           print("fail2")

        hdb.close()
        


    
