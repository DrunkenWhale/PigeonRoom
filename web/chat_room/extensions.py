from web.model import User, Message, db
from flask_socketio import disconnect
import jwt
import flask


def check_user_token(data):
    try:
        token = data['token']
        login_msg = jwt.decode(token, key="priority_queue", algorithms="HS256")
        login_status = bool(login_msg.get('login_status', None))  # 传入bool值
        login_user_id = int(login_msg.get('login_user_id', None))  # 登录用户id 必须是全部由数字组成
        user = User.query.get(login_user_id)
        if login_status is True and login_user_id is not None and user is not None:
            return {'id': login_user_id, 'name': user.name}
        else:
            raise
    except:
        disconnect()
        return None


def check_room_id(id, room_id):  # 判断用户是否在房间内及房间是否合法
    try:
        if "$" in room_id:
            member = room_id.split("$")
            if str(id) in member:
                return True
            else:
                raise
        else:
            raise
    except:
        return False

#
# def check_login_chat(data):     # 前端发送的消息使用对象 其中token属性用于鉴权  话说这里用session不是好多了
#     try:
#         token = data["token"]
#         message = data["message"]
#         login_msg = jwt.decode(token, key="priority_queue", algorithms="HS256")
#         login_status = bool(login_msg.get('login_status', None))  # 传入bool值
#         login_user_id = int(login_msg.get('login_user_id', None))  # 登录用户id 必须是全部由数字组成
#         if login_status is True and login_user_id is not None:
#             if login_user_id not in user_online_dict:  # 未在已登录用户之列
#                 user = User.query.get(login_user_id)
#                 username = user.name
#                 user_online_dict[login_user_id] = username
#             else:
#                 username = user_online_dict[login_user_id]
#             db.session.add(Message(user=login_user_id, body=message))
#             try:
#                 db.session.commit()
#             except:
#                 pass
#             return {
#                 "id": login_user_id,
#                 "username": username,
#                 "message": message
#             }
#         else:
#             raise
#     except:
#         disconnect()
