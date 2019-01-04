''' Hollis Brookline Middle School Greenhouse sensor data project.

    genweb.py is a small program that generates a web page 
    with the sensor data and plots the data in several graphs.
    It is expected to simply execute this program every 15 minutes
    via a cron job.

    This program MUST be run from the HBMSGreenHouse/web/data directory

    usage:
      cd /home/pi/HBMSGreenHouse/web/data; python ../../software/genweb.py

    Author: Eric Ryherd
    Date: 2 Jan 2019
'''

import os





''' If you are new to Python, this section of code is run when the file is executed from the commandline.'''
if __name__ == "__main__":
    file_list = os.listdir(".")     # list all the files in the directory
    csv_list=[]
    for i in file_list:             # prune the list to just the .csv files
        if "csv" in i:
            csv_list.append(i)
    for i in csv_list:
        os.system('tail -n 96 {} > genplot.dat'.format(i))          # plot just the last 24 hours
        os.system('gnuplot ../../software/gengraph.plt > ../pix/{}.png'.format(i[:-4]))
        os.system('cat {} > genplot.dat'.format(i))                 # plot all the data which is a pretty busy graph
        os.system('gnuplot ../../software/gengraph.plt > ../pix/{}All.png'.format(i[:-4]))
    os.system('rm -f genplot.dat')
    senhtml=open("../sensors.html",'w',1)
    senhtml.write("<!DOCTYPE html><html><head><title>HBMS Greenhouse Sensor Data</title></head>\n")
    senhtml.write("<body>\n")
    senhtml.write("<h1>HBMS Greenhouse Sensor Data</h1>\n")
    senhtml.write('<h3><a href="index.html">Back</a> to the index</h3>\n')
    senhtml.write("<h2>There are {} sensors collecting data</h2>\n".format(len(csv_list)))
    for i in csv_list:
        senhtml.write('<h1>Sensor <a href="./data/{0}">{0}</a> last 24 hours</h2>\n'.format(i))
        senhtml.write('<img src=./pix/{}.png>\n'.format(i[:-4]))
        senhtml.write('<h1>Sensor {0} all data</h2>\n'.format(i))
        senhtml.write('<img src=./pix/{}All.png>\n'.format(i[:-4]))
    senhtml.write("</body></html>\n")
    senhtml.close()
