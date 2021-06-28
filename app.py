from web import *

if __name__ == '__main__':
    app = create_app(__name__)
    socketio.run(app,port=2333,host="0.0.0.0")
