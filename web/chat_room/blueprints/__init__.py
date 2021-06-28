"""
这个聊天室的主体在socket.py下
还有一些ajax的就放在这里啦
"""

from .get_online_user import get_online_user_bp
from .get_chat_message import get_chat_message_bp
from .get_all_rooms import get_all_rooms_bp


def chat_room_register_blueprints(app):
    app.register_blueprint(get_online_user_bp)
    app.register_blueprint(get_chat_message_bp)
    app.register_blueprint(get_all_rooms_bp)
