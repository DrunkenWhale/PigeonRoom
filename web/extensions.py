from flask_sqlalchemy import SQLAlchemy
from flask import jsonify, request, Response
from datetime import datetime, timedelta
import jwt
from flask_socketio import SocketIO, disconnect

db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins='*')


# 采用refresh_token  即过期时间短 需要延时时重新发送进行判断就可返回新的token
# 算了 好像得全部重写一遍  下次一定
def make_json_response(
        status=0,
        message=None,
        data=None
):
    response = jsonify({
        "status": status,
        "message": message,
        "data": data,
    })
    response.headers.add('Access-Control-Allow-Origin', "*")
    response.headers.add('Access-Control-Allow-Methods', "GET, POST, OPTIONS")
    response.headers.add('Access-Control-Allow-Headers', "*")
    return response


def login_check(func):                     # token放在请求头中
    def wrapper(*args, **kwargs):
        token = request.headers.get('token')
        try:
            login_msg = jwt.decode(token, key="priority_queue", algorithms="HS256")
            login_status = bool(login_msg.get('login_status', None))  # 传入bool值
            login_user_id = int(login_msg.get('login_user_id', None))  # 登录用户id 必须是全部由数字组成
            if login_status is True and login_user_id is not None:
                return func(login_user_id, *args, **kwargs)  # 返回函数返回的值
            else:
                raise
        except:
            return make_json_response(status=0, message="NoLogin", data={})

    wrapper.__name__ = func.__name__  # 装饰器联用会导致名称冲突 函数名都变为wrapper 会报overwrite的错误 需要手动修改函数名
    return wrapper


def token_return(user_id):
    payload = {
        "exp": datetime.utcnow() + timedelta(days=7),
        "login_user_id": user_id,
        "login_status": True,  # jwt的那几个标准键值对还要再看看
    }
    msg = jwt.encode(payload=payload, key="priority_queue", algorithm="HS256")
    return msg
