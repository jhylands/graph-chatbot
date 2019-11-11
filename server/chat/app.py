from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
'''
Main app
sources:
For the original server code
https://codeburst.io/building-your-first-chat-application-using-flask-in-7-minutes-f98de4adfa5d

'''

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://timepcou_chatter:thefluffycatinmyhouse@31.220.21.116/timepcou_chat'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
socketio = SocketIO(app)
db = SQLAlchemy()
db.init_app(app)

class Message(db.Model):
    __tablename__ = "message"
    id = db.Column("id", db.Integer, autoincrement=True, primary_key=True)
    message = db.Column("message", db.Text)

def handle_message(message):
    if type(message) == type({}) and "message" in message:
        message = Message(message = message["message"])
        db.session.add(message)
        db.session.commit()
        

@app.route('/')
def sessions():
    messages = Message.query.all()
    return render_template('session.html', messages=messages)

@app.route('/send', methods=['POST'])
def con_test():
    content = request.json
    handle_message(content)
    return jsonify({'resp':True})

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    handle_message(json)
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", debug=True)
