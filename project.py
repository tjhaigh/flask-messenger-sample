from eventlet import wsgi
import eventlet
from datetime import datetime
from flask import Flask, session, request, render_template, redirect, url_for, jsonify 
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret'
socketio = SocketIO(app)

#keep count of messages sent
msgcount = 0

@app.route('/')
def home():
    if 'name' in session:
        return redirect(url_for('chat'))
    else:
        return redirect(url_for('pick_name'))

@app.route('/pickname', methods=['GET', 'POST'])
def pick_name():
    if request.method == 'POST':
        session['name'] = request.form['name']
        return redirect(url_for('chat'))
    return render_template('pick_name.html')

@app.route('/chat')
def chat():
    if 'name' in session:
        return render_template('chat.html')
    else:
        return redirect(url_for('pick_name'))

@app.route('/count')
def count():
    return render_template('count.html', msgcount=msgcount)

@socketio.on('message')
def handle_message(message):
    global msgcount
    msgcount += 1
    timestamp = datetime.strftime(datetime.now(), '%H:%M:%S')
    message = session['name'] + ': ' + message
    data = { 'message': message, 'timestamp': timestamp } 
    emit('message', data, broadcast=True)

@socketio.on('connected')
def handle_connection(message):
    timestamp = datetime.strftime(datetime.now(), '%H:%M:%S')
    data = { 'message': session['name'] + ' has connected.', 'timestamp': timestamp }
    emit('message', data, broadcast=True)


if __name__ == "__main__":
    wsgi.server(eventlet.listen(('172.19.50.221',8000)),app)
    #socketio.run(app)
    #app.run()

