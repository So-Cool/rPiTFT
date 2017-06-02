#!/usr/bin/env python
from sys import argv as __argv__
from menu_settings import *

################################################################################
def _1():
    # X HDMI
    x("fb0", __file__, __argv__)
def _2():
    # X TFT
    x("fb1", __file__, __argv__)
def _3():
    run_proc("/usr/bin/sudo -u pi /usr/bin/kodi", __file__, __argv__)
def _4():
    run_proc("/usr/bin/sudo -u pi /usr/bin/emulationstation", __file__, __argv__)
def _5():
    # next page
    go_to_page(SCREEN_OFF)
def _6():
    # next page
    go_to_page(PAGE_02)
################################################################################

hostname = get_hostname()
names = [hostname, "X on HDMI", "X on TFT", "Kodi", "RetroPi", "Screen Off", ">>>"]

screen = init()
populate_screen(names, screen)
main([_1, _2, _3, _4, _5, _6])
