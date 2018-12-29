import microgear.client as client
import time
import random
import logging
import pymysql

appid = "HydroSmartFarm"
gearkey = "lqeDWZIACnZIMh6"
gearsecret =  "IQdRfzzTS6syfiizgbOsJH0LJ"

client.create(gearkey,gearsecret,appid,{'debugmode': True})

def connection():
	print ("Now I am connected with netpie")

def subscription(topic,message):
	print (topic+" "+message)

client.setname("doraemon")
client.on_connect = connection
client.on_message = subscription
client.subscribe("/mails")


client.connect()

var1 = 0.0
var2 = 0.0

while True:
    #client.chat("doraemon","Hello world. "+str(int(time.time())))
    #time.sleep(2)

    db = pymysql.connect("localhost", "root", "009564", "Status")
    cursor = db.cursor()
    sql= "SELECT ec, ph FROM ecphCurrent WHERE id=1"
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        var1 = result[0]# + random.uniform(0.0, 0.5) - 0.25
        var2 = result[1]# + random.uniform(0.0,0.5) - 0.25
        answer = ("%.2f"%var1 + "," +"%.2f"%var2)
        
        client.publish("/status/5735451", answer)
        logging.info(answer)
        print(answer)
        time.sleep(4)
        db.close()
    except:
        var1 = 0
        var2 = 0
        db.close
        time.sleep()
    '''
    var1 = round(random.uniform(1.3, 1.4), 2)
    var2 = round(random.uniform(5.5, 5.6), 2)
    result = (str(var1) + "," + str(var2))
    client.publish("/status/5735451", result)
    logging.info(result)
    print(result)
    time.sleep(4)
    '''
