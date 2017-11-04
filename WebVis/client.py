import socket
import json

class SocketReceiver:
    '''demonstration class only
    - coded for clarity, not efficiency
    '''
    jointTypeDict = [
        "SpineBase",
        "SpineMid",
        "Neck",
        "Head",
        "ShoulderLeft",
        "ElbowLeft",
        "WristLeft",
        "HandLeft",
        "ShoulderRight",
        "ElbowRight",
        "WristRight",
        "HandRight",
        "HipLeft",
        "KneeLeft",
        "AnkleLeft",
        "FootLeft",
        "HipRight",
        "KneeRight",
        "AnkleRight",
        "FootRight",
        "SpineShoulder",
        "HandTipLeft",
        "ThumbLeft",
        "HandTipRight",
        "ThumbRight"
    ];

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def receiveFrame(self):
        chunk = []
        while 1:
            ichar = self.sock.recv(min(1, 2048))
            # disconnect
            if ichar == "":
                raise RuntimeError("socket connection broken")
            elif ichar == "*":
                oneframe = "".join(chunk)
                return oneframe
            else :
                chunk.append(ichar)

if __name__ == '__main__':
    client = SocketReceiver()
    client.connect("127.0.0.1", 12345)
    while True:
        client.receiveFrame()
