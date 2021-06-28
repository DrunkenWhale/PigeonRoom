# from flask import Flask
# from chat_room.extensions import socketio
# from chat_room.config import Config
# from chat_room.socket import handle_message
#
#
# def create_app(name=__name__):
#     app = Flask(name)
#     app.config.from_object(Config)
#     register_extensions(app)
#     return app
#
#
# def register_extensions(app: Flask):
#     socketio.init_app(app=app)
"""
前排提醒 这里应该是最混乱的地方了 标准不一 为您带来困扰非常抱歉
在前端使用emit发送消息时 需要使用token$message的格式
程序会自动分割token并检查是否有效
message为你上传的信息
不带token所有的都不能用 会直接断开连接
"""

