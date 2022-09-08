import socket
import time
import logging
import json

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', filename="log.txt", level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info("Starting Log")


def log(text):
    # Log and log text
    print(text)
    logger.info(text)


# Controller Information
CON_IP = "10.0.0.100"
CON_PORT = 23

# Controller Socket Connection
con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
con.connect((CON_IP, CON_PORT))
con.settimeout(2)
log(f'Creating Socket to Controller at {CON_IP}:{CON_PORT}')
welcome = con.recv(1024)
log(welcome.decode())


def byte(command):
    # use byte(string) to convert to byte string before sending to controller. ex: con.send(byte(hello))
    bytestring = f"{command} \r\n".encode()
    return bytestring


def recvall(sock, msg):
    sock.send(byte(msg))
    arr = b''
    fragments = []
    count = 0
    try:
        while True:
            chunk = sock.recv(4096)
            count += 1
            if len(chunk) < 400:

                break
            fragments.append(chunk)
        arr = b''.join(fragments)
    except:
        log("Received Timeout")

    log(f'Received {count} blocks of data')
    return arr


def getsettings(sock, msg):
    data = recvall(sock, msg)
    data = data.decode()
    data = data.split(":", 1)
    #data = data[1]
    js = json.loads(data)
    js = json.dumps(js, indent=2)
    print(data)


#########SETTINGS START#############
# Bezel size .01mm
# vw bezelgap vw-name ow oh vw vh
# Samsung Demo office 9144 5270 8890 4953
# inches to .01mm (inches x 254)
OW = 9144
OH = 5270
VW = 8890
VH = 4953


def setbezel():
    log("Starting Bezel adjustments")
    con.send(byte("vw get"))
    msg = con.recv(1024)
    time.sleep(1)
    fullmsg = msg.decode()
    walls = fullmsg.splitlines()
    # remove items with "Row"
    walls = [x for x in walls if not x.startswith("Row")]
    # remove items with "Video"
    walls = [x for x in walls if not x.startswith("Video")]
    # remove end of each item in list after space
    walls = [item.split(' ', 1)[0] for item in walls]
    # remove empty strings
    walls = [x for x in walls if x]
    log(walls)
    for item in walls:
        con.send(byte(f'vw bezelgap {item} {OW} {OH} {VW} {VH}'))
        log(f'vw bezelgap {item} {OW} {OH} {VW} {VH}')
        time.sleep(.5)


# Encoder names, Set the name as the host name from the Encoders
EN01 = "IPE6000W-XXXXXXXXXXXX"
EN02 = "IPE6000W-XXXXXXXXXXXX"
EN03 = "IPE6000W-XXXXXXXXXXXX"
EN04 = "IPE6000W-XXXXXXXXXXXX"
EN05 = "IPE6000W-XXXXXXXXXXXX"
EN06 = "IPE6000W-XXXXXXXXXXXX"
EN07 = "IPE6000W-XXXXXXXXXXXX"
EN08 = "IPE6000W-XXXXXXXXXXXX"
EN09 = "IPE6000W-XXXXXXXXXXXX"
EN10 = "IPE6000W-XXXXXXXXXXXX"
EN11 = "IPE6000W-XXXXXXXXXXXX"
EN12 = "IPE6000W-XXXXXXXXXXXX"
EN13 = "IPE6000W-XXXXXXXXXXXX"
EN14 = "IPE6000W-XXXXXXXXXXXX"
EN15 = "IPE6000W-XXXXXXXXXXXX"
EN16 = "IPE6000W-XXXXXXXXXXXX"
EN17 = "IPE5100-BABB87D44C6A"
EN18 = "IPE5100-341B22F00532"
EN19 = "IPE5100-8ACBD04FAB3F"
EN20 = "IPE5100-CE17116E0D56"


# Decoder names, Set the name as the host name from the Decoders
DEC01 = "IPD6000W-341B22F00502"
DEC02 = "IPD6000W-341B22F004C0"
DEC03 = "IPD6000W-XXXXTEST3XXX"
DEC04 = "IPD6000W-XXXXTEST4XXX"
DEC05 = "IPD5100-5A070AC4E24B"
DEC06 = "IPD5100-9A7A201CE92F"
DEC07 = "IPD5100-CAC95249B11C"
DEC08 = "IPD5100-C6D6B6467C22"
DEC09 = "IPD6000W-XXXXXXXXXXXX"
DEC10 = "IPD6000W-XXXXXXXXXXXX"
DEC11 = "IPD6000W-XXXXXXXXXXXX"
DEC12 = "IPD6000W-XXXXXXXXXXXX"
DEC13 = "IPD6000W-XXXXXXXXXXXX"
DEC14 = "IPD6000W-XXXXXXXXXXXX"
DEC15 = "IPD6000W-XXXXXXXXXXXX"
DEC16 = "IPD6000W-XXXXXXXXXXXX"
DEC17 = "IPD6000W-XXXXXXXXXXXX"
DEC18 = "IPD6000W-XXXXXXXXXXXX"
DEC19 = "IPD6000W-XXXXXXXXXXXX"
DEC20 = "IPD6000W-XXXXXXXXXXXX"


# Alias Names, Set the name for the source connected to the Encoder
# rename ETEMPxx to the name you would like to use ex: change ETEMP02 to apple_TV_1
tba2 = EN01
bright1 = EN02
apple1 = EN05
bright2 = EN06
source3 = EN08
muredio = EN07


# Alias Names, Set the name for the Display connected to the Dencoder
# rename DTEMPxx to the name you would like to use ex: change DTEMP01 to living_room
tv1 = DEC01
tv2 = DEC02
tv3 = DEC03
tv4 = DEC04

# Brightsign UDP Socket
BR1_IP = "10.0.0.35"
BR1_PORT = 5000
br1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Server Information - Device Python is running on
WEB_IP = "10.0.0.18"
WEB_PORT = 65432

# B-260 IR Codes
SWINPUT1 = "0000 006D 0022 0002 0155 00AA 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0040 0015 0040 0015 0040 0015 0040 0015 0040 0015 0040 0015 0040 0015 0040 0015 0015 0015 0015 0015 0040 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0040 0015 0040 0015 0015 0015 0040 0015 0040 0015 0040 0015 0040 0015 0040 0015 05ED 0155 0055 0015 0E47"
SWINPUT2 = "0000 006D 0022 0002 0155 00AA 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0040 0015 0040 0015 0040 0015 0040 0015 0040 0015 0040 0015 0040 0015 0040 0015 0015 0015 0015 0015 0040 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0040 0015 0040 0015 0015 0015 0040 0015 0040 0015 0040 0015 0040 0015 0040 0015 05ED 0155 0055 0015 0E47"
SWINPUT3 = "0000 006D 0022 0002 0155 00AA 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0040 0015 0040 0015 0040 0015 0040 0015 0040 0015 0040 0015 0040 0015 0040 0015 0015 0015 0040 0015 0040 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0040 0015 0015 0015 0015 0015 0040 0015 0040 0015 0040 0015 0040 0015 0040 0015 05ED 0155 0055 0015 0E47"
SWINPUT4 = "0000 006D 0022 0002 0155 00AA 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0040 0015 0040 0015 0040 0015 0040 0015 0040 0015 0040 0015 0040 0015 0040 0015 0015 0015 0015 0015 0040 0015 0040 0015 0015 0015 0015 0015 0015 0015 0015 0015 0040 0015 0040 0015 0015 0015 0015 0015 0040 0015 0040 0015 0040 0015 0040 0015 05ED 0155 0055 0015 0E47"


def setinput(input):
    # expects int 1-4 for the input
    if input == 1:
        con.send(byte(f'infrared "{SWINPUT1}" IPD5100-5A070AC4E24B'))
        log(f'Setting Switcher input to {SWINPUT1}')

# Keypad Button Locations
###1,6###
###2,7###
###3,8###
###4,9###
###5,10##


# Change Keyx to string that is coming from Keypad
# Do not send \r or \n always send None
KEY1 = "Key1"
KEY2 = "Key2"
KEY3 = "Key3"
KEY4 = "Key4"
KEY5 = "Key5"
KEY6 = "Key6"
KEY7 = "Key7"
KEY8 = "Key8"
KEY9 = "Key9"
KEY10 = "Key10"

#### CEC Commands ####
INPUT1 = "4f821000"
INPUT2 = "4f822000"
INPUT3 = "4f823000"
PWRON = "4004"
PWROFF = "4036"
DEFAULT_INPUT = "HDMI 1"  # Name of Default Input
DEFAULT_SCENE = "Wall"  # Name of Default on Scene
# IP5100 CEC Command "cec_send CEC_FRAME"

#########SETTINGS END#############

##### Global Variables #####
pwrstatus = False
mx = 1
wall = 1
brmsg = 1
##### Global End #####


def bright(message):
    br1.sendto(message, (BR1_IP, BR1_PORT))
    log(f'Sending to BrightSign: {message}, ({BR1_IP}, {BR1_PORT})')


def matrix(encoder, decoder):
    # Used to set any encoder to any decoder manually
    matrixstr = f'matrix set {encoder} {decoder}'
    log(f'Connecting {encoder} to {decoder}')
    con.send(byte(matrixstr))


def all_on():
    # Power on TV's via CEC & set inputs.
    global wall
    con.send(byte(f'scene active 5100Wall-5100W{wall}'))
    log(f'Setting Scene to 5100Wall-5100W{wall}')
    wall += 1

    con.send(byte(f'cec "{PWRON}" ALL_RX'))
    con.send(byte(f'config set device cec onetouchplay ALL_RX'))
    log("Turning on all devices...")
    time.sleep(5)

    con.send(byte(f'cec "{INPUT1}" ALL_RX'))
    log(f'Setting input to {DEFAULT_INPUT}')
    time.sleep(2)


def all_off():
    # Turn off TV's after sending Input command
    global wall
    global mx
    con.send(byte(f'cec "{DEFAULT_INPUT}" ALL_RX'))
    log(f'Sending default {DEFAULT_INPUT} command')
    time.sleep(2)

    con.send(byte(f'cec "{PWROFF}" ALL_RX'))
    con.send(byte(f'config set device cec standby ALL_RX'))
    wall = 1
    mx = 1
    log(f'Sending All off CEC Command')
    time.sleep(5)

    con.send(byte(f'matrix set NULL ALL_RX'))
    log(f'Disconnecting all Sources')


def macro01():
    # Toggle all on/off
    log("Starting macro01")
    global pwrstatus
    if pwrstatus == False:
        all_on()
        pwrstatus = True
    else:
        all_off()
        pwrstatus = False


def macro02():
    # Rotate through Video walls
    log("Starting macro03")
    global wall
    log(f'Starting Video Wall {wall}')
    wallstr = f'scene active 5100Wall-5100W{wall}'
    con.send(byte(wallstr))
    wall += 1
    if wall >= 5:
        wall = 1


def macro03():
    # Switch Matrix Scene 1-4
    log("Starting macro02")
    global mx
    log(f'Starting Matrix Scene {mx}')
    mxstr = f'scene active 5100Wall-5100MX{mx}'
    con.send(byte(mxstr))
    mx += 1
    if mx >= 5:
        mx = 1


def macro04():
    # Swap Brightsign Video
    global brmsg
    log("Starting macro04")
    if brmsg >= 5:
        brmsg = 1
    else:
        brmsg += 1
    msg = f'dbv{brmsg}'  # ex dbv1, dbv2
    log(f'Sending {msg} to BrightSign')
    br1.sendto(msg.encode('ascii'), (BR1_IP, BR1_PORT))


def macro05():
    # Description of macro
    recvall(con, f'config get telnet alias')
    pass


def macro06():
    # Description of macro
    log("Starting macro06")
    global pwrstatus
    if pwrstatus == False:
        all_on()
        pwrstatus = True
    else:
        all_off()
        pwrstatus = False


def macro07():
    # Description of macro
    log("Starting macro07")
    global mx
    log(f'Starting Matrix Scene {mx}')
    mxstr = f'scene active 6000Wall-6000MX{mx}'
    con.send(byte(mxstr))
    mx += 1
    if mx >= 5:
        mx = 1


def macro08():
    # Description of macro
    log("Starting macro08")
    global wall
    log(f'Starting Video Wall {wall}')
    wallstr = f'scene active 6000Wall-6000W{wall}'
    con.send(byte(wallstr))
    wall += 1
    if wall >= 5:
        wall = 1


def macro09():
    # Description of macro
    global brmsg
    log("Starting macro09")
    if brmsg >= 5:
        brmsg = 1
    else:
        brmsg += 1
    msg = f'dbv{brmsg}'
    log(f'Sending {msg} to BrightSign')
    br1.sendto(msg.encode('ascii'), (BR1_IP, BR1_PORT))


def macro10():
    # Description of macro
    log("Starting macro10")
    pass


#print(getsettings(con, f'config get devicejsonstring'))
setbezel()
setinput(1)


log("Starting Socket to listen for Keypad commands")
# Socket incoming from Keypad
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((WEB_IP, WEB_PORT))
    s.listen()
    conn, addr = s.accept()
    log(f'Listening on {WEB_IP},{WEB_PORT}')
    with conn:
        log(f"Connected by {addr}")
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                # conn.sendall(data)
                request = str(data.decode().title())
                log(f'Requesting: {request}')

            except socket.timeout:
                log("Caught a timeout error")

            if request == "Key1":
                macro01()

            if request == "Key2":
                macro02()

            if request == "Key3":
                macro03()

            if request == "Key4":
                macro04()

            if request == "Key5":
                macro05()

            if request == "Key6":
                macro06()

            if request == "Key7":
                macro07()

            if request == "Key8":
                macro08()

            if request == "Key9":
                macro09()

            if request == "Key10":
                macro10()

con.close()
