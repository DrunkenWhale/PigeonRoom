from web.extensions import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    password = db.Column(db.String(128))
    phone = db.Column(db.Integer)
    sex = db.Column(db.Boolean)  # 男1女0 请勿打拳
    email = db.Column(db.String(128))
    birth = db.Column(db.String(80))
    age = db.Column(db.Integer)
    admin = db.Column(db.Integer, index=True)
    # >= 7即为管理员 别问我为什么 问就是我喜欢这个数字 我就是不用bool值

    # #######################全是关联表#############################

    user_note = db.relationship("Note")  # 关联留言板
    user_message = db.relationship("Message")  # 关联消息

    #######################################################
    def __init__(self, id, name, password, phone=None, sex=0, email=None, birth="1970-1-1"):
        self.id = id
        self.name = name
        self.password = password
        self.phone = phone
        self.sex = sex
        self.email = email
        self.birth = birth


class Message(db.Model):  # 聊天记录
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(128))
    time = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    room_id = db.Column(db.String(80), db.ForeignKey("room.id"))  # 房间 用于返回历史消息

    def __init__(self, user_id, body, room_id):
        self.user_id = user_id
        self.body = body
        self.time = datetime.now()
        self.room_id = room_id

    @staticmethod
    def add_message_to_db(user_id, body, room_id):
        db.session.add(Message(user_id=user_id, body=body, room_id=room_id))
        try:
            db.session.commit()
        except:
            pass


class Note(db.Model):  # 用户留言  有一说一 这个单词到底怎么说啊..我知道note不太对 但是词汇量不够啊喂
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)  # 留言内容
    time = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, body, user_id):
        self.body = body
        self.user_id = user_id
        self.time = datetime.now()

    @staticmethod
    def add(user_id, body):  # 最多三条留言 自动覆盖最早一条
        temp_note = Note(user_id=user_id, body=body)
        user_note_list = User.query.get(temp_note.user_id).user_note
        if 3 <= len(user_note_list):
            temp = user_note_list[0]  # 不能使用pop 一使用父类User就被gc吃掉了 会报错
            db.session.delete(temp)
        db.session.add(temp_note)
        try:
            db.session.commit()
            return True  # 测试完成后请使用一个try包起这块代码 因为sqlite单线程写入你懂得
        except:
            return False

    @staticmethod
    def get_all(user_id):
        return User.query.get(user_id).user_note


class Room(db.Model):
    id = db.Column(db.String(80), primary_key=True)  # 房间号 因为奇怪的原因用字符串格式存了 abab
    messages = db.relationship("Message")
    time = db.Column(db.DateTime)

    def __init__(self, room_id):
        self.id = room_id
        self.time = datetime.now()

    @staticmethod
    def add_room_to_db(room_id):
        if Room.query.get(room_id) is None:
            db.session.add(Room(room_id=room_id))
            try:
                db.session.commit()
            except:
                pass
            return True
        else:
            return False
