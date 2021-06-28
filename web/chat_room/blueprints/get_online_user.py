from flask import Blueprint
from ..socket import online_user_sid
from web.model import User
from web.extensions import login_check, make_json_response

get_online_user_bp = Blueprint('get_online_user', __name__, url_prefix='/chat')


@get_online_user_bp.route('/user', methods=['GET'])
@login_check
def _get_online_user(id):
    user = User.query.get(id)
    if user.admin >= 7:  # 管理员权限
        re = [usr for usr in online_user_sid.values()]
        return make_json_response(status=1, message='Succeed', data=re)
    else:
        return make_json_response(status=0, message='PermissionDenied',data=None)