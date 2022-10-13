'''
Create macro's for IP6000 on key's 6-10
'''
import socket
import time
import logging
import json
import urllib.request
import urllib.error
import pyconsettings as set
import pyControlClasses as py

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', filename="log.txt", level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info("Starting Log")
# Constructors
# Controller
con = py.Controller('SC009', set.CON_IP, set.CON_PORT)

# BrightSign
br1 = py.BrightSign('BR1', set.BR1_IP, set.BR_PORT)
br2 = py.BrightSign('BR2', set.BR2_IP, set.BR_PORT)
br3 = py.BrightSign('BR3', set.BR3_IP, set.BR_PORT)
br4 = py.BrightSign('BR4', set.BR4_IP, set.BR_PORT)
units = [br1, br2, br3, br4]


def wait_for_network():
    while True:
        try:
            print('Waiting on Network')
            response = urllib.request.urlopen('http://10.0.0.100', timeout=10)
            return
        except urllib.error.URLError:
            pass


def log(text):
    # Log and log text
    print(text)
    logger.info(text)


def setinput(input):
    # expects int 1-4 for the input
    if input == 1:
        con.ir(set.SWINPUT1)
        log(f'Setting Switcher input to {input}')
    elif input == 2:
        con.ir(set.SWINPUT2)
        log(f'Setting Switcher input to {input}')
    elif input == 3:
        con.ir(set.SWINPUT3)
        log(f'Setting Switcher input to {input}')
    else:
        con.ir(set.SWINPUT4)
        log(f'Setting Switcher input to {input}')


##### Global Variables #####
pwrstatus = False
mx = 1
wall = 1
brmsg = 1
##### Global End #####


def all_on():
    # Power on TV's via CEC & set inputs.
    global wall
    con.set_Scene(f'scene active 5100Wall-5100W{wall}')
    log(f'Setting Scene to 5100Wall-5100W{wall}')
    wall += 1
    setinput(1)

    # con.send(byte(f'cec "{set.PWRON}" ALL_RX'))
    # con.send(byte(f'config set device cec onetouchplay ALL_RX'))
    # log("Turning on all devices...")
    # time.sleep(5)

    # con.send(byte(f'cec "{set.CECINPUT1}" ALL_RX'))
    # log(f'Setting input to {set.DEFAULT_INPUT}')
    # time.sleep(2)

    br1.select_Movie('Leviathan')
    br2.select_Movie('blackpanther')
    br3.select_Movie('Guardians2')
    br4.select_Movie('Starwarslast')


def start5100():
    global wall
    con.set_Scene(f'5100Wall-5100W{wall}')
    log(f'Setting Scene to 5100Wall-5100W{wall}')
    wall += 1
    setinput(1)

    br1.select_Movie('Leviathan')
    br2.select_Movie('Blackpanther')
    br3.select_Movie('Guardians2')
    br4.select_Movie('Starwarslast')


def start6000():
    global wall
    con.set_Scene(f'6000Wall-6000W{wall}')
    log(f'Setting Scene to 6000Wall-6000W{wall}')
    wall += 1
    setinput(2)


def all_off():
    # Turn off TV's after sending Input command
    global wall
    global mx
    # con.send(byte(f'cec "{set.DEFAULT_INPUT}" ALL_RX'))
    # log(f'Sending default {set.DEFAULT_INPUT} command')
    # time.sleep(2)

    # con.send(byte(f'cec "{set.PWROFF}" ALL_RX'))
    con.send(f'config set device cec standby ALL_RX')
    wall = 1
    mx = 1
    log(f'Sending All off CEC Command')
    time.sleep(5)

    con.disconnect_All()
    log(f'Disconnecting all Sources')


def macro01():
    # Toggle all on/off
    log("Starting macro01")
    start5100()
    # global pwrstatus
    # if pwrstatus == False:
    #     all_on()
    #     pwrstatus = True
    # else:
    #     all_off()
    #     pwrstatus = False


def macro02():
    # Rotate through Video walls
    log("Starting macro02")
    global wall
    log(f'Starting Video Wall {wall}')
    con.set_Scene(f'5100Wall-5100W{wall}')
    wall += 1
    if wall >= 5:
        wall = 1


def macro03():
    # Switch Matrix Scene 1-4
    log("Starting macro03")
    global mx
    log(f'Starting Matrix Scene {mx}')
    con.set_Scene(f'5100Wall-5100MX{mx}')
    mx += 1
    if mx >= 5:
        mx = 1


def macro04():
    # Restart Movies
    log("Starting macro04")
    for device in units:
        device.select_Movie('CoreUniverse')

    br1.select_Movie('Leviathan')
    br2.select_Movie('Guardians2')
    br3.select_Movie('Starwarslast')
    br4.select_Movie('Blackpanther')


def macro05():
    # Description of macro
    pass


def macro06():
    # Description of macro
    log("Starting macro06")
    start6000()


def macro07():
    # Description of macro
    log("Starting macro07")
    global mx
    log(f'Starting Matrix Scene {mx}')
    con.set_Scene(f'6000Wall-6000MX{mx}')

    mx += 1
    if mx >= 5:
        mx = 1


def macro08():
    # Description of macro
    log("Starting macro08")
    global wall
    log(f'Starting Video Wall {wall}')
    con.set_Scene(f'6000Wall-6000W{wall}')
    wall += 1
    if wall >= 5:
        wall = 1


def macro09():
    # Description of macro
    macro04()


def macro10():
    # Description of macro
    pass


# Core Program
wait_for_network()
con.set_Bezel(set.bezel)
log("Starting Socket to listen for Keypad commands")


# Socket incoming from Keypad
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((set.WEB_IP, set.WEB_PORT))
    s.listen()
    conn, addr = s.accept()
    log(f'Listening on {set.WEB_IP},{set.WEB_PORT}')
    with conn:
        log(f"Connected by {addr}")
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                request = str(data.decode().title())
                log(f'Requesting: {request}')

            except socket.timeout:
                log("Caught a timeout error")

            if request == set.KEY1:
                macro01()
            elif request == set.KEY2:
                macro02()
            elif request == set.KEY3:
                macro03()
            elif request == set.KEY4:
                macro04()
            elif request == set.KEY5:
                macro05()
            elif request == set.KEY6:
                macro06()
            elif request == set.KEY7:
                macro07()
            elif request == set.KEY8:
                macro08()
            elif request == set.KEY9:
                macro09()
            elif request == set.KEY10:
                macro10()
            else:
                log("Invalid Input from Request")
