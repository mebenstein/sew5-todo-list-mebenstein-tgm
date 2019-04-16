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
    locked = db.Column(db.Boolean,default=False)
    title = db.Column(db.String(80),nullable=False)
    parent_id = db.Column(db.Integer,db.ForeignKey('todos.id'))
    children = db.relationship('ToDoObject', backref=db.backref('parent',remote_side=[id]))

    def __init__(self,title,parent=None):
        self.title = title
        self.parent_id = parent

    def setLocked(self,state):
        self.locked = state

class ToDoEncoder(json.JSONEncoder):
        def default(self, o):
            return {"id":o.id,"title":o.title,"locked":o.locked,'children':o.children}

db.create_all()
db.session.commit()

@app.route("/add")
def addTodo():
    obj = json.loads(request.data)
    
    todo = ToDoObject(obj["title"],obj.get("parent"))

    db.session.add(todo)
    db.session.commit()

    return (str(todo.id),200)

@app.route("/get")
def getTodo():
    return (json.dumps(
        ToDoObject.query
            .filter(ToDoObject.parent_id == None)
            .all()
            ,cls=ToDoEncoder)
        ,200)

@app.route("/set/<int:id>")
def setTodo(id=None):
    obj = json.loads(request.data)
    todo = ToDoObject.query.get(id)
    
    if todo == None:
        return ("Todo does not exist",404)

    if not todo.locked:
        for key,val in obj.items():
            setattr(todo,key,val)
    elif obj.get("locked") != None:
        todo.locked = obj["locked"]
    else:
        return ("Cant write on locked todo",403)

    db.session.commit()

    return (json.dumps(todo,cls=ToDoEncoder),200)


@app.route("/del/<int:id>")
def delTodo(id=None):
    todo = ToDoObject.query.get(id)

    if todo.locked:
        return ("Cant delete locked todo",403)

    db.session.delete(todo)
    db.session.commit()

    return ("deleted "+str(id),200)

if __name__ == "__main__":
    app.run(port=9000)