''' Hollis Brookline Middle School Greenhouse sensor data project.
    This project uses a Raspberry Pi to collect data from a number of 
    TI SensorTags for temperature, humidity and light level (lux).

    The SensorTags are configured to send data every few minutes.
    This program collects that data and stores it in a .CSV file.

    This code is tested using the Sensor Tag versions available in late 2018 - FW Version 1.42
    If other SensorTag versions are used the code may need to be modified.
    The bluepy sensortag.py has good examples of how to communicate with the SensorTags.

    Author: Eric Ryherd
    Date: 9 Dec 2018
'''

#from bluepy import btle # is pre-installed on the RPi. Bluepy handles all the bluetooth communication.
from bluepy.btle import UUID, DefaultDelegate, Scanner, Peripheral, AssignedNumbers # Bluetooth communication handler
import sys, struct, math, time, os, datetime    # system utilities

def _TI_UUID(val):
    return UUID("%08X-0451-4000-b000-000000000000" % (0xF0000000+val))

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
        
    def handleDiscovery(self,dev,isNewDev,isNewData):
        if isNewDev:
            print "discovered device {}".format(dev.addr)
            
        elif isNewData:
            print "Received new data from {}".format(dev.addr)

    def handleNotification(self,hnd,data):
        print "scandelegate notification"

class SensorBase:
    # Derived classes should set: svcUUID, ctrlUUID, dataUUID
    sensorOn  = struct.pack("B", 0x01)
    sensorOff = struct.pack("B", 0x00)

    def __init__(self, periph):
        self.periph = periph
        self.service = None
        self.ctrl = None
        self.data = None

    def enable(self):
        if self.service is None:
            self.service = self.periph.getServiceByUUID(self.svcUUID)
        if self.ctrl is None:
            self.ctrl = self.service.getCharacteristics(self.ctrlUUID) [0]
        if self.data is None:
            self.data = self.service.getCharacteristics(self.dataUUID) [0]
        if self.sensorOn is not None:
            self.ctrl.write(self.sensorOn,withResponse=True)

    def read(self):
        return self.data.read()

    def disable(self):
        if self.ctrl is not None:
            self.ctrl.write(self.sensorOff)


class SensorTag(Peripheral):
    def __init__(self,addr):
        Peripheral.__init__(self,addr)

        fwVers = self.getCharacteristics(uuid=AssignedNumbers.firmwareRevisionString)
        if len(fwVers) >= 1:
            self.firmwareVersion = fwVers[0].read().decode("utf-8")
        else:
            self.firmwareVersion = u''
        print "firmware version={}".format(self.firmwareVersion)

#        self._mpu9250       = MovementSensorMPU9250(self)
#        self.IRtemperature  = IRTemperatureSensorTMP007(self)
#        self.accelerometer  = AccelerometerSensorMPU9250(self._mpu9250)
        self.humidity       = HumiditySensorHDC1000(self)   # The humidity sensor includes a temperature sensor
#        self.magnetometer   = MagnetometerSensorMPU9250(self._mpu9250)
#        self.barometer      = BarometerSensorBMP280(self)
#        self.gyroscope      = GyroscopeSensorMPU9250(self._mpu9250)
        self.keypress       = KeypressSensor(self)
        self.lightmeter     = OpticalSensorOPT3001(self)
        self.battery        = BatterySensor(self)

class HumiditySensorHDC1000(SensorBase):
    svcUUID  = _TI_UUID(0xAA20)
    dataUUID = _TI_UUID(0xAA21)
    ctrlUUID = _TI_UUID(0xAA22)

    def __init__(self, periph):
        SensorBase.__init__(self, periph)

    def read(self):
        '''Returns (ambient_temp, rel_humidity)'''
        (rawT, rawH) = struct.unpack('<HH', self.data.read())
        temp = -40.0 + 165.0 * (rawT / 65536.0)
        RH = 100.0 * (rawH/65536.0)
        return (round(temp,1), round(RH,1))

class OpticalSensorOPT3001(SensorBase):
    svcUUID  = _TI_UUID(0xAA70)
    dataUUID = _TI_UUID(0xAA71)
    ctrlUUID = _TI_UUID(0xAA72)

    def __init__(self, periph):
       SensorBase.__init__(self, periph)

    def read(self):
        '''Returns value in lux'''
        raw = struct.unpack('<h', self.data.read()) [0]
        m = raw & 0xFFF;
        e = (raw & 0xF000) >> 12;
        return round(0.01 * (m << e),1)

class BatterySensor(SensorBase):
    svcUUID  = UUID("0000180f-0000-1000-8000-00805f9b34fb")
    dataUUID = UUID("00002a19-0000-1000-8000-00805f9b34fb")
    ctrlUUID = None
    sensorOn = None

    def __init__(self, periph):
       SensorBase.__init__(self, periph)

    def read(self):
        '''Returns the battery level in percent'''
        val = ord(self.data.read())
        return val

class KeypressSensor(SensorBase):
    svcUUID = UUID(0xFFE0)
    dataUUID = UUID(0xFFE1)
    ctrlUUID = None
    sensorOn = None

    def __init__(self, periph):
        SensorBase.__init__(self, periph)
 
    def enable(self):
        SensorBase.enable(self)
        self.char_descr = self.service.getDescriptors(forUUID=0x2902)[0]
        self.char_descr.write(struct.pack('<bb', 0x01, 0x00), True)

    def disable(self):
        self.char_descr.write(struct.pack('<bb', 0x00, 0x00), True)

class sensorDelegate(DefaultDelegate):
    ''' More to come'''
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleNotification(self, hnd, data):
        print "Hum={}".format(tag.humidity.read())
        print "Notification"
        print hnd
        print ord(data[0])
        sys.stdout.flush()

class utility():
    def usage(self):
        print "\ncd HBMSGreenHouse/web/data - always run the program from this directory"
        print "USAGE: sudo python tempHumLux.py"
        print "Note this program REQUIRES being run as root (IE: sudo)"
        print "BLE devices will be scanned and SensorTags identified"
        print "SensorTag data will then be appended to the respective .csv file\n"

''' If you are new to Python, this section of code is run when the file is executed from the commandline.'''
if __name__ == "__main__":
    # Scan for BLE devices
    ble=Scanner().withDelegate(ScanDelegate())
    try:
        devs=ble.scan()
    except:
        u=utility()
        u.usage()  # if executed without being root (sudo) this is exectued.
        sys.exit(1)
    tags=[]
    # look thru the list for SensorTags
    for dev in devs:
        print "Device {} {} RSSI={}".format(dev.addr, dev.addrType, dev.rssi)
        for (adtype,desc,value) in dev.getScanData():
            #print " {}={}".format(desc,value)
            if "CC2650" in value:
                print "found tag {}".format(dev.addr)
                tags.append(SensorTag(dev.addr))
    print "Found {} SensorTags.".format(len(tags))
    if len(tags)<1:
        print "No SensorTags found. Exiting"
        sys.exit(3)

    # for the SensorTag devices, enable the desired sensors
    for tag in tags:
        tag.humidity.enable()
        tag.lightmeter.enable()
        #tag.keypress.enable()
        tag.battery.enable()
        tag.withDelegate(sensorDelegate())
        tag.filename="ST"
        tag.filename +=tag.addr
        tag.filename=tag.filename.replace(":","_")
        tag.filename+=".csv"
        print "filename={}".format(tag.filename)
        if not os.path.isfile(tag.filename):
            tag.csvfile=open(tag.filename, 'w+',1) 
            tag.csvfile.write("Date Time,Temperature C, Humidity, Lux, Battery, Comment\n")
        else:
            tag.csvfile=open(tag.filename, 'a+',1) 

    # capture the data from the sensors forever or as long as they remain connected to the RPi3
    while len(tags)>0:
        time.sleep(60*15)      # wait until the next reading (TODO could compute the time to the next fractional hour boundary to always be say 1/4 past the hour)
        for tag in tags:
            try:
                temphum=tag.humidity.read()
                temp=temphum[0]
                hum=temphum[1]
                lux=tag.lightmeter.read()
                bat=tag.battery.read()
                print "Temp={}, Hum={}, Lux={}".format(temp,hum,lux)
                tag.csvfile.write("{}, {},{},{},{}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), temp,hum,lux,bat))
            except: # if the device disconnects, close the file.
                tag.csvfile.close()
                print "tag {} has disconnected".format(tag.addr)
                tags.remove(tag)

    for tag in tags:
        tag.csvfile.close()
    print "Exit"
