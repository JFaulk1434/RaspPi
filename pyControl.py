# Try/Except on start to help crash when socket not communicating
# Items to fix
'''
Add commands for all 4 Brightsign players
Add IR commands for all 4 Switchers
Create macro's for IP6000 on key's 6-10
Add different commands for Brightsign videos

'''
import socket
import time
import logging
import json
import pyconsettings as set

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', filename="log.txt", level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info("Starting Log")


def log(text):
    # Log and log text
    print(text)
    logger.info(text)


# Controller Socket Connection
con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
con.settimeout(2)
try:
    con.connect((set.CON_IP, set.CON_PORT))
    log(f'Creating Socket to Controller at {set.CON_IP}:{set.CON_PORT}')
    welcome = con.recv(1024)
    log(welcome.decode())
except:
    log(
        f'Connection Failed while attempting to connect to {set.CON_IP}:{set.CON_PORT}')


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

    except:
        log("Received Timeout")

    arr = b''.join(fragments)
    arr = arr.decode()
    log(f'Received {count} blocks of data')
    return arr


def getsettings(sock, msg):
    try:
        data = recvall(sock, msg)
        data = data.split(":", 1)
        data = data[1]
        js = json.loads(data)
        js = json.dumps(js, indent=2)
        log(js)
    except:
        log(f'Unable to get settings')


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
        con.send(
            byte(f'vw bezelgap {item} {set.OW} {set.OH} {set.VW} {set.VH}'))
        log(f'vw bezelgap {item} {set.OW} {set.OH} {set.VW} {set.VH}')
        time.sleep(.5)


# Brightsign UDP Socket

brs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# B-260 IR Codes
SWINPUT1 = "0000 006D 0022 0002 0155 00AA 0015 0015 0015 0040 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0040 0015 0015 0015 0040 0015 0040 0015 0040 0015 0040 0015 0040 0015 0040 0015 0015 0015 0015 0015 0040 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0040 0015 0040 0015 0015 0015 0040 0015 0040 0015 0040 0015 0040 0015 0040 0015 05ED 0155 0055 0015 0E47"
SWINPUT2 = "0000 006D 0022 0002 0155 00AA 0015 0015 0015 0040 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0040 0015 0015 0015 0040 0015 0040 0015 0040 0015 0040 0015 0040 0015 0040 0015 0040 0015 0015 0015 0040 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0040 0015 0015 0015 0040 0015 0040 0015 0040 0015 0040 0015 0040 0015 05ED 0155 0055 0015 0E47"
SWINPUT3 = "0000 006D 0022 0002 0155 00AA 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0040 0015 0040 0015 0040 0015 0040 0015 0040 0015 0040 0015 0040 0015 0040 0015 0015 0015 0040 0015 0040 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0040 0015 0015 0015 0015 0015 0040 0015 0040 0015 0040 0015 0040 0015 0040 0015 05ED 0155 0055 0015 0E47"
SWINPUT4 = "0000 006D 0022 0002 0155 00AA 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0040 0015 0040 0015 0040 0015 0040 0015 0040 0015 0040 0015 0040 0015 0040 0015 0015 0015 0015 0015 0040 0015 0040 0015 0015 0015 0015 0015 0015 0015 0015 0015 0040 0015 0040 0015 0015 0015 0015 0015 0040 0015 0040 0015 0040 0015 0040 0015 05ED 0155 0055 0015 0E47"


def setinput(input):
    # expects int 1-4 for the input
    if input == 1:
        con.send(byte(f'infrared "{SWINPUT1}" ALL_RX'))
        log(f'Setting Switcher input to {input}')
    elif input == 2:
        con.send(byte(f'infrared "{SWINPUT2}" ALL_RX'))
        log(f'Setting Switcher input to {input}')
    elif input == 3:
        con.send(byte(f'infrared "{SWINPUT3}" ALL_RX'))
        log(f'Setting Switcher input to {input}')
    else:
        con.send(byte(f'infrared "{SWINPUT4}" ALL_RX'))
        log(f'Setting Switcher input to {input}')


##### Global Variables #####
pwrstatus = False
mx = 1
wall = 1
brmsg = 1
##### Global End #####


def bright(message):
    brs.sendto(message, (set.BR1_IP, set.BR_PORT))
    log(f'Sending to BrightSign: {message}, ({set.BR1_IP}, {set.BR_PORT})')


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
    setinput(1)

    con.send(byte(f'cec "{set.PWRON}" ALL_RX'))
    con.send(byte(f'config set device cec onetouchplay ALL_RX'))
    log("Turning on all devices...")
    time.sleep(5)

    con.send(byte(f'cec "{set.INPUT1}" ALL_RX'))
    log(f'Setting input to {set.DEFAULT_INPUT}')
    time.sleep(2)


def all_off():
    # Turn off TV's after sending Input command
    global wall
    global mx
    con.send(byte(f'cec "{set.DEFAULT_INPUT}" ALL_RX'))
    log(f'Sending default {set.DEFAULT_INPUT} command')
    time.sleep(2)

    con.send(byte(f'cec "{set.PWROFF}" ALL_RX'))
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
    log("Starting macro02")
    global wall
    log(f'Starting Video Wall {wall}')
    wallstr = f'scene active 5100Wall-5100W{wall}'
    con.send(byte(wallstr))
    wall += 1
    if wall >= 5:
        wall = 1


def macro03():
    # Switch Matrix Scene 1-4
    log("Starting macro03")
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
    # Deal with all of the Brightsign players
    brs.sendto(msg.encode('ascii'), (set.BR1_IP, set.BR_PORT))


def macro05():
    # Description of macro
    recvall(con, f'config get telnet alias')
    pass


def macro06():
    # Description of macro
    log("Starting macro06")
    # set IR on switchers to Input2


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
    brs.sendto(msg.encode('ascii'), (set.BR1_IP, set.BR_PORT))


def macro10():
    # Description of macro
    pass


# Core Program
getsettings(con, f'config get devicejsonstring')
setbezel()
setinput(1)


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
