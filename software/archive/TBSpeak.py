''' HBMS Greenhouse temperature sensor project
Author  Eric Ryherd - e_ryherd@yahoo.com
Date    6 Jan 2019

Initially copied from the Silicon Labs web site: https://www.silabs.com/community/projects.entry.html/2017/08/20/project_completedan-3RvH

This python code connects to a Silicon Labs ThunderBoard BLE sensor
and then stores the data at ThingsSpeak.com as well as in a local CSV File
'''

#from __future__ import division
import sys
from bluepy.btle import *
import struct
import thread
from time import sleep
import urllib2

PRIVATE_KEY = 'O2RNOOMHOQAGEHP9'

# Base URL of Thingspeak
baseURL = 'https://api.thingspeak.com/update?api_key='


def vReadSENSE():
    scanner = Scanner(0)        # create the scanner object
    devices = scanner.scan(10)   # scan for devices for up to 10s
    for dev in devices:
        print "BLE Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi)

        for (adtype, desc, value) in dev.getScanData():
            print "  %s = %s" % (desc, value)
    num_ble = len(devices)
    print "{} BLE devices found".format(num_ble)
    if num_ble == 0:
        print "No BLE devices found, exiting"
        return None
    ble_service = []
    char_sensor = 0
    non_sensor = 0
    TVOC_char = Characteristic              # The BluePy doc specifically says this is NOT the way to do this...
    eCO2_char = Characteristic
    Pressure_char = Characteristic
    Sound_char = Characteristic
    temperature_char = Characteristic
    humidity_char = Characteristic

    #bat_char = Characteristic
    
    count = 15

    for i in range(num_ble):
        try:
            devices[i].getScanData()
            ble_service.append(Peripheral())
            #ble_service[char_sensor].connect('00:0b:57:36:63:ff',devices[i].addrType)
            ble_service[char_sensor].connect(devices[i].addr, devices[i].addrType)
            char_sensor = char_sensor + 1
            print "Connected %s device with addr %s " % (char_sensor, devices[i].addr)
        except:
            non_sensor = non_sensor + 1
    print char_sensor
    try:
        for i in range(char_sensor):

            services = ble_service[i].getServices()
            characteristics = ble_service[i].getCharacteristics()
            for k in characteristics:
                print k
                if k.uuid == "efd658ae-c401-ef33-76e7-91b00019103b":
                    print "eCO2 Level"
                    TVOC_char = k
                if k.uuid == "efd658ae-c402-ef33-76e7-91b00019103b":
                    print "TVOC Level"
                    TVOC_char = k
                if k.uuid == "00002a6d-0000-1000-8000-00805f9b34fb":
                    print "Pressure Level"
                    Pressure_char = k
                if k.uuid == "c8546913-bf02-45eb-8dde-9f8754f4a32e":
                    print "Sound Level"
                    Sound_char = k
                if k.uuid == "00002a6e-0000-1000-8000-00805f9b34fb":
                    print "Temperature"
                    temperature_char = k
                if k.uuid == "00002a6f-0000-1000-8000-00805f9b34fb":
                    print "Humidity"
                    humidity_char = k

                #if k.uuid == "2a19":
                    #print "Battery Level"
                    #bat_char = k

    except:
        return None
    while True:
        # units of ppb
        TVOC_data = TVOC_char.read()
        TVOC_data_value = ord(TVOC_data/100)

        #units of ppm
        eCO2_data = eCO2_char.read()
        eCO2_data_value = ord(eCO2_data[0])

        # pressure is in units of 0.1Pa
        Pressure_data = Pressure_char.read()
        Pressure_data_value = (Pressure_data * 10)

        # units of 0.01dB
        Sound_data = Sound_char.read()
        Sound_data_value = (Sound_data * 100)

        #bat_data = bat_char.read()
        #bat_data_value = ord(bat_data[0])

        #convert from farenheit
        temperature_data = temperature_char.read()
        temperature_data_value = (ord(temperature_data[1]) << 8) + ord(temperature_data[0])
        float_temperature_data_value = (temperature_data_value / 100)

        humidity_data = humidity_char.read()
	humidity_data_value =(ord(humidity_data[1])<<8)+ord(humidity_data[0])

	print "TVOC: ", TVOC_data_value
	print "eCO2: ", eCO2_data_value
	print "Pressure: ", Pressure_data_value
	print "Sound: ", Sound_data_value
	print "Temperature: ", float_temperature_data_value
	print "Humidity: ", humidity_data_value

	if count > 14:

        	f = urllib.urlopen(baseURL + PRIVATE_KEY + "&field1=%s&field2=%s&field3=%s&field4=%s&field5=%s&field6=%s" % (TVOC_data_value, eCO2_data_value, Pressure_data_value, Sound_data_value, float_temperature_data_value, humidity_data_value))
        	print f.read()
        	f.close()
        	count = 0
        	count = count + 1
        	sleep(1)

while True:
    vReadSENSE()
