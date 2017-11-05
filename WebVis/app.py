#!/usr/bin/env python
from threading import Lock
from flask import Flask, render_template, session, request, url_for
from flask_socketio import SocketIO, emit
from enum import Enum
import math
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

class body(object):
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
        ans = math.sqrt(vec[0] * vec[0] + vec[1] * vec[1] + vec[2] * vec[2])
        if -1e-9 < ans < 1e-9:
            ans = 1e-7
        return ans

    def angle(self, p):
        v = []
        for i in range(3):
            v.append(p[i]-self.p[i])
        return math.acos(
            (v[0]*self.v[0] + v[1] * self.v[1] + v[2] * self.v[2]) /
            (self.veclen(v) * self.veclen(self.v))
        ) * 180. / 3.14159

    def dis(self, p):
        v = []
        for i in range(3):
            v.append(p[i]-self.p[i])
        ang = self.angle(p)
        ans = self.veclen(self.v) * math.sin(ang * 3.14159 / 180.)
        return ans

def check_body(bp):
    b = body()
    top = bp[b.Head]
    bottom = bp[b.SpineBase]
    line = vector(top, bottom)
    badness = 0
    # body spine
    badness += line.dis(bp[b.Neck])
    badness += line.dis(bp[b.SpineShoulder])
    badness += line.dis(bp[b.SpineMid])
    # body shoulder
    shoulder = vector(bp[b.SpineShoulder], bp[b.ShoulderLeft])
    angle = shoulder.angle(bp[b.ShoulderRight])
    print badness, '%', angle
    # a = True
    # b = True
    # if badness >0.4:
    #     a = False
    # if angle < 140:
    #     b = False

    # return -
    return [badness, angle]
    # print badness,angle
    # if badness > 0.4 and angle < 145:
    #     return 3
    # if badness > 0.4 and angle >= 145:
    #     return 2
    # if badness < 0.4 and angle < 145:
    #     return 1
    return 0


def right_position(body):
    state = check_body(body)
    # from tts import TextToSpeech
    # tapi = TextToSpeech()
    # if state == 0:
        # wav = tapi.post("Perfect")
    # elif state == 1:
        # wav = tapi.post("Good")
    # else:
        # wav = tapi.post("Better nect time")
    # tapi.play(istream=wav)
    return state

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    heatmap_data = []
    # heatmap_json = []
    # for i in range(50):
    #     for j in range(50):
    #         heatmap_json.append([i, j, 0])
    while True:
        global database
        s = database.get('pic')
        socketio.sleep(0.1)
        count += 1
        position_data = json.loads(s);
        position_data = position_data[0]
        state = check_body(position_data)
        print 'state :', state

        if heatmap_data == []:
            heatmap_data = np.array(position_data)
        else:
            try:
                heatmap_data = (heatmap_data * (count - 1) + np.array(position_data)) / count;
            except:
                pass

        # if count % 10 == 0:
        #     heatmap_json = []
        #     for i in range(50):
        #         for j in range(50):
        #             heatmap_json.append([i, j, 0])
        #     for point in heatmap_data:
        #         try:
        #             heatmap_json[int((point[0] + 5) * 5) * 50 + int((point[1] + 5) * 5)][2] = 0.7
        #         except:
        #             pass


        socketio.emit('my_response',
                      {'data': s, 'count': count, 'heatmap': str([list(x) for x in heatmap_data]), 'badness': state[0], 'angle':state[1]},
                      namespace='/test')


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@app.route('/audio/<string:text>', methods=['POST'])
def audio(text):
    from tts import TextToSpeech
    tapi = TextToSpeech()
    tapi.post(text, text+'.wav')

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
