''' tbsense_scan.py - scan for SiLabs BLE Thunderboard Sense 2 boards and read out certain sensor data
    
'''
from bluepy.btle import *
import struct
import time, datetime
import Thunderboard     # Silicon Labs Thunderboard sensor data routines which is in this directory. PYTHONPATH has to include this directory.
import urllib2          # Post data to ThingSpeak.com

# Base URL of Thingspeak
baseURL = 'https://api.thingspeak.com/update?api_key='
# The PRIVATE_KEY is needed to post data to the HBMS page on Thingspeak.com
ThingSpeakKeys = {
        'TB90_fd_9f_7b_4d_27.csv' : 'O2RNOOMHOQAGEHP9', # Outside
        'TB90_fd_9f_7b_81_33.csv' : 'FWFN30ITMBINUXBP', # Inside
        'TB90_fd_9f_7b_81_7e.csv' : 'U1KZMR05RPI04Z8V'  # Ground
        }

# DEBUG=0 turns off messages, the higher the number the more messages are printed to the screen
DEBUG = 5

def getThunderboards():
    ''' Scan for TB2 boards for a few seconds and return all that are found'''
    scanner = Scanner()         # initialize BLE
    devices = scanner.scan(1.1)   # scan for BLE devices for this many seconds
    tbsense = dict()
    for dev in devices:
        scanData = dev.getScanData()
        for (adtype, desc, value) in scanData:
            if desc == 'Complete Local Name':
                if 'Thunder Sense #' in value:              # if the device is a TB2, then add it to tbsense
                    deviceId = int(value.split('#')[-1])
                    tbsense[deviceId] = Thunderboard.Thunderboard(dev)

    return tbsense

def Post2Thingspeak(key, temp, hum, lux, batt):
    f = urllib2.urlopen(baseURL + key + "&field1={}&field2={}&field3={}&field4={}".format(temp,hum,lux,batt))
    f.close() 

def scanSensors(thunderboards):

    for devId, tb in thunderboards.items():

        try:
            value = tb.sensor['power_source_type'].read()   # TODO why do we need to know this? are some sensors only enabled when powered via USB?
        except:
            print "scanSensor disconnected"
            return

        if ord(value) == 0x04:
            tb.coinCell = True

        tb.filename="TB"
        tb.filename+=tb.dev.addr.replace(":","_")
        tb.filename+=".csv"
        print "filename={}".format(tb.filename)
        if not os.path.isfile(tb.filename):
            tb.csvfile=open(tb.filename, 'w+',1) 
            tb.csvfile.write("Date Time,Temperature C, Humidity, Lux, Battery, Comment\n")
        else:
            tb.csvfile=open(tb.filename, 'a+',1) 

     
        text = ''
        text += '\n' + tb.name + '\n'
        data = dict()                   # the sensor data is stored in this dictionary

        try:

            #for key in tb.sensor.keys():
            for key in ('firmware', 'temperature','humidity','ambientLight','battery'): # TODO change this to a list of sensors passed in from the command line
                if key == 'temperature':
                        data['temperature'] = tb.readTemperature()
                        text += 'Temperature:\t{} C\n'.format(data['temperature'])

                elif key == 'humidity':
                    data['humidity'] = tb.readHumidity()
                    text += 'Humidity:\t{} %RH\n'.format(data['humidity'])

                elif key == 'ambientLight':
                    data['ambientLight'] = tb.readAmbientLight()
                    text += 'Ambient Light:\t{} Lux\n'.format(data['ambientLight'])

                elif key == 'uvIndex':
                    data['uvIndex'] = tb.readUvIndex()
                    text += 'UV Index:\t{}\n'.format(data['uvIndex'])

                elif key == 'co2' and tb.coinCell == False:
                    data['co2'] = tb.readCo2()
                    text += 'eCO2:\t\t{}\n'.format(data['co2'])

                elif key == 'voc' and tb.coinCell == False:
                    data['voc'] = tb.readVoc()
                    text += 'tVOC:\t\t{}\n'.format(data['voc'])

                elif key == 'sound':
                    print "before sound"
                    try:
                        data['sound'] = tb.readSound()
                    except:
                        print "failed readsound"
                    print "after sound"
                    text += 'Sound Level:\t{}\n'.format(data['sound'])

                elif key == 'pressure':
                    data['pressure'] = tb.readPressure()
                    text += 'Pressure:\t{}\n'.format(data['pressure'])

                elif key == 'battery':
                    data['battery'] = tb.readBattery()
                    text += 'Battery:\t{}\n'.format(data['battery'])

                elif key == 'firmware':
                    data['firmware'] = tb.readFirmware()
                    text += 'Firmware:\t{}\n'.format(data['firmware'])

        except:
            print "Failed to get sensor data"
            return
        
        print(text)
        tb.csvfile.write("{}, {},{},{},{}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data['temperature'],data['humidity'],data['ambientLight'],data['battery']))

        thunderboards[devId].ble_service.disconnect() # disconnect from the TB2 so it will go back to sleep and save battery power
        # if we have a Thingspeak channel setup, send the data to the respective channel
        if tb.filename in ThingSpeakKeys:
            Post2Thingspeak(ThingSpeakKeys[tb.filename], data['temperature'],data['humidity'],data['ambientLight'],data['battery'])
        else:
            print "failed to find Thingspeak key {}".format(tb.filename)
    return

def usage():
    print "Usage: sudo python tbsense_scan.py [thlpg]"
    print " Optional command line arguments select which sensors to read"
    print " NOTE ----- THE OPTIONAL COMMAND LINE ARGUMENTS have not been coded yet..."
    print " t=temperature in C"
    print " h=relative humidity in %"
    print " l=light level in Lux"
    print " p=barometric pressure in ?"
    print " g=gas sensor in ?"
    print "Version 0.9.1 28 Jan 2019"
    print "Requires being run as root to access the BLE chip"
    print "Scans for Silicon Labs Thunderboard Sense 2 BLE sensor boards (TB2)"
    print "When a TB2 board wakes up and begins advertising, this program will connect to it,"
    print "then read out the desired sensor readings and store the values in a .csv file"


if __name__ == '__main__':
    ''' Program execution begins here '''

    while True:                                 # this program runs forever (hopefully)
        thunderboards = getThunderboards()      # scan BLE looking for a TB2 
        if len(thunderboards) == 0:
            if DEBUG>6: print "\b.",            # print out .s which makes it easy to visialize the time between samples
        else:
            #print("{} Thunderboards found - begin scanning".format(len(thunderboards)))
            scanSensors(thunderboards)          # scan the sensors

            time.sleep(1)          # wait for this TB board to sleep before looking for the others

