from web.auth.blueprints import auth_register_blueprints
from web.file_io.blueprints import file_io_register_blueprints
from web.static_html.blueprints import static_html_register_blueprints
from web.note.blueprints import note_register_blueprints
from web.chat_room.socket import handle_message
from web.chat_room.blueprints import chat_room_register_blueprints
from web.admin import admin_register_blueprints
from web.extensions import db, socketio
from web.config import Config
from web.model import Room
from flask import Flask, send_from_directory
from flask_cors import CORS
import os


def create_app(name=__name__):
    app = Flask(name)
    app.config.from_object(Config)
    register_extensions(app)
    register_blueprints(app)
    CORS(app, origins='*')   # 允许跨域
    return app


def register_blueprints(app):
    auth_register_blueprints(app)  # 总的注册函数
    file_io_register_blueprints(app)
    static_html_register_blueprints(app)
    note_register_blueprints(app)
    chat_room_register_blueprints(app)
    admin_register_blueprints(app)


def register_extensions(app):
    socketio.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
        Room.add_room_to_db("public")  # 创建初始房间
