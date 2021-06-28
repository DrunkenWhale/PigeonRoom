from flask import Blueprint, request, send_file
from web.extensions import login_check, make_json_response
from werkzeug.utils import secure_filename
import jwt
import os

AVATAR_ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', "webp"}

auth_avatar_bp = Blueprint('avatar', __name__, url_prefix='/auth')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in AVATAR_ALLOWED_EXTENSIONS


@auth_avatar_bp.route('/avatar', methods=["POST"])   # 头像文件上传
@login_check
def avatar_upload(id):
    file = request.files['file']
    filename = secure_filename(file.filename)
    if filename and allowed_file(filename):
        dir_path = os.getcwd() + os.sep + 'file_upload' + os.sep + "avatar"
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        file.save(dir_path + os.sep + str(id) + '.png')
        return make_json_response(status=1, message="Succeed")
    else:
        return make_json_response(status=0, message="FileExtensionsError")


@auth_avatar_bp.route('/avatar', methods=["GET"])   # 头像文件获取 主要是靠缓存
def avatar_download():                          # 这里比较特别 token要放在params里  别问 问就是方便
    token = request.args.get('token', None)
    try:
        login_msg = jwt.decode(token, key="priority_queue", algorithms="HS256")
        login_status = bool(login_msg.get('login_status', None))  # 传入bool值
        login_user_id = int(login_msg.get('login_user_id', None))  # 登录用户id 必须是全部由数字组成
        filename = str(request.args.get('username')) + '.png'  # 登陆的用户才能获取头像
        if login_status is True and login_user_id is not None:
            dir_path = os.getcwd() + os.sep + 'file_upload' + os.sep + 'avatar'
            if os.path.exists(dir_path + os.sep + filename):
                return send_file(filename_or_fp=dir_path + os.sep + filename, attachment_filename=filename,
                                 as_attachment=True)
            else:
                return send_file(filename_or_fp=dir_path + os.sep + "default.png", attachment_filename=filename,
                                 as_attachment=True)
        return make_json_response(status=0, message='FileUnExist', data=None)
    except:
        return "<script>window.alert('你没有登录哦 白嫖怪~');window.location.href='javascript:history.go(-1)';</script>"
