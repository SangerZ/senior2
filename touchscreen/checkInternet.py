import pymysql
import urllib2
import time as t

'''
0 for no internet
1 for internet
2 for no idea
'''
flag = False
index = 0

def checkInternet():
    global flag, index
    db = pymysql.connect("localhost", "root", "009564", "Status")
    cursor = db.cursor()
    sql= "SELECT status FROM machineStatus WHERE name=internet"
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        flag = result[0]
    except:
        flag = False
    db.close()

    if flag:
        try:
            x = urllib2.urlopen('http://www.google.com/', timeout=20)
            #print('peanut')
            flag = True
            return
        except urllib2.URLError as err: pass
        #print('butter')
        if index == 0:
            os.system('sudo wifi-connect -d 192.168.42.2,192.168.42.254')
            index == 1
        flag = False

    
    '''
    db = pymysql.connect("localhost", "root", "009564", "Status")
    cursor = db.cursor()
    sql= "SELECT status FROM machineStatus WHERE name=internet"
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        flag = result[0]
    except:
        flag = 2
    '''
    
