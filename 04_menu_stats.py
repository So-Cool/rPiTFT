#!/usr/bin/env python
from sys import argv as __argv__
from menu_settings import *

################################################################################
def _1():
    pass
def _2():
    pass
def _3():
    pass
def _4():
    pass
def _5():
    # next page
    go_to_page(PAGE_03)
def _6():
    # Refresh
    pygame.quit()
    os.execv(__file__, sys.argv)
################################################################################

temp, clock, volts = get_temp(), get_clock(), get_volts()
names = [temp, clock, "", volts, "", "<<<", "Refresh"]

screen = init()
populate_screen(names, screen, label2=True, label3=True, b12=False, b34=False)
main([_1, _2, _3, _4, _5, _6])
