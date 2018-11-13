# HBMSGreenHouse
Hollis-Brookline Middle School Greenhouse temperature/humidity monitor

The HBMS greenhouse project captures temperature, humidity and other sensor data in the greenhouse behind HBMS.

The 2018 goal is to capture data during the winter to determine what heating and structure components will enable the use of the greenhouse during most of the school year. It is understood that the greenhouse will probably not support a growing environment in January but if a portion of the greenhouse can remain above freezing this would allow the aquaponics to remain in place.

The ultimate goal is to enable year-round use of the greenhouse for educational purposes. Extend the growing season as much as practical in NH utilizing passive solar thermal capture and possibly solar PV for additional heating.

http://sites.sau41.org/hbms-health-education/home/hbms-greenhouse

The GitHub repository is located at: https://github.com/drzwave/HBMSGreenHouse

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

# Basic GIT commands
- git clone HTTPS://github.com/drzwave/HBMSGreenHouse.git = downloads the repository to the local RPi
- cd HBMSGreenHouse = you have to be in the repository directory to run the other git commands
- git status = prints a list of files that have changed on this RPi
- git commit -am "message" = checks your changes in TO THIS RPI! not the repository!
- git push   = Checks the changes in your repository into the GitHub master respository
- git pull   = logs into the GutHub master and downloads any changes - ALWAYS DO THIS BEFORE committing
- git add <filename> = adds the file to the repository. Don't forget to PUSH it!
    - Note that directories are not checked in but the structure will be built automatically.
    - cd to a directory and just git add a file to create the directory.
- see the many git tutorials for more details

# Contacts
- Eric Ryherd - Hollis Energy Committee coded the initial development of this project - e_ryherd@yahoo.com
- Erin White - Teacher - erin.white@sau41.org
