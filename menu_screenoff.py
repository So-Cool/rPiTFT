#!/usr/bin/env python
import RPi.GPIO as GPIO
from menu_settings import *

init(draw=False)
# Initialise GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

#While loop to manage touch screen inputs
screen_off()
main()
