from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from web.extensions import db, make_json_response, token_return
from web.model import User

auth_login_bp = Blueprint('login', __name__, url_prefix='/auth')


# 只有这一个接口可以传回token 请认准！ 带着token畅通无阻哟！
@auth_login_bp.route('/login', methods=["POST"])
def login():
    user_id = request.form.get("user_id")
    password = request.form.get("password")
    user1 = User.query.get(int(user_id))
    if user1 is None or check_password_hash(pwhash=user1.password, password=password) == False:
        return make_json_response(status=0, message='PasswordWrong', data={})
    else:
        token = token_return(user1.id)
        name = user1.name
        response = jsonify({
            'status': 1,
            'message': "Succeed",
            'data': {},
            "user_name": name,
            "token": str(token)[2:-1],  # 把b和''去掉
        })
        return response
