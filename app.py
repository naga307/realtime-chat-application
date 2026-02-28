from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.secret_key = 'secretkey'
socketio = SocketIO(app)

users = {}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        users[username] = True
        return redirect(url_for('chat'))
    return render_template('login.html')

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html', username=session['username'])

@socketio.on('join')
def handle_join(data):
    room = data['room']
    join_room(room)
    emit('message', f"{data['user']} joined the room.", to=room)

@socketio.on('send_message')
def handle_message(data):
    room = data['room']
    message = data['message']
    user = data['user']
    emit('message', f"{user}: {message}", to=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)
