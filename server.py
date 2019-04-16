from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class ToDoObject(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    locked = False
    title = db.Column(db.String(80),nullable=False)
    parent_id = db.Column(db.Integer,db.ForeignKey('todos.id'))
    children = db.relationship('ToDoObject', backref=db.backref('parent',remote_side=[id]))

    def __init__(self,title,parent=None):
        self.title = title
        self.parent_id = parent

    def setLocked(self,state):
        self.locked = state

db.create_all()
db.session.commit()

@app.route("/add")
def addTodo():
    obj = json.loads(request.data)
    
    todo = ToDoObject(obj["title"],obj.get("parent"))

    db.session.add(todo)
    db.session.commit()

    return (str(todo.id),0)

if __name__ == "__main__":
    app.run(port=9000)