#!/usr/bin/env python
from threading import Lock
from flask import Flask, render_template, session, request, url_for
from flask_socketio import SocketIO, emit
import time
import socket
import json
import redis
import numpy as np

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
# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__, static_url_path="/static")
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

database = redis.Redis(host='localhost', port=6379,)

class SocketReceiver:
    '''demonstration class only
      - coded for clarity, not efficiency
    '''
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
          oneframe = eval("".join(chunk))
          return oneframe
        else :
          chunk.append(ichar)


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    heatmap_data = []
    heatmap_json = []
    for i in range(50):
        for j in range(50):
            heatmap_json.append([i, j, 0])
    client = SocketReceiver();
    while True:
        global database
        s = database.get('pic')
        socketio.sleep(0.1)
        count += 1
        position_data = json.loads(s);
        position_data = position_data[0]


        if heatmap_data == []:
            heatmap_data = np.array(position_data)
        else:
            try:
                heatmap_data = (heatmap_data * count + np.array(position_data)) / count;
            except:
                pass

        if count % 10 == 0:
            heatmap_json = []
            for i in range(50):
                for j in range(50):
                    heatmap_json.append([i, j, 0])
            for point in heatmap_data:
                try:
                    heatmap_json[int((point[0] + 5) * 5) * 50 + int((point[1] + 5) * 5)][2] = 0.7
                except:
                    pass


        sitting = None


        socketio.emit('my_response',
                      {'data': s, 'count': count, 'heatmap': json.dumps(heatmap_json), 'sitting': sitting},
                      namespace='/test')


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('my_event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.on('my_ping', namespace='/test')
def ping_pong():
    emit('my_pong')


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)
    # emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':

    socketio.run(app, debug=True)
