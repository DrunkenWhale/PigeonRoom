from flask import Blueprint, request
from web.model import User
from werkzeug.security import generate_password_hash
from web.extensions import db, make_json_response

auth_register_bp = Blueprint('register', __name__, url_prefix='/auth')


@auth_register_bp.route("/register", methods=["POST"])
def register():
    user_id = request.form.get("user_id")
    password = request.form.get("password")
    username = request.form.get("user_name")
    user_phone = request.form.get("phone")
    user_sex = request.form.get("sex")
    if user_sex == "1":   # 直接对字符串转化总会得到True 所以我拒绝
        user_sex = True
    else:
        user_sex = False
    user_email = request.form.get("email")
    user_birth = request.form.get("birth")
    user1 = User.query.get(user_id)
    if user1 is None:
        if username is None or password is None or user_id is None:
            return make_json_response(status=0, message='WrongInput', data={})
        else:
            password = generate_password_hash(password)
            user1 = User(name=username, id=user_id, password=password, phone=user_phone, sex=user_sex, birth=user_birth,
                         email=user_email)
            db.session.add(user1)
            db.session.commit()
            return make_json_response(status=1, message='Succeed', data={})
    else:
        return make_json_response(status=0, message='UserExist', data={})
