#!/usr/bin/env python
from threading import Lock
from flask import Flask, render_template, session, request, url_for
from flask_socketio import SocketIO, emit
from enum import Enum
import time
import socket
import json
import redis

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

class body(Enum):
    SpineBase = 0
    SpineMid  = 1
    Neck  = 2
    Head  = 3
    ShoulderLeft  = 4
    ElbowLeft = 5
    WristLeft = 6
    HandLeft  = 7
    ShoulderRight = 8
    ElbowRight    = 9
    WristRight    = 10
    HandRight = 11
    HipLeft   = 12
    KneeLeft  = 13
    AnkleLeft = 14
    FootLeft  = 15
    HipRight  = 16
    KneeRight = 17
    AnkleRight    = 18
    FootRight = 19
    SpineShoulder = 20
    HandTipLeft   = 21
    ThumbLeft = 22
    HandTipRight  = 23
    ThumbRight    = 24
    Count = ThumbRight + 1

class vector(object):
    def __init__(self, p1, p2):
        self.v = []
        for i in range(3):
            self.v.append(p2[i]-p1[i])
        self.p = p1

    @staticmethod
    def veclen(vec):
        import math
        return math.sqrt(vec[0] * vec[0] + vec[1] * vec[1] + vec[2] * vec[2])

    def dis(self, p):
        v = []
        for i in range(3):
            v.append(p[i]-self.p[i])
        ans = []
        for i in range(3):
            ans.append(self.v[i] * v[i])
        return veclen(ans) / veclen(v[i])

def check_body(bp):
    b = body
    top = bp[b.Head]
    bottom = bp[b.SpineBase]
    line = vector(top, bottom)
    badness = 0
    badness += line.dis(bp[b.Neck])
    badness += line.dis(bp[b.SpineShoulder])
    badness += line.dis(bp[b.SpineMid])
    print badness
    if badness > 0.3:
        return 2
    if badness > 0.1:
        return 1
    return 0


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        global database
        s = database.get('pic')
        socketio.sleep(0.1)
        count += 1
        position_data = json.loads(s);
        print position_data
        print type(position_data)

        position_data = position_data[0]


        socketio.emit('my_response',
                      {'data': s, 'count': count, 'heatmap': heatmap, 'sitting': sitting},
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
