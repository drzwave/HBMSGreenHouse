# HBMSGreenHouse
Hollis-Brookline Middle School Greenhouse temperature/humidity monitor

The HBMS greenhouse project captures temperature, humidity and other sensor data in the greenhouse behind HBMS.

The 2018 goal is to capture data during the winter to determine what heating and structure components will enable the use of the greenhouse during most of the school year. It is understood that the greenhouse will probably not support a growing environment in January but if a portion of the greenhouse can remain above freezing this would allow the aquaponics to remain in place.

The ultimate goal is to enable year-round use of the greenhouse for educational purposes. Extend the growing season as much as practical in NH utilizing passive solar thermal capture and possibly solar PV for additional heating.

http://sites.sau41.org/hbms-health-education/home/hbms-greenhouse

# Equipment
- Raspberry Pi (RPi) model 3 or 3B+
    - Bluetooth is required so use at least a model 3B (3B+ has not been tried yet)
    - Model 3 also has Wifi to connect to the school Wifi
- RPi Power Supply (5V 2.5A minimum) 
- RPi enclosure
- microSD card 8GB or larger
- Texas Instruments SensorTags
    - TI SensorTags are wireless (BLE) $30 Temp/Humidity/light level sensors 
    - CR2032 batteries
- 110VAC power for the RPi

# Setup
- See the SETUP.TXT document in the DOC directory for details on how to setup and configure the RPi

# Directory Structure
- DOC - documentation on the project
- SOFTWARE - software for the RPi to capture the sensor data and serve a web page
- HARDWARE - Details on the hardware, mostly on the TI SensorTags

# Contacts
- Eric Ryherd - Hollis Energy Committee coded the initial development of this project - e_ryherd@yahoo.com
- Erin White - Teacher - erin.white@sau41.org
