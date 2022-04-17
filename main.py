#!/usr/bin/env python3

import uuid

import fastapi
import uvicorn

from montydb import set_storage, MontyClient
from montydb.types.objectid import ObjectId

STORAGE_DIR = './db/'

set_storage(repository='./db/', storage='sqlite')
app = fastapi.FastAPI()
app.state.storage = MontyClient(STORAGE_DIR)


@app.post('/api')
def create_api():
    res = {'api_token': str(uuid.uuid4())}
    app.state.storage.internal.api_tokens.insert_one(res)
    res.pop('_id')
    return res


def validate_api_token(storage, api_token: str):
    query = {'api_token': api_token}
    is_found = next(app.state.storage.internal.api_tokens.find(query), None)
    if not is_found:
        raise fastapi.HTTPException(404, detail='Unknown API token')


@app.get('/api/{api_token}')
def get_resources(api_token: str):
    validate_api_token(app.state.storage, api_token)
    return app.state.storage[api_token].collection_names()


@app.get('/api/{api_token}/{resource}')
def get_resource_list(api_token: str, resource: str):
    validate_api_token(app.state.storage, api_token)
    entities = list(app.state.storage[api_token][resource].find())
    for entity in entities:
        entity['_id'] = str(entity['_id'])

    return entities


@app.post('/api/{api_token}/{resource}')
def create_resource(
    api_token: str,
    resource: str,
    entity: dict = fastapi.Body(...),
):
    validate_api_token(app.state.storage, api_token)
    res = app.state.storage[api_token][resource].insert_one(entity)
    entity['_id'] = str(res.inserted_id)
    return entity


@app.get('/api/{api_token}/{resource}/{entity_id}')
def get_entity(api_token: str, resource: str, entity_id: str):
    validate_api_token(app.state.storage, api_token)
    try:
        query = {'_id': ObjectId(entity_id)}
        [entity] = list(app.state.storage[api_token][resource].find(query))
        entity['_id'] = str(entity['_id'])
    except:
        raise fastapi.HTTPException(404, detail='No entity with given id')

    return entity


@app.put('/api/{api_token}/{resource}/{entity_id}')
def put_entity(
    api_token: str,
    resource: str,
    entity_id: str,
    new_entity: dict = fastapi.Body(...),
):
    query = {'_id': ObjectId(entity_id)}
    app.state.storage[api_token][resource].replace_one(query, new_entity)
    return get_entity(api_token, resource, entity_id)


@app.patch('/api/{api_token}/{resource}/{entity_id}')
def patch_entity(
    api_token: str,
    resource: str,
    entity_id: str,
    patch: dict = fastapi.Body(...),
):
    old_entity = get_entity(api_token, resource, entity_id)
    new_entity = {**old_entity, **patch}
    res = put_entity(api_token, resource, entity_id, new_entity)
    return res


@app.delete('/api/{api_token}/{resource}/{entity_id}')
def delete_resource(api_token: str, resource: str, entity_id: str):
    validate_api_token(app.state.storage, api_token)
    query = {'_id': ObjectId(entity_id)}
    try:
        app.state.storage[api_token][resource].delete_one(query)
    except:
        pass
    return True


if __name__ == '__main__':
    HOST, PORT = 'localhost', 7777
    uvicorn.run(app, host=HOST, port=PORT)