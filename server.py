from threading import Thread, Lock

class ToDoObject():
    lock = Lock()
    id = 0
    locked = False
    title = ""

    def __init__(self,title):
        self.title = title

        with lock:
            self.id = ToDoObject.id
            ToDoObject.id += 1

    def setLocked(self,state):
        self.locked = state

class ToDoItem(ToDoObject):
    def __init__(self,title):
        ToDoObject.__init__(title)

class ToDoList(ToDoObject):    
    tasks = []

    def __init__(self,title,tasks = []):
        ToDoObject.__init__(title)
        self.tasks = tasks

    def addTask(self,task):
        self.tasks.append(task)


    