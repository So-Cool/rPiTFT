#!/usr/bin/env python
from sys import argv as __argv__
from menu_settings import *

################################################################################
def _1():
    run_cmd("con2fbmap 1 0")
    exit_menu()
    # run_proc("con2fbmap 1 0", __file__, __argv__)
    # # Kismet
    # run_proc("/usr/bin/sudo -u pi /usr/bin/kismet", __file__, __argv__)
def _2():
    run_cmd("con2fbmap 1 1")
    exit_menu()
    # SDR-Scanner
    # pygame.quit()
    # run_cmd("/bin/bash " + MENUDIR + "sdr-scanner.sh")
    # os.execv(__file__, __argv__)
    # htop
    # run_proc("/usr/bin/htop", __file__, __argv__)
    # run_proc("/usr/bin/sudo setsid sh -c 'exec /usr/bin/htop <> /dev/tty1 >&0 2>&1'", __file__, __argv__)
def _3():
    # shutdown
     pygame.quit()
     run_cmd("/usr/bin/sudo /sbin/shutdown -h now")
     sys.exit()
def _4():
    global screen
    global black
    # reboot
    screen.fill(black)
    font=pygame.font.Font(None,72)
    label=font.render("Rebooting. .", 1, (white))
    screen.blit(label,(40,120))
    pygame.display.flip()
    pygame.quit()
    run_cmd("/usr/bin/sudo /sbin/shutdown -r now")
    sys.exit()
def _5():
    # Previous page
    go_to_page(PAGE_01)
def _6():
    # Next page
    go_to_page(PAGE_03)
################################################################################

ip = get_ip()
names = [ip, "HDMI console", "TFT console", "Shutdown", "Reboot", "<<<", ">>>"]

screen = init()
populate_screen(names, screen)
main([_1, _2, _3, _4, _5, _6])
