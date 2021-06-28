from flask import Blueprint
from ..socket import online_user_sid
from web.model import User
from web.extensions import login_check, make_json_response
from flask_socketio import rooms

get_all_rooms_bp = Blueprint('get_all_rooms', __name__, url_prefix='/chat')


@get_all_rooms_bp.route('/room', methods=['GET'])
@login_check
def _get_online_user(id):
    user = User.query.get(id)
    if user.admin >= 7:  # 管理员权限
        re = [{online_user_sid[sid]['id']: rooms(sid=sid, namespace='/')} for sid in online_user_sid.keys()]
        return make_json_response(status=1, message='Succeed', data=re)
    else:
        return make_json_response(status=0, message='PermissionDenied', data=None)
