import socket

MSGLEN = 8;
class mysocket:
    '''demonstration class only
      - coded for clarity, not efficiency
    '''

    positionDict = {
      0 : ""
    }

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
      self.sock.connect((host, port))

    def receiveChar(self):
      chunk = self.sock.recv(min(1, 2048))
      if chunk == '':
        raise RuntimeError("socket connection broken")
      return ''.join(chunk)

    def receiveFrame(self):
      framechunk = []
      jointchunk = []
      wordchunk = []
      while 1:
        ichar = self.sock.recv(min(1, 2048))
        if ichar == '':
          raise RuntimeError("socket connection broken")
        else if ichar = ' ':
          jointchunk.append(wordchunk);
          wordchunk = []
        else if ichar = '\n':
          index = 0
          while index < len(jointchunk):



    def receiveFrame(self):


client = mysocket();
client.connect("127.0.0.1", 12345)
while 1 :
  print client.receiveChar()