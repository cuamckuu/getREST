import sys
sys.path.append('..')

from fastapi.testclient import TestClient

from main import app

# Not very good tests, but better than nothing for now
client = TestClient(app)


def test_create_api():
    r = client.post('/api')
    assert r.status_code == 200
    res_json = r.json()
    assert 'api_token' in res_json

    return res_json['api_token']


def test_create_object():
    api_key = test_create_api()

    # Empty collection
    r = client.get(f'/api/{api_key}/cats')
    assert r.status_code == 200
    assert r.json() == []

    # Create object
    obj = {'name': 'Felix', 'color': 'black'}
    r = client.post(f'/api/{api_key}/cats', json=obj)
    res_json = r.json()
    assert r.status_code == 200
    assert '_id' in res_json

    # Non-empty collection
    r = client.get(f'/api/{api_key}/cats')
    assert r.status_code == 200
    assert r.json() == [res_json]


def test_update_object():
    api_key = test_create_api()

    obj = {'name': 'Felix', 'color': 'black'}
    obj2 = {'name': 'Tom'}
    patch = {'color': 'gray'}

    # Create object
    r = client.post(f'/api/{api_key}/cats', json=obj)
    res_json = r.json()

    # Replace element
    r = client.put(f'/api/{api_key}/cats/{res_json["_id"]}', json=obj2)
    res_json2 = r.json()
    new_id = res_json2.pop('_id')
    assert new_id == res_json['_id']
    assert r.status_code == 200
    assert res_json2 == obj2

    # Update element
    r = client.patch(f'/api/{api_key}/cats/{res_json["_id"]}', json=patch)
    res_json3 = r.json()
    new_id = res_json3.pop('_id')
    assert new_id == res_json['_id']
    assert r.status_code == 200
    assert res_json3 == {**obj2, **patch}


def test_delete_object():
    api_key = test_create_api()

    # Create object
    obj = {'name': 'Felix', 'color': 'black'}
    r = client.post(f'/api/{api_key}/cats', json=obj)
    res_json = r.json()
    assert r.status_code == 200
    assert '_id' in res_json

    # Non-empty collection
    r = client.get(f'/api/{api_key}/cats')
    assert r.status_code == 200
    assert r.json() == [res_json]

    # Delete element
    r = client.delete(f'/api/{api_key}/cats/{res_json["_id"]}')
    assert r.status_code == 200
    assert r.json() == True

    # Empty collection
    r = client.get(f'/api/{api_key}/cats')
    assert r.status_code == 200
    assert r.json() == []
