from subprocess import Popen, PIPE, call
from pygame.locals import KEYDOWN, K_ESCAPE
import commands
import pygame
import time
import os
import socket
import sys

try:
    import RPi.GPIO as GPIO
except:
    print "No GPIO package"

# Hardware
SCREEN_DEVICE = "/dev/fb1"
TOUCH_DEVICE = "/dev/input/touchscreen"
MOUSE_DRIVER = "TSLIB"

PAGE_01 = "01_menu_run.py"
PAGE_02 = "02_menu_system.py"
PAGE_03 = "03_menu_services.py"
PAGE_04 = "04_menu_stats.py"
SCREEN_OFF = "menu_screenoff.py"

# bash export
FRAMEBUFFER = "/dev/fb1"
MENUDIR = "/home/pi/pitftmenu/"
startpage = PAGE_01

################################################################################

def exit_menu():
    # exit
    pygame.quit()
    sys.exit()

def x(fb, f, a, exit_menu=True):
    if exit_menu:
        pygame.quit()
    ## Requires "Anybody" in dpkg-reconfigure x11-common if we have scrolled pages previously
    run_x = "/usr/bin/sudo FRAMEBUFFER=/dev/%s startx" % fb
    run_cmd(run_x)
    os.execv(f, a)

def go_to_page(p):
    # next page
    pygame.quit()
    ##startx only works when we don't use subprocess here, don't know why
    page = MENUDIR + p
    os.execvp("python", ["python", page])
    sys.exit()

def get_hostname():
    hostname = run_cmd("hostname")
    hostname = "  " + hostname[:-1]
    return hostname

def get_ip():
    # Get Your External IP Address
    ip_msg = "Not connected"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.connect(('<broadcast>', 0))
        ip_msg=" IP: " + s.getsockname()[0]
    except Exception:
        pass
    return ip_msg

def get_date():
    # Get time and date
    d = time.strftime("%a, %d %b %Y  %H:%M:%S", time.localtime())
    return d

def get_temp():
    # Get CPU temperature
    temp = run_cmd("vcgencmd measure_temp")
    temp = "Temp: " + temp[5:-1]
    return temp

def get_clock():
    clock = run_cmd("vcgencmd measure_clock arm")
    clock = clock.split("=")
    clock = int(clock[1][:-1]) / 1024 /1024
    clock = "Clock: " + str(clock) + "MHz"
    return clock

def get_volts():
    volts = run_cmd("vcgencmd measure_volts")
    volts = 'Core:   ' + volts[5:-1]
    return volts

# Turn screen on
def screen_on():
    backlight = GPIO.PWM(18, 1023)
    backlight.start(100)
    GPIO.cleanup()
    go_to_page(PAGE_01)

# Turn screen off
def screen_off():
    backlight = GPIO.PWM(18, 0.1)
    backlight.start(0)

def check_service(srvc):
    if not srvc:
        return False

    if srvc == "vnc":
        if 'vnc :1' in commands.getoutput('/bin/ps -ef'):
            return True
        else:
            return False

    try:
        check = "/usr/sbin/service " + srvc + " status"
        status = run_cmd(check)
        if ("is running" in status) or ("active (running)") in status:
            return True
        else:
            return False
    except:
        return False

def s2c(srvc):
    # change service status to colour
    if check_service(srvc):
        return green
    else:
        return tron_light

def toggle_service(srvc):
    if srvc == "vnc":
        if check_service("vnc"):
            run_cmd("/usr/bin/sudo -u pi /usr/bin/vncserver -kill :1")
            return tron_light#True
        else:
            run_cmd("/usr/bin/sudo -u pi /usr/bin/vncserver :1")
            return green#False

    check = "/usr/bin/sudo /usr/sbin/service " + srvc + " status"
    start = "/usr/bin/sudo /usr/sbin/service " + srvc + " start"
    stop = "/usr/bin/sudo /usr/sbin/service " + srvc + " stop"
    status = run_cmd(check)
    if ("is running" in status) or ("active (running)") in status:
        run_cmd(stop)
        return tron_light#True
    else:
        run_cmd(start)
        return green#False
################################################################################

# Colours
# colors    R    G    B
white    = (255, 255, 255)
tron_whi = (189, 254, 255)
red      = (255,   0,   0)
green    = (  0, 255,   0)
blue     = (  0,   0, 255)
tron_blu = (  0, 219, 232)
black    = (  0,   0,   0)
cyan     = ( 50, 255, 255)
magenta  = (255,   0, 255)
yellow   = (255, 255,   0)
tron_yel = (255, 218,  10)
orange   = (255, 127,   0)
tron_ora = (255, 202,   0)

# Tron theme orange
tron_regular = tron_ora
tron_light   = tron_yel
tron_inverse = tron_whi

# Tron theme blue
##tron_regular = tron_blu
##tron_light   = tron_whi
##tron_inverse = tron_yel

################################################################################

label_pos_1 = (32, 30, 48)
label_pos_2 = (32, 105, 48)
label_pos_3 = (32, 180, 48)
button_pos_1 = (30, 105, 55, 210)
button_pos_2 = (260, 105, 55, 210)
button_pos_3 = (30, 180, 55, 210)
button_pos_4 = (260, 180, 55, 210)
button_pos_5 = (30, 255, 55, 210)
button_pos_6 = (260, 255, 55, 210)

size = width, height = 480, 320

################################################################################
# Functions
# define function for printing text in a specific place with a specific width
# and height with a specific colour and border
def make_button(text, (xpo, ypo, height, width), colour, screen):
    pygame.draw.rect(screen, tron_regular, (xpo-10,ypo-10,width,height),3)
    pygame.draw.rect(screen, tron_light, (xpo-9,ypo-9,width-1,height-1),1)
    pygame.draw.rect(screen, tron_regular, (xpo-8,ypo-8,width-2,height-2),1)
    font=pygame.font.Font(None,42)
    label=font.render(str(text).rjust(12), 1, (colour))
    screen.blit(label,(xpo,ypo))

# define function for printing text in a specific place with a specific colour
def make_label(text, (xpo, ypo, fontsize), colour, screen):
    font=pygame.font.Font(None,fontsize)
    label=font.render(str(text), 1, (colour))
    screen.blit(label,(xpo,ypo))

# define function that checks for touch location
def on_touch():
    # get the position that was touched
    touch_pos = pygame.mouse.get_pos()
    touch_pos = (touch_pos[0], touch_pos[1])
    # button 1 event x_min, x_max, y_min, y_max
    if 30 <= touch_pos[0] <= 240 and 105 <= touch_pos[1] <=160:
        return 1
    # button 2 event
    if 260 <= touch_pos[0] <= 470 and 105 <= touch_pos[1] <=160:
        return 2
    # button 3 event
    if 30 <= touch_pos[0] <= 240 and 180 <= touch_pos[1] <=235:
        return 3
    # button 4 event
    if 260 <= touch_pos[0] <= 470 and 180 <= touch_pos[1] <=235:
        return 4
    # button 5 event
    if 30 <= touch_pos[0] <= 240 and 255 <= touch_pos[1] <=310:
        return 5
    # button 6 event
    if 260 <= touch_pos[0] <= 470 and 255 <= touch_pos[1] <=310:
        return 6

def run_cmd(cmd):
    process = Popen(cmd.split(), stdout=PIPE)
    output = process.communicate()[0]
    return output

def run_proc(proc, f, a):
    pygame.quit()
    process = call(proc, shell=True)
    os.execv(f, a)

# Define each button press action
def button(number, _1, _2, _3, _4, _5, _6):
    if number == 1:
        _1()
        return
    if number == 2:
        _2()
        return
    if number == 3:
        _3()
        return
    if number == 4:
        _4()
        return
    if number == 5:
        _5()
        return
    if number == 6:
        _6()
        return

def init(draw=True):
    # init os environment
    os.environ["SDL_FBDEV"] = SCREEN_DEVICE
    os.environ["SDL_MOUSEDEV"] = TOUCH_DEVICE
    os.environ["SDL_MOUSEDRV"] = MOUSE_DRIVER

    # Initialize pygame modules individually (to avoid ALSA errors) and hide mouse
    pygame.font.init()
    pygame.display.init()
    pygame.mouse.set_visible(0)

    if draw:
        # Customise layout
        # Set size of the screen
        screen = pygame.display.set_mode(size)
        # Background Color
        screen.fill(black)
        # Outer Border
        pygame.draw.rect(screen, tron_regular, (0,0,479,319),8)
        pygame.draw.rect(screen, tron_light, (2,2,479-4,319-4),2)

        return screen

def populate_screen(names, screen, service=["","","","","",""], label1=True,
        label2=False, label3=False, b12=True, b34=True, b56=True):
    # Buttons and labels
    # First Row Label
    if label1:
        make_label(names[0], label_pos_1, tron_inverse, screen)
    # Second Row buttons 3 and 4
    if b12:
        make_button(names[1], button_pos_1, s2c(service[0]), screen)
        make_button(names[2], button_pos_2, s2c(service[1]), screen)
    elif label2:
        make_label(names[1], label_pos_2, tron_inverse, screen)
    # Third Row buttons 5 and 6
    if b34:
        make_button(names[3], button_pos_3, s2c(service[2]), screen)
        make_button(names[4], button_pos_4, s2c(service[3]), screen)
    elif label3:
        make_label(names[3], label_pos_3, tron_inverse, screen)
    # Fourth Row Buttons
    if b56:
        make_button(names[5], button_pos_5, s2c(service[4]), screen)
        make_button(names[6], button_pos_6, s2c(service[5]), screen)

def main(buttons=[]):
    if buttons:
        [_1, _2, _3, _4, _5, _6] = buttons
        sleep_delay=0.1
    else:
        sleep_delay=0.4
    #While loop to manage touch screen inputs
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons:
                    pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
                    b = on_touch()
                    button(b, _1, _2, _3, _4, _5, _6)
                else:
                    screen_on()

            #ensure there is always a safe way to end the program if the touch screen fails
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()
        if buttons:
            pygame.display.update()
        ## Reduce CPU utilisation
        time.sleep(sleep_delay)

################################################################################
