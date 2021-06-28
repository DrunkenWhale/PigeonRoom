"""
个人主页
"""

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from web.extensions import db, make_json_response, token_return, login_check
from web.model import User

auth_home_bp = Blueprint('home', __name__, url_prefix='/auth')


@auth_home_bp.route('/home', methods=["GET"])
@login_check  # 通过token检查并且该用户存在
def home(id):
    user = User.query.get(id)
    if user is None:
        return make_json_response(
            status=0,
            message="UserUnExist",
            data=None,
        )
    else:
        re = {"id": user.id, "name": user.name, "phone": user.phone, "sex": user.sex,
              "email": user.email, "birth": user.birth,
              "note": [{"body": i.body, "time": i.time} for i in user.user_note]}
        return make_json_response(status=1, message="Succeed", data=re)
