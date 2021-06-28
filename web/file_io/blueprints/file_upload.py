from flask import Blueprint, request
from web.extensions import make_json_response, login_check
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'py', 'm', 'md', 'mp4','doc','docx'}  # 允许上传的文件类型

file_io_bp = Blueprint('file_upload', __name__, url_prefix='/file')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@file_io_bp.route('/upload', methods=["POST"])
@login_check
def upload(id):
    file = request.files['file']
    filename = secure_filename(file.filename)
    if filename and allowed_file(filename):
        dir_path = os.getcwd() + os.sep+'file_upload'+os.sep+str(id)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        file.save(dir_path + os.sep + filename)
        return make_json_response(status=1, message="Succeed")
    else:
        return make_json_response(status=0, message="FileExtensionsError")
