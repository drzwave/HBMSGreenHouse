''' Thunderboard.py - Silicon Labs Thunderboard Sense 2 methods
'''
from bluepy.btle import *
import struct
import time

class Thunderboard:
    ''' Connects to a SiLabs Thunderboard and reads out all the characteristics and builds the self.sensor dictionary
        Methods are provided for reading the value of each sensor.
        TODO add more here about the units for each sensor.
    '''

    def __init__(self, dev):
        ''' Initialize the BLE device dev which is already known to be a thundersense board
        '''
        self.dev  = dev
        self.sensor = dict()
        self.name = ''
        self.session = ''
        self.coinCell = False

        # Get device name and characteristics

        scanData = dev.getScanData()

        for (adtype, desc, value) in scanData:
            if (desc == 'Complete Local Name'):
                self.name = value

        print "Connect to {}".format(self.name)
        self.ble_service = Peripheral()
        try:
            self.ble_service.connect(dev.addr, dev.addrType)             # TODO why is this failing to connect??? - #1
        except:
            print "failed to connect - wait a sec and try again"
            time.sleep(2)
            try:
                self.ble_service.connect(dev.addr, dev.addrType)             # TODO why is this failing to connect??? - #2
                print "connected on 2nd try"
            except:
                print "failed to connect the 2nd time too"
                return

        try:
            characteristics = self.ble_service.getCharacteristics()
        except:
            return

        for k in characteristics:
            #print "Chars={} UUID={}".format(k,k.uuid)
            if k.uuid == '2a6e':
                self.sensor['temperature'] = k
            
            elif k.uuid == '2a6f':
                self.sensor['humidity'] = k
            
            elif k.uuid == '2a76':
                self.sensor['uvIndex'] = k
            
            elif k.uuid == '2a6d':
                self.sensor['pressure'] = k
            
            elif k.uuid == '2a19':
                self.sensor['battery'] = k
            
            elif k.uuid == '2a26':
                self.sensor['firmware'] = k
            
            elif k.uuid == 'c8546913-bfd9-45eb-8dde-9f8754f4a32e':
                self.sensor['ambientLight'] = k

            elif k.uuid == 'c8546913-bf02-45eb-8dde-9f8754f4a32e':
                self.sensor['sound'] = k

            elif k.uuid == 'efd658ae-c401-ef33-76e7-91b00019103b':
                self.sensor['co2'] = k

            elif k.uuid == 'efd658ae-c402-ef33-76e7-91b00019103b':
                self.sensor['voc'] = k

            elif k.uuid == 'ec61a454-ed01-a5e8-b8f9-de9ec026ec51':
                self.sensor['power_source_type'] = k

   
    def readTemperature(self):
        value = self.sensor['temperature'].read()
        value = struct.unpack('<h', value)          # signed
        value = value[0] / 100.0
        timeout=0
        while value<-50 and timeout<5:              # sensor not ready - try again
            time.sleep(.3) 
            value = self.sensor['temperature'].read()
            value = struct.unpack('<h', value) 
            value = value[0] / 100.0
            timeout+=1
        return value

    def readHumidity(self):
        value = self.sensor['humidity'].read()
        value = struct.unpack('<H', value)
        value = value[0] / 100
        timeout=0
        while value>100 and timeout<5:              # sensor not ready - try again
            value = self.sensor['humidity'].read()
            value = struct.unpack('<H', value)
            value = value[0] / 100
            timeout+=1
        return value

    def readAmbientLight(self):
        value = self.sensor['ambientLight'].read()
        value = struct.unpack('<L', value)
        value = value[0] / 100
        timeout=0
        while value>100000 and timeout<5:    # then the value is invalid which means the sensor has not fully powered up
            time.sleep(.2)  # wait a bit and try again
            value = self.sensor['ambientLight'].read()
            value = struct.unpack('<L', value)
            print value
            value = value[0] / 100
            timeout+=1
        return value

    def readUvIndex(self):
        value = self.sensor['uvIndex'].read()
        value = ord(value)
        return value

    def readCo2(self):
        value = self.sensor['co2'].read()
        value = struct.unpack('<h', value)
        value = value[0]
        return value

    def readVoc(self):
        value = self.sensor['voc'].read()
        value = struct.unpack('<h', value)
        value = value[0]
        return value
    
    def readSound(self):
        value = self.sensor['sound'].read()
        value = struct.unpack('<h', value)
        value = value[0] / 100
        return value

    def readPressure(self):
        value = self.sensor['pressure'].read()
        value = struct.unpack('<L', value)
        value = value[0] / 1000
        return value

    def readBattery(self):
        value = self.sensor['battery'].read()
        value = struct.unpack('<B', value)
        value = value[0]
        return value

    def readFirmware(self):
        value = self.sensor['firmware'].read()
        print value
        return value
