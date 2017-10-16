#!/usr/bin/python3.4

import pexpect
import csv
import sys
import shutil
import time
import datetime
import subprocess


def floatfromhex(h):
    t = float.fromhex(h)
    if t > float.fromhex('7FFF'):
        t = -(float.fromhex('FFFF') - t + 1)
        pass
    return t


def scan_advertisement_data():
    tool = pexpect.spawn('sudo hcidump -R')
    scan = pexpect.spawn('sudo hcitool lescan')
    start_time = time.time()
    time.sleep(5)
    scan.kill(2)
    tool.kill(2)
    tool.expect (['%',pexpect.EOF])                                     
    adv_data = tool.before
    print("adv data: %s		", adv_data)
    return adv_data


def parse_nodes(advdata_gathered):
    count = 0
    nodes = []
    while (count < len(advdata_gathered)):
        # Parse advertisement data  
        if ( advdata_gathered[count] is '>'):
          try:
            if ( advdata_gathered[count + 47] is 'F' and advdata_gathered[count + 48] is 'F' ):
                if ( advdata_gathered[count + 50] is 'C' and advdata_gathered[count + 51] is 'C' \
                and advdata_gathered[count + 53] is 'C' and advdata_gathered[count + 54] is 'C'): 
                       #                      CC CC 64 08 \r\n  F9 00 33 00 00 00 DA CB
                    try:
                        nodes.append(advdata_gathered[count + 38] + advdata_gathered[count + 39] \
                        + '' + advdata_gathered[count + 35] + advdata_gathered[count + 36] \
                        + '' + advdata_gathered[count + 32] + advdata_gathered[count + 33] \
                        + '' + advdata_gathered[count + 29] + advdata_gathered[count + 30] \
                        + '' + advdata_gathered[count + 26] + advdata_gathered[count + 27] \
                        + '' + advdata_gathered[count + 23] + advdata_gathered[count + 24] \
                        + ';' + advdata_gathered[count + 56] + advdata_gathered[count + 57] \
                        + ';' + advdata_gathered[count + 59] + advdata_gathered[count + 60] \
                        + '' + advdata_gathered[count + 66] + advdata_gathered[count + 67] \
                        + ';' + advdata_gathered[count + 69] + advdata_gathered[count + 70] \
                        + '' + advdata_gathered[count + 72] + advdata_gathered[count + 73] \
                        + ';' + advdata_gathered[count + 75] + advdata_gathered[count + 76] \
                        + '' + advdata_gathered[count + 78] + advdata_gathered[count + 79] \
                        + ';' + advdata_gathered[count + 81] + advdata_gathered[count + 82] \
                        + '' + advdata_gathered[count + 84] + advdata_gathered[count + 85] \
                        + ';' + advdata_gathered[count + 87] + advdata_gathered[count + 88] )
                        print ('nodes: %s', nodes)
                        addrs = advdata_gathered[count + 38] + advdata_gathered[count + 39] + advdata_gathered[count + 35] + advdata_gathered[count + 36] \
                        + advdata_gathered[count + 32] + advdata_gathered[count + 33] + advdata_gathered[count + 29] + advdata_gathered[count + 30] \
                        + advdata_gathered[count + 26] + advdata_gathered[count + 27] + advdata_gathered[count + 23] + advdata_gathered[count + 24]
                        batteryLevel = int(floatfromhex(advdata_gathered[count + 56] + advdata_gathered[count + 57]))
                        temperature = int(floatfromhex(advdata_gathered[count + 59] + advdata_gathered[count + 60] + advdata_gathered[count + 66] + advdata_gathered[count + 67]))
                        humidity = int(floatfromhex(advdata_gathered[count + 69] + advdata_gathered[count + 70] + advdata_gathered[count + 72] + advdata_gathered[count + 73]))
                        pressure = int(floatfromhex(advdata_gathered[count + 75] + advdata_gathered[count + 76] + advdata_gathered[count + 78] + advdata_gathered[count + 79]))
                        volts = int(floatfromhex(advdata_gathered[count + 81] + advdata_gathered[count + 82] + advdata_gathered[count + 84] + advdata_gathered[count + 85]))
                        now = datetime.datetime.now()
                        with open('/home/pi/demo/sensors.csv', 'a') as csvfile:
                            fieldnames = ['Time', 'Sensor MAC', 'Battery %', 'Temperature C', 'Humidity %', 'Pressure', 'Volts']
                            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                            writer.writerow({'Time': now.strftime("%Y-%m-%d %H:%M:%S"), 'Sensor MAC': addrs, 'Battery %': batteryLevel, 'Temperature C': temperature, 'Humidity %': humidity, 'Pressure': pressure, 'Volts': volts})
                    except IndexError:
                        pass
          except IndexError:
                print ('Index of out of array and not valid, lets continue')
                pass
        count = count + 1
    nodes_found = list(nodes)
    print ('Data %s', nodes_found)
    if nodes_found:
        pass
        print (nodes_found)
    return nodes_found


print ('******************** PehuTec-Valmet POC Demo ********************')

with open('/home/pi/demo/sensors.csv', 'a') as csvfile:
    fieldnames = ['Time', 'Sensor MAC', 'Battery %', 'Temperature C', 'Humidity %', 'Pressure', 'Volts']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
       
while True:
    print ('-----scanning nodes----')

    return_code = subprocess.call(["sudo", "hciconfig", "hci0" ,"reset"])
    if return_code != 0:
       print ('Check that your BLE device is enabled')
       sys.exit(0)

    advdata_gathered = scan_advertisement_data()
    nodes = parse_nodes(advdata_gathered)

    if len(nodes) == 0:
        pass
        #print ('No nodes')


