import os


class Config(object):
    FLASK_APP = "web"
    SECRET_KEY = "Websocket+Vue_is_so_nice"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///" + os.path.join(
        os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'data.db'))
    MAX_CONTENT_LENGTH = 64 * 1024 * 1024    # 最大允许上传64 MB
