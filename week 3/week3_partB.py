from grovepi import *
from grove_rgb_lcd import *
from time import sleep
from math import isnan
import datetime

import mysql.connector as mariadb

dht_sensor_port = 7 # connect the DHt sensor to port 7
sound_sensor = 2 # connect the sound sensor to port 2
dht_sensor_type = 0 # use 0 for the blue-colored sensor and 1 for the white-colored sensor

# set green as backlight color
# we need to do it just once
# setting the backlight color once reduces the amount of data transfer over the I2C line
setRGB(0,255,0)


global c
global db
def main():
    while True:
        try:
            # get the temperature and Humidity from the DHT sensor
            # get the sound level from the sound sensor
            [ temp,hum ] = dht(dht_sensor_port,0)
            sound_level = analogRead(sound_sensor)
            print("temp =", temp, "C\thumidity =", hum,"%")

            # set the values to string for output
            t = str(temp)
            h = str(hum)
            s = str(sound_level)
            
            # instead of inserting a bunch of whitespace, we can just insert a \n
            # we're ensuring that if we get some strange strings on one line, the 2nd one won't be affected
            setText("Tem:" + t + "Hum:" + h + "\n" + "Sound:" + s)

            # Use python package datetime to get the current time Hr/Min/Sec
            timestamp = (datetime.datetime.fromtimestamp(time.time()).strftime("%H:%M:%S"))
            
            # output to shell
            print (t + " - "  + h + " - " + s + " - " + timestamp)
            # The SQL command to insert data into our table
            # It uses variable strings(%s) which can be assigned by some other strings later on
            sql =  "INSERT INTO Temp_Hum_Sound (temperature, humidity, sound, time) VALUES (%s, %s, %s, %s)" 
            try:
                c.execute(sql,( str(t) , str(h), str(s), str(timestamp)))
                print("update database.")
                db.commit()
            except:
                db.rollback()
            #db.close()

        except (IOError, TypeError) as e:
            print("Error")

        # wait some time before re-updating the LCD
        sleep(5)

if __name__ == '__main__':

    db = mariadb.connect(user='root',password='test',database='test1')
    c = db.cursor()
             
    try:
      main()
    except KeyboardInterrupt:
      print ("bye bye...")
      pass  