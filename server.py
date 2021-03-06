from flask import Flask,request,render_template, g
from flask_sqlalchemy import SQLAlchemy
import json
from flask_cors import CORS
from flask_httpauth import HTTPTokenAuth

app = Flask(__name__,static_folder="./frontend/dist/static",template_folder="./frontend/dist")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
auth = HTTPTokenAuth(scheme='Token')
CORS(app)

tokens = {
    "1234": "web",
    "5678": "testing"
}

class ToDoObject(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    locked = db.Column(db.Boolean,default=False)
    title = db.Column(db.String(80),nullable=False)
    parent_id = db.Column(db.Integer,db.ForeignKey('todos.id'))
    children = db.relationship('ToDoObject',cascade="all,delete", backref=db.backref('parent',remote_side=[id]))

    def __init__(self,title,parent=None):
        self.title = title
        self.parent_id = parent

class ToDoEncoder(json.JSONEncoder):
        def default(self, o):
            return {"id":o.id,"title":o.title,"locked":o.locked,'children':o.children}

db.create_all()
db.session.commit()

def parent_locked(todo):
    parent_lock = False
    if todo.parent_id != None:
        parent_lock = ToDoObject.query.get(todo.parent_id).locked

    return parent_lock

@auth.verify_token
def verify_token(token):
    if token in tokens:
        g.current_user = tokens[token]
        return True
    return False

@app.route('/')
def index():
   return render_template("index.html")

@app.route("/add",methods=["POST"])
@auth.login_required
def addTodo():
    obj = json.loads(request.data)

    if obj.get("title") == None:
        return ("Title required",403)
    
    todo = ToDoObject(obj["title"],obj.get("parent"))

    db.session.add(todo)
    db.session.commit()

    return (str(todo.id),200)

@app.route("/get",methods=["GET"])
@auth.login_required
def getTodo():
    return (json.dumps(
        ToDoObject.query
            .filter(ToDoObject.parent_id == None)
            .all()
            ,cls=ToDoEncoder)
        ,200)

@app.route("/set/<int:id>",methods=["POST"])
@auth.login_required
def setTodo(id=None):
    obj = json.loads(request.data)
    todo = ToDoObject.query.get(id)
    
    if todo == None:
        return ("Todo does not exist",404)


    if not todo.locked and not parent_locked(todo):
        for key,val in obj.items():
            setattr(todo,key,val)
    elif obj.get("locked") != None:
        todo.locked = obj["locked"]
    else:
        return ("Cant write on locked todo",403)

    db.session.commit()

    return (json.dumps(todo,cls=ToDoEncoder),200)


@app.route("/del/<int:id>",methods=["POST"])
@auth.login_required
def delTodo(id=None):
    todo = ToDoObject.query.get(id)

    if todo.locked and not parent_locked(todo):
        return ("Cant delete locked todo",403)

    db.session.delete(todo)
    db.session.commit()

    return ("deleted "+str(id),200)

if __name__ == "__main__":
    app.run(port=9000)