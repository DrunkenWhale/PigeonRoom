from flask import Blueprint, request
from ..socket import online_user_sid, online_user_id
from web.model import User, Message, Room
from web.extensions import login_check, make_json_response
from web.chat_room.extensions import check_room_id

get_chat_message_bp = Blueprint('get_chat_message', __name__, url_prefix='/chat')


@get_chat_message_bp.route('/message', methods=['GET'])
@login_check
def _get_chat_message(id):
    user = User.query.get(id)
    room_id = request.args.get('room', None)  # 未得到默认视为查询所有房间
    if type(user.admin) == int and user.admin >= 7:  # 管理员开放所有操作
        if room_id is None:
            # 管理员权限获取所有消息记录 写的比较繁琐是为了每个房间的数据都一起返回
            temp = set([room for room in Room.query.all()])
            re = [{
                room.id:  # 保证房间号不会重复
                    [
                        {"user_id": message.user_id, "message": message.body, "time": message.time}
                        for message in room.messages
                    ]
            } for room in temp]
            return make_json_response(status=1, message='Succeed', data=re)
        else:
            temp = Room.query.get(room_id)
            if temp is not None:
                re = {
                    temp.id: [
                        {
                            "user_id": message.user_id,
                            "user_name": User.query.get(message.user_id).name,
                            "message": message.body,
                            "time": message.time
                        }
                        for message in temp.messages
                    ]
                }
                return make_json_response(status=1, message='Succeed', data=re)
            else:
                return make_json_response(status=1, message="Succeed", data=[])
    else:
        if room_id is None:
            return make_json_response(status=0, message='PermissionDenied', data=None)
        else:
            if check_room_id(id, room_id) or room_id == "public":  # 阳间的格式 public的记录谁都可以看
                room = Room.query.get(room_id)
                re = {
                    room_id:  # 保证房间号不会重复
                        [
                            {
                                "user_id": message.user_id,
                                "user_name": User.query.get(message.user_id).name,
                                "message": message.body,
                                "time": message.time,
                            }
                            for message in room.messages
                        ]
                }
                re[room_id].reverse()
                return make_json_response(status=1, message='Succeed', data=re)
            else:
                return make_json_response(status=0, message='PermissionDenied', data=None)
