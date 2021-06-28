from web.file_io.blueprints.file_delete import file_delete_bp
from web.file_io.blueprints.file_upload import file_io_bp
from web.file_io.blueprints.file_list import file_list_bp
from web.file_io.blueprints.file_download import file_download_bp


def file_io_register_blueprints(app):
    app.register_blueprint(file_io_bp)  # 文件读写 算是一个工具站？
    app.register_blueprint(file_list_bp)  # 文件列表
    app.register_blueprint(file_download_bp)  # 文件下载
    app.register_blueprint(file_delete_bp)  # 文件删除