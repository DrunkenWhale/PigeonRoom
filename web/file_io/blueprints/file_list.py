from flask import Blueprint
from web.extensions import make_json_response, login_check
import os

file_list_bp = Blueprint('file_list', __name__, url_prefix='/file')


@file_list_bp.route('/list', methods=["GET"])
@login_check
def file_list(id):
    dir_path = os.getcwd() + os.sep + 'file_upload' + os.sep + str(id)
    if os.path.exists(dir_path):  # 文件夹存在 查询文件
        re = os.listdir(dir_path)
        return make_json_response(status=1, message='Succeed', data=re)
    else:
        return make_json_response(status=0, message="NoFile", data=None)  # 文件夹不存在 未上传过文件
