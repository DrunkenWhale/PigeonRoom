from flask import Blueprint, request
from web.extensions import make_json_response
from web.admin.extensions import markdown_sqlite
from web.model import User
import sqlite3
import os
import jwt

get_data_from_db_bp = Blueprint("get_data_from_db", __name__, url_prefix="/admin")


@get_data_from_db_bp.route("/data", methods=["GET"])
def _get_data_from_db():
    if 1:
        token = request.headers.get("token")
        login_msg = jwt.decode(token, key="priority_queue", algorithms="HS256")
        login_status = bool(login_msg.get('login_status', None))  # 传入bool值
        login_user_id = int(login_msg.get('login_user_id', None))  # 登录用户id 必须是全部由数字组成
        if login_status is True and login_user_id is not None:
            user = User.query.get(login_user_id)
            if user is not None:
                if type(user.admin) == int and user.admin >= 7:  # 究极管理员好吧
                    database = request.args.get("db", "data.db")
                    order = request.args.get("order", "SELECT * FROM MESSAGE")
                    path = os.getcwd() + os.sep
                    markdown = markdown_sqlite(path=path, database=database, order=order)
                    res = markdown.content
                    return make_json_response(status=1,message="Succeed",data=res)  # 这里考虑用vue 的html插值来操作
                else:
                    return make_json_response(status=0, message="PermissionDenied", data=None)
        else:
            raise
    #except:
      #  return make_json_response(status=0, message="OrderWrong", data=None)
