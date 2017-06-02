#!/usr/bin/env python
from sys import argv as __argv__
from menu_settings import *

################################################################################
def _1():
    # Apache
    # Transmission
    c = toggle_service(services[0])
    make_button(names[1], button_pos_1, c, screen)
def _2():
    # Pure-ftpd
    # c = toggle_service(services[1])
    # make_button(names[2], button_pos_2, c, screen)
    pass
def _3():
    # VNC Server
    # c = toggle_service(services[2])
    # make_button(names[3],  button_pos_3, c, screen)
    pass
def _4():
    # msfconsole
    # run_proc("/usr/bin/msfconsole", __file__, __argv__)
    pass
def _5():
    # Previous page
    go_to_page(PAGE_02)
def _6():
    # Next page
    go_to_page(PAGE_04)
################################################################################

date = get_date()
# names = [date, "WWW Server", "FTP Server", "VNC-Server", "Metasploit", "<<<", ">>>"]
# services = ["apache2", "pure-ftpd", "vnc", "", "", ""]
names = [date, "Transmission", "", "", "", "<<<", ">>>"]
services = ["transmission-daemon", "", "", "", "", ""]

screen = init()
populate_screen(names, screen, service=services, b34=False)
main([_1, _2, _3, _4, _5, _6])
