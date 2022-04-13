#!/usr/bin/env python3

import uuid

import fastapi
import uvicorn


app = fastapi.FastAPI()
app.state.storage = {}


@app.post('/api')
def create_api():
    api_token = str(uuid.uuid4())
    app.state.storage[api_token] = {}
    return {'api_token': api_token}


def validate_api_token(storage, api_token: str):
    if api_token not in storage:
        raise fastapi.HTTPException(404, detail='Unknown API token')


@app.get('/api/{api_token}')
def get_resources(api_token: str):
    validate_api_token(app.state.storage, api_token)

    resources = list(app.state.storage.get(api_token, {}).keys())
    return resources


@app.get('/api/{api_token}/{resource}')
def get_resource_list(api_token: str, resource: str):
    validate_api_token(app.state.storage, api_token)

    entities = list(
        app.state.storage[api_token].get(resource, {}).values()
    )
    return entities


@app.post('/api/{api_token}/{resource}')
def create_resource(
    api_token: str,
    resource: str,
    entity: dict = fastapi.Body(...),
):
    validate_api_token(app.state.storage, api_token)

    entity_id = str(uuid.uuid4())
    entity['_id'] = entity_id
    app.state.storage.setdefault(api_token, {}).setdefault(resource, {})
    app.state.storage[api_token][resource][entity_id] = entity

    return entity


@app.get('/api/{api_token}/{resource}/{entity_id}')
def get_entity(api_token: str, resource: str, entity_id: str):
    validate_api_token(app.state.storage, api_token)
    try:
        entity = (
            app.state.storage.get(api_token, {}).get(resource, {})[entity_id]
        )
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
    old_entity = get_entity(api_token, resource, entity_id)
    new_entity['_id'] = old_entity['_id']
    app.state.storage[api_token][resource][entity_id] = new_entity

    return new_entity


@app.patch('/api/{api_token}/{resource}/{entity_id}')
def put_entity(
    api_token: str,
    resource: str,
    entity_id: str,
    new_entity: dict = fastapi.Body(...),
):
    old_entity = get_entity(api_token, resource, entity_id)
    new_entity.pop('_id', None)
    old_entity.update(new_entity)
    app.state.storage[api_token][resource][entity_id] = old_entity

    return old_entity


@app.delete('/api/{api_token}/{resource}/{entity_id}')
def delete_resource(api_token: str, resource: str, entity_id: str):
    validate_api_token(app.state.storage, api_token)
    app.state.storage.get(api_token, {}).get(resource, {}).pop(entity_id, None)

    return True


if __name__ == '__main__':
    HOST, PORT = 'localhost', 7777
    uvicorn.run(app, host=HOST, port=PORT)