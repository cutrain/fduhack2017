import redis
import client

if __name__ == '__main__':
    r = redis.Redis(
        host='localhost',
        port=6379,
    )

    cli = client.SocketReceiver()
    cli.connect('localhost', 12345)
    while True:
        r.set('pic', cli.receiveFrame())

