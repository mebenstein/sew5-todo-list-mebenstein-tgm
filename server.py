from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from threading import Lock

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://todo.db'
db = SQLAlchemy(app)

class ToDoObject(db.Model):
    lock = Lock()
    id = db.Column(db.Integer, primary_key=True)
    locked = False
    title = db.Column(db.String(80))
    parent = db.Column(db.Integer,db.ForeignKey('todoobject.id'))

    def __init__(self,title):
        self.title = title

        with lock:
            self.id = ToDoObject.id
            ToDoObject.id += 1

    def setLocked(self,state):
        self.locked = state



