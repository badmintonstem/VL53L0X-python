#!/usr/bin/python

# MIT License
# 
# Copyright (c) 2017 John Bryan Moore
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import time
import VL53L0X
import RPi.GPIO as GPIO

# GPIO for Sensor 1 shutdown pin
sensor1_shutdown = 20
# GPIO for Sensor 2 shutdown pin
sensor2_shutdown = 16
#! sensor3_shutdown = ??

GPIO.setwarnings(False)

# Setup GPIO for shutdown pins on each VL53L0X
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor1_shutdown, GPIO.OUT)
GPIO.setup(sensor2_shutdown, GPIO.OUT)
#!GPIO.setup(sensor3_shutdown, GPIO.OUT)

# Set all shutdown pins low to turn off each VL53L0X
GPIO.output(sensor1_shutdown, GPIO.LOW)
GPIO.output(sensor2_shutdown, GPIO.LOW)
#!GPIO.output(sensor3_shutdown, GPIO.LOW)

# Keep all low for 500 ms or so to make sure they reset
time.sleep(0.50)

# Create one object per VL53L0X passing the address to give to
# each.
tof = VL53L0X.VL53L0X(i2c_address=0x2B)
tof1 = VL53L0X.VL53L0X(i2c_address=0x2D)
#!tof2 = VL53L0X.VL53L0X(i2c_address=???)
tof.open()
tof1.open()
#!tof2.open()

# Set shutdown pin high for the first VL53L0X then 
# call to start ranging 
GPIO.output(sensor1_shutdown, GPIO.HIGH)
time.sleep(0.50)
tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

# Set shutdown pin high for the second VL53L0X then 
# call to start ranging 
GPIO.output(sensor2_shutdown, GPIO.HIGH)
time.sleep(0.50)
tof1.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

GPIO.output(sensor3_shutdown, GPIO.HIGH)
time.sleep(0.50)
tof2.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

timing = tof.get_timing()
if timing < 20000:
    timing = 20000
print("Timing %d ms" % (timing/1000))

for count in range(1,101):
    distance = tof.get_distance()
    if distance > 0:
        print("sensor %d - %d mm, %d cm, iteration %d" % (1, distance, (distance/10), count))
        sensor1distance = distance
    else:
        print("%d - Error" % 1)

    distance = tof1.get_distance()
    if distance > 0:
        print("sensor %d - %d mm, %d cm, iteration %d" % (2, distance, (distance/10), count))
        sensor2distance = distance
    else:
        print("%d - Error" % 2)

    distance = tof2.get_distance()
    if distance > 0:
        print("sensor %d - %d mm, %d cm, iteration %d" % (3, distance, (distance/10), count))
        sensor3distance = distance
    else:
        print("%d - Error" % 2)


    #if front sensor < amount(say 1cm):
    #Take readings from both sensors left and right (or just turn predetermined direction)
    # if leftd > rightd (or other way), turn the way with the longest distance to go
    #After button pressed or so many turns (5) stop

    time.sleep(timing/1000000.00)

tof1.stop_ranging()
GPIO.output(sensor2_shutdown, GPIO.LOW)
tof.stop_ranging()
GPIO.output(sensor1_shutdown, GPIO.LOW)
tof2.stop_ranging()
GPIO.output(sensor1_shutdown, GPIO.LOW)

tof.close()
tof1.close()
tof2.close()
