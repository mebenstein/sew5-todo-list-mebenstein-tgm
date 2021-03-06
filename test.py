import os
import tempfile
import pytest
from server import app,db
import json

@pytest.fixture(scope="session", autouse=True)
def init():
    db.drop_all()
    db.create_all()

@pytest.fixture
def credentials():
    return {"Authorization":"Token 5678"}

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_web(client,credentials):
    rv = client.get('/')
    assert rv.status_code == 200

def test_get_none_success(client,credentials):
    rv = client.get('/get',headers=credentials)
    assert len(json.loads(rv.data)) == 0
    assert rv.status_code == 200
    
def test_credentials_fail(client,credentials):
    rv = client.get('/get')
    assert rv.status_code == 401

def test_add_one_success(client,credentials):
    rv = client.post('/add',data=json.dumps({"title":"do SEW"}), content_type='application/json',headers=credentials)

    assert int(rv.data) == 1
    assert rv.status_code == 200


def test_get_one_success(client,credentials):
    rv = client.get('/get',headers=credentials)
    obj = json.loads(rv.data)

    assert len(obj) == 1
    assert obj[0]["id"] == 1
    assert obj[0]["title"] == "do SEW"
    assert obj[0]["locked"] == False
    assert len(obj[0]["children"]) == 0
    assert rv.status_code == 200

def test_add_one_fail_no_title(client,credentials):
    rv = client.post('/add',data=json.dumps({}),headers=credentials)

    assert rv.data.decode() == "Title required"
    assert rv.status_code == 403

def test_add_child_success(client,credentials):
    rv = client.post('/add',data=json.dumps({"title":"do Todo","parent":1}),headers=credentials)

    assert int(rv.data) == 2
    assert rv.status_code == 200

def test_get_child_success(client,credentials):
    rv = client.get('/get',headers=credentials)
    obj = json.loads(rv.data)
    cldr = obj[0]["children"]

    assert len(obj) == 1
    assert obj[0]["id"] == 1
    assert obj[0]["title"] == "do SEW"
    assert len(cldr) == 1
    assert cldr[0]["id"] == 2
    assert cldr[0]["title"] == "do Todo"
    assert cldr[0]["locked"] == False
    assert rv.status_code == 200

def test_update_success(client,credentials):
    rv = client.post('/set/2',data=json.dumps({"title":"do Threads"}),headers=credentials)
    obj = json.loads(rv.data)

    assert obj["locked"] == False
    assert obj["title"] == "do Threads"
    assert rv.status_code == 200

def test_update_lock_success(client,credentials):
    rv = client.post('/set/2',data=json.dumps({"locked":True}),headers=credentials)
    obj = json.loads(rv.data)

    assert obj["locked"] == True
    assert rv.status_code == 200

def test_update_on_lock_fail(client,credentials):
    rv = client.post('/set/2',data=json.dumps({"title":"do JS"}),headers=credentials)

    assert rv.data.decode() == "Cant write on locked todo"
    assert rv.status_code == 403

    rv = client.get('/get',headers=credentials)
    obj = json.loads(rv.data)[0]["children"][0]

    assert obj["locked"] == True
    assert obj["title"] == "do Threads"
    assert rv.status_code == 200

def test_delete_on_lock_fail(client,credentials):
    rv = client.post('/del/2',headers=credentials)

    assert rv.data.decode() == "Cant delete locked todo"
    assert rv.status_code == 403

def test_update_nolock_success(client,credentials):
    rv = client.post('/set/2',data=json.dumps({"locked":False}),headers=credentials)
    obj = json.loads(rv.data)

    assert obj["locked"] == False
    assert rv.status_code == 200

def test_delete_success(client,credentials):
    rv = client.post('/del/2',headers=credentials)

    assert rv.data.decode() == "deleted 2"
    assert rv.status_code == 200

def test_delete_success_parent(client,credentials):
    rv = client.post('/del/1',headers=credentials)

    assert rv.data.decode() == "deleted 1"
    assert rv.status_code == 200

def test_update_nonexisting_fail(client,credentials):
    rv = client.post('/set/2',data=json.dumps({"locked":False}),headers=credentials)

    assert rv.data.decode() == "Todo does not exist"
    assert rv.status_code == 404

def test_parent_delete_child_delete_success(client,credentials):
    rv = client.post('/add',data=json.dumps({"title":"do Vue"}), content_type='application/json',headers=credentials)

    assert int(rv.data) == 1
    assert rv.status_code == 200

    rv = client.post('/add',data=json.dumps({"title":"do frontend","parent":2}),headers=credentials)

    assert int(rv.data) == 2
    assert rv.status_code == 200

    rv = client.post('/del/1',headers=credentials)

    assert rv.data.decode() == "deleted 1"
    assert rv.status_code == 200

    rv = client.get('/get',headers=credentials)
    obj = json.loads(rv.data)
    assert len(obj) == 0
    assert rv.status_code == 200

def test_parent_lock_child_lock_success(client,credentials):
    rv = client.post('/add',data=json.dumps({"title":"do Testing"}),headers=credentials)

    assert int(rv.data) == 3
    assert rv.status_code == 200

    rv = client.post('/add',data=json.dumps({"title":"do unittest","parent":3}),headers=credentials)

    assert int(rv.data) == 4
    assert rv.status_code == 200

    rv = client.post('/set/3',data=json.dumps({"locked":True}),headers=credentials)
    obj = json.loads(rv.data)

    assert obj["locked"] == True
    assert rv.status_code == 200

    rv = client.post('/set/4',data=json.dumps({"title":"do JS"}),headers=credentials)
    
    assert rv.data.decode() == "Cant write on locked todo"
    assert rv.status_code == 403

    rv = client.get('/get',headers=credentials)
    obj = json.loads(rv.data)
    cldr = obj[0]["children"]

    assert len(obj) == 1
    assert obj[0]["id"] == 3
    assert obj[0]["title"] == "do Testing"
    assert obj[0]["locked"] == True
    assert len(cldr) == 1
    assert cldr[0]["id"] == 4
    assert cldr[0]["title"] == "do unittest"
    assert cldr[0]["locked"] == False
    assert rv.status_code == 200