from socket import socket
from flask import Flask, request
from flask_socketio import SocketIO, emit
from flask_socketio import ConnectionRefusedError
from flask_socketio import Namespace

import datetime
import os
import pytz

from .model import db, Message

app = Flask(__name__)

user = os.environ.get("MARIADB_USER", "")
password = os.environ.get("MARIADB_PASSWORD", "")
host = os.environ.get("MARIADB_HOST", "")
database = os.environ.get("MARIADB_DATABASE", "")

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{user}:{password}@{host}/{database}"

db.init_app(app)
with app.app_context():
    db.create_all()

socketio = SocketIO(app, 
        cors_allowed_origins="*", 
        async_mode='gevent',
        logger=True, 
        engineio_logger=True)

class ChatNamespace(Namespace):
    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_get_messages(self):
        result = (db.session.query(Message)
            .order_by(Message.date.desc())
            .limit(100)
            .all())
        messages = []
        for current in result:
            date = current.date.astimezone(datetime.timezone.utc)
            print(f"From: {current.date} -> {date}")
            messages.append({
                "id": current.uuidString, 
                "date": date.isoformat(), 
                "username": current.username,
                "text": current.text
            })
        emit("prev_messages", messages)

    def on_message(self, uuidString, dateString, username, text):
        date = datetime.datetime.fromisoformat(dateString)
        date = date.astimezone(datetime.timezone.utc)
        message = Message(uuidString=uuidString, date=date, username=username, text=text)
        db.session.add(message)
        db.session.commit()
        messages = [{
            "id": uuidString, 
            "date": dateString, 
            "username": username, 
            "text": text
        }]
        emit("new_messages", messages, broadcast=True)

socketio.on_namespace(ChatNamespace("/chat"))


if __name__ == "__main__":
    socketio.run(app)