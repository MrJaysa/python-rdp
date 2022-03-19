from flask import Flask, jsonify, request
import Xlib.threaded
from flask_socketio import SocketIO, send, emit, disconnect
from flask_cors import CORS
from model import Users
from secrets import token_hex
from uuid import uuid4
from engineio.payload import Payload

app = Flask(__name__)
app.config['SECRET_KEY'] =  uuid4().hex + token_hex(32)
cors = CORS(app)
Payload.max_decode_packets = 500
socket = SocketIO(app, async_mode='gevent', engineio_logger=False, cors_allowed_origins=['file://', "null"])

users = Users()

@socket.on("message")
def message(payload):
    check_user = users.get_devices_by_rid(payload['id'])

    if not check_user:
        users.create(
            sid = request.sid,
            typ = payload.get('type'),
            pwd = payload.get('pass'),
            rid = payload.get("id") if payload.get("id") else "12345"
        )
    send({
        "user" : users.return_desktop_type(),
        "message": "users list, message",
        "status": 200,
        "status_id": payload.get("id")
    }, broadcast=True)


@socket.on('disconnect')
def disconnect():
    users.remove_by_sid(request.sid)
    print(f'{request.sid}, disconnected')
    send({
        "user" : users.return_desktop_type(),
        "message": "users list for disconnection",
        "status": 200
    }, broadcast=True)

@socket.on('connect_users')
def connect_users(payload):
    check = users.check_user(payload.get('id'), payload.get('pwd'))
    if check:
        emit("establish_connection", {
            "status": 200,
            "msg": f"establishing connection to user with rid: {check.rid}",
            'user': check.rid
        }, room=request.sid)

    else:
        emit("establish_connection",{
            "status": 400,
            "msg": "Password entered is wrong please try again"
        }, room=request.sid)

@socket.on('trigger_desktop')
def trigger_desktop(user):
    client = users.get_devices_by_sid(request.sid)
    dev_client = users.get_devices_by_rid(user)
    emit('establish_connection', {
        "status": 200,
        "msg": f"establishing connection to user with rid: {client.rid}",
        "user": client.rid
    }, room=dev_client.sid)

@socket.on('streamer')
def streamer(payload):
    client = users.get_devices_by_rid(payload['user'])
    if client:
        emit("img_stream", payload['data'], room=client.sid)
    print('device not found')

@socket.on('received_signal')
def received_signal(data):
    pass

@app.errorhandler(Exception)
def error(err):
    try:
        return jsonify({
            'message': str(err),
            'status' : err.code
        }), err.code

    except:
        return jsonify({
            'message': str(err),
            'status' : 500
        }), 500

if __name__ == "__main__":
    socket.run(app, host="0.0.0.0", debug=True, port=3001)