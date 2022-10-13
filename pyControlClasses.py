import socket
import json
import pyconsettings as set


class Controller:
    def __init__(self, name, ip_address, port):
        self.name = name
        self.ip = ip_address
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.language = 'utf-8'
        self.sock.connect((self.ip, self.port))
        self.sock.settimeout(.5)
        welcome = self.sock.recv(1024)
        print(welcome.decode())

    def send(self, message):
        byte_message = f'{message}\r'.encode()
        print(f'Sent: {message}')
        bytestring = b''
        fragments = []
        count = 0
        self.sock.send(byte_message)
        try:
            while True:
                chunk = self.sock.recv(4096)
                count += 1
                fragments.append(chunk)
                if len(chunk) < 1:
                    break

        except:
            pass
        bytestring = b''.join(fragments)
        message = bytestring.decode()
        print(f'Received: {message}')
        print()
        return message

    def get_Matrix(self):
        matrix = self.send('matrix get')
        return matrix

    def get_Devicelist(self):
        devices = self.send('config get devicelist')
        devices = devices.split()
        del devices[0:2]
        return devices

    def get_Settings(self):
        # Currently Crashes
        settings = self.send('config get devicejsonstring')
        try:
            data = settings.split(":", 1)
            data = data[1]
            js = json.loads(data)
            js = json.dumps(js, indent=2)
            return js
        except:
            return ('Failed to get settings')

    def set_Bezel(self, bezel_size):
        # Expecting List of 4 int OW, OH, VW, VH
        # OW = Overall Width
        # OH = Overall Height
        # VW = Viewing Width
        # VH = Viewing Height
        bezel = self.send('vw get')
        print('Starting Bezel adjustments')
        walls = bezel.splitlines()
        # remove items with "Row"
        walls = [x for x in walls if not x.startswith("Row")]
        # remove items with "Video"
        walls = [x for x in walls if not x.startswith("Video")]
        # remove end of each item in list after space
        walls = [item.split(' ', 1)[0] for item in walls]
        # remove empty strings
        walls = [x for x in walls if x]
        print('List of video walls found')
        print(walls)
        for item in walls:
            self.send(
                f'vw bezelgap {item} {bezel_size[0]} {bezel_size[1]} {bezel_size[2]} {bezel_size[3]}')

    def reboot(self):
        devices = self.get_Devicelist()
        for device in devices:
            self.send(f'config set device reboot {device}')

    def ir(self, ir_command, *device):
        if device:
            self.send(f'infrared "{ir_command}" {device}')
        else:
            self.send(f'infrared "{ir_command}" ALL_RX')

    def set_Matrix(self, encoder, decoder):
        matrixstr = f'matrix set {encoder} {decoder}'
        self.send(matrixstr)

    def set_Scene(self, scene):
        self.send(f'scene active {scene}')

    def disconnect_All(self):
        self.send(f'matrix set NULL ALL_RX')


class BrightSign:
    def __init__(self, name, ip_address, port):
        self.name = name
        self.ip = ip_address
        self.port = port
        self.communication = 'UDP'
        self.movielist = set.movielist
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(
            f'Creating new BrightSign Player : Name={self.name}, IP={self.ip}:{self.port}')

    def message(self, message):
        # Encode message and send to BrightSign
        self.socket.sendto(message.encode('ascii'), (self.ip, self.port))

    def select_Movie(self, movie):
        # Select Movie to play
        self.message(movie)

    def reboot(self):
        self.message('Leviathan')
        self.message('reboot')
