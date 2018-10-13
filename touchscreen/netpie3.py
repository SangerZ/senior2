import microgear.client as microgear
import logging
import time
import random
import pymysql

counter = 0
value = 0
otherValue = 0

appid = "HydroSmartFarm"
gearkey = "lqeDWZIACnZIMh6"
gearsecret =  "IQdRfzzTS6syfiizgbOsJH0LJ"

microgear.create(gearkey,gearsecret,appid,{'debugmode': True})

def connection():
    logging.info("Now I am connected with netpie")

def subscription(topic,message):
    logging.info(topic+" "+message)

def disconnect():
    logging.info("disconnected")

microgear.setalias("5735451")
microgear.on_connect = connection
microgear.on_message = subscription
microgear.on_disconnect = disconnect
microgear.connect()

while True:
    db = pymysql.connect("localhost","root","009564","Status" )
    cursor = db.cursor()
    sql= "SELECT ec, ph FROM ecphCurrent WHERE id=1"
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        value = result[0]
        otherValue = result[1]
    except:
        value = 0.0
        otherValue = 0.0

    result = (str(value) + "," + str(otherValue))
    microgear.publish("/status/5735451", result)
    logging.info(result)

    time.sleep(4)
