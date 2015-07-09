#/usr/bin/python2.4

import psycopg2
import calendar
from datetime import datetime
import random

try:
    conn = psycopg2.connect("dbname='gameboard' user='gameboarduser' password='123'")
    #print "Ok connected"
except:
    print "I am unable to connect to the database."


#-------------------------------------------------------
# section query generator consumer_id + power_id
#--------------------------------------------------------
cur = conn.cursor()
try:
    cur.execute(""" SELECT DISTINCT pow_usr.consumer_id_id,  pow_u.unit_power_id, pow.power_startdate, pow.power_closedate, pow.updated_at FROM power_userunitanswer AS pow_usr  LEFT JOIN  power_unit  as pow_u ON pow_u.unit_id =  pow_usr.unit_id_id  LEFT JOIN  power_power  as pow ON pow.power_id = pow_u.unit_power_id ORDER BY pow_usr.consumer_id_id """)
except:
    print "I can't SELECT from bar"

rows = cur.fetchall()
print rows 

def get_new_order_number():
    order_number = random.randrange(0, 101, 2)
    today = datetime.now()
    dd = calendar.timegm(today.timetuple())
    return dd+order_number

#-------------------------------------------------------
# insert data for add info
#--------------------------------------------------------
cur = conn.cursor()

try:
    cur.execute("SELECT segment_id FROM users_notificationsuserpowersegment order by segment_id desc limit 1 ")
except psycopg2.Error as e:
    print "I can't SELECT the last insertion"

res = cur.fetchall()

if len(res) != 0:
    segment_id = res[0][0]
    for linea in rows:
        dstart = calendar.timegm(linea[2].timetuple())
        dclose = calendar.timegm(linea[3].timetuple())
        dstart = int(dstart)
        dclose = int(dclose)
        segment_id = segment_id+1
        try:
            cur.execute("INSERT INTO users_notificationsuserpowersegment( segment_id, consumer_id, power_id, power_startdate, power_closedate, power_update_at) VALUES (%s,%s,%s,%s,%s,%s)", (segment_id, linea[0], linea[1], dstart, dclose, linea[4]))
        except psycopg2.Error as e:
            print "error"
            print e.pgerror
else:
    segment_id = 0
    for linea in rows:
        dstart = calendar.timegm(linea[2].timetuple())
        dclose = calendar.timegm(linea[3].timetuple())
        dstart = int(dstart)
        dclose = int(dclose)
        segment_id = segment_id+1
        try:
            cur.execute("INSERT INTO users_notificationsuserpowersegment( segment_id, consumer_id, power_id, power_startdate, power_closedate, power_update_at) VALUES (%s,%s,%s,%s,%s,%s)", (segment_id, linea[0], linea[1], dstart, dclose, linea[4]))
        except psycopg2.Error as e:
            print "error"
            print e.pgerror

conn.commit()
