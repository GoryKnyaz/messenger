from datetime import datetime
from flask import Flask, render_template, request
import json

my_db_name = 'db.json'


def load_info(db_name):
    with open(db_name, 'r') as db_file:
        db_info = json.load(db_file)
    return db_info['messages']


def save_info(db_name, db_info):
    data = {"messages": db_info}
    with open(db_name, 'w') as json_file:
        json.dump(data, json_file)


app = Flask(__name__)
all_messages = load_info(my_db_name)


@app.route('/')
def index_page():
    return render_template('authorization.html')


@app.route('/chat')
def display_chat():
    return render_template('form.html')

@app.route('/images/back_ground.jpg')
def image_background():
    return render_template('images/back_ground.html')


@app.route('/get_messages')
def get_message():
    return {"messages": all_messages}

@app.route('/send_message')
def send_message():
    sender = request.args['name']
    text = request.args['text']
    time = datetime.now().strftime("%H:%M")
    text_info = \
        {
            "text": text,
            "sender": sender,
            "time": time
        }
    all_messages.append(text_info)
    save_info(my_db_name, all_messages)
    return {"messages": all_messages}


app.run(host='0.0.0.0', port=4567)
app.config['UPLOAD_FOLDER'] = '/images'