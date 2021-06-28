from flask_socketio import emit, disconnect, join_room, leave_room, send, rooms
from web.extensions import socketio
from web.model import Message, User, Room
from .extensions import check_user_token, check_room_id
from flask import request
import flask

'''

讲一下基本思路

public事件为公共频道聊天使用的事件 前端监听public即可 下同

private为私聊事件 区分房间

notice为通知事件 由服务器发起 用于通知用户是否要和某某用户加入私聊


'''

online_user_sid = {}  # 已登录用户的字典（字典好查找） sid作为键 含有应有的所有数据

online_user_id = {}  # id作为键 方便后续房间创建 纯粹是为了房间那一块方便才写的 数据仅有id:sid


# @socketio.on('connect')
# def check_user_token(data):
#     if 1:
#         token = data['token']
#         login_msg = jwt.decode(token, key="priority_queue", algorithms="HS256")
#         login_status = bool(login_msg.get('login_status', None))  # 传入bool值
#         login_user_id = int(login_msg.get('login_user_id', None))  # 登录用户id 必须是全部由数字组成
#         print(request.args)

# except:
#     disconnect()


@socketio.on('login')  # 只需登录一次 节省开销
def chat_check(data):
    temp_dict = check_user_token(data)
    if temp_dict is not None:
        online_user_sid[flask.request.sid] = temp_dict
        online_user_id[temp_dict['id']] = flask.request.sid


@socketio.on('disconnect')
def remove_user_from_login_list():
    try:
        online_user_sid.pop(flask.request.sid)
    except:
        pass

@socketio.on('public')  # 公共频道
def handle_message(data):
    message = data.get('message', ' ')
    sid = flask.request.sid
    if sid in online_user_sid:
        if message is None:
            disconnect()
        else:
            Message.add_message_to_db(user_id=online_user_sid[sid]['id'], body=message, room_id='public')
            socketio.emit('public', {"id": online_user_sid[sid]['id'],
                                     "username": online_user_sid[sid]['name'],
                                     "message": message})  # 公共频道
    else:
        disconnect()


#
# @socketio.on('join')
# def user_room(data):
#     join_room(room=data)


@socketio.on('private')  # 房间和message一起发上来
def private_message(data):
    room_id = data['room_id']  # 房间id 会在notice事件下返回
    message = data['message']
    if check_room_id(online_user_sid[flask.request.sid]['id'], room_id):  # 检查房间名是否合法
        Message.add_message_to_db(user_id=online_user_sid[flask.request.sid]['id'], body=message, room_id=room_id)
        emit('private', {
            'message': message,
            "user_id": online_user_sid[flask.request.sid]['id'],
            "user_name": online_user_sid[flask.request.sid]['name'],
            'room_id': room_id},
             room=room_id)  # 私有频道


@socketio.on('create')  # 请求创建一个私聊房间
def create_room(id):  # 请求私聊的用户id
    sid = flask.request.sid  # 不在已登录用户列表就断开连接
    name = User.query.get(id).name  # 用户必须存在
    if sid in online_user_sid and name is not None:
        if str(online_user_sid[sid]['id']) != str(id):  # 不是和自己创建房间
            room_id = str(id) + "$" + str(online_user_sid[sid]['id']) if int(id) < int(
                online_user_sid[sid]['id']) else str(online_user_sid[sid]['id']) + "$" + str(
                id)  # 创建房间的话 房间名由两个id组成 使用$分割 小的id在前大的在后
            Room.add_room_to_db(room_id=room_id)  # 不存在就加入数据库 否则不加入
            join_room(sid=sid, room=room_id)  #
            join_room(sid=online_user_id[id], room=room_id)
            emit('notice', {
                'User1': online_user_sid[online_user_id[id]]['name'],
                'User2': online_user_sid[flask.request.sid]['name'],
                'RoomID': room_id,
            }, room_id)

    else:  # 没登录 踢出
        disconnect()
