# getREST

Service to provide simple RESTful API for small business, MVPs or prototypes...

![diagram](./assets/diagram.drawio.png)

# Why

Often all you need from API is just common CRUD operations and with `getREST` it's easy to get such API even without programming

# Actions

`getREST` supports CRUD operations listed below:

Action  | HTTP Verb                 | Description
--------|---------------------------|--------------
Create  | `POST /<resource>`        | Create resource entity from JSON payload
Read    | `GET /<resource>`         | Get all entities from the resource
Read    | `GET /<resource>/<id>`    | Get one resource entity by id
Update  | `PUT /<resource>/<id>`    | Replace existing resource entitiy JSON payload
Update  | `PATCH /<resource>/<id>`  | Partial update for existing resource entitiy with JSON payload
Delete  | `DELETE /<resource>/<id>` | Delete resource entity

# Examples

```bash
# Get personal API endpoint
curl -X POST 'http://localhost:7777/api'
# => {"api_token":"4be8973a-5991-44f0-ba2a-1c968a5a7168"}

# Get entities list for given resource
curl 'http://localhost:7777/api/4be8973a-5991-44f0-ba2a-1c968a5a7168/cats'
# => []

# Create new entity for given resource
curl -X POST 'http://localhost:7777/api/4be8973a-5991-44f0-ba2a-1c968a5a7168/cats' -H 'Content-Type: application/json' --data '{"name": "Felix", "color": "black"}'
# => {"name":"Felix","color":"black","_id":"0f002a06-a6a3-4ada-9653-d017c87155d1"}

# Get all available resources
curl 'http://localhost:7777/api/4be8973a-5991-44f0-ba2a-1c968a5a7168'
# => ["cats"]

# Get entities list for given resource
curl 'http://localhost:7777/api/4be8973a-5991-44f0-ba2a-1c968a5a7168/cats'
# => [{"name":"Felix","color":"black","_id":"0f002a06-a6a3-4ada-9653-d017c87155d1"}]

# Replace given entitiy
curl -X PUT 'http://localhost:7777/api/4be8973a-5991-44f0-ba2a-1c968a5a7168/cats/0f002a06-a6a3-4ada-9653-d017c87155d1' -H 'Content-Type: application/json' --data '{"name": "Felix"}'
# => {"name":"Felix","_id":"0f002a06-a6a3-4ada-9653-d017c87155d1"}

# Partial update given entity
curl -X PATCH 'http://localhost:7777/api/4be8973a-5991-44f0-ba2a-1c968a5a7168/cats/0f002a06-a6a3-4ada-9653-d017c87155d1' -H 'Content-Type: application/json' --data '{"color": "black"}'
# => {"name":"Felix","color":"black","_id":"0f002a06-a6a3-4ada-9653-d017c87155d1"}

# Delete given entity
curl -X DELETE 'http://localhost:7777/api/4be8973a-5991-44f0-ba2a-1c968a5a7168/cats/0f002a06-a6a3-4ada-9653-d017c87155d1'
# => true

# Get entities list for given resource
curl 'http://localhost:7777/api/4be8973a-5991-44f0-ba2a-1c968a5a7168/cats'
# => []
```

# Usage

```bash
# TODO: docker run ...
```

# TODO

- [X] Generate token API
- [X] Endpoint for GET resource
- [X] Endpoint for POST resource
- [X] Endpoint for DELETE
- [X] Endpoint for PUT
- [X] Endpoint for PATCH
- [ ] Add tests
- [ ] User Dashboard for token
- [ ] Admin dashboard for tokens
- [ ] Add persistent storage
- [ ] Token (custom) TTL
- [ ] Protected API
- [ ] Versioning?
- [ ] Nested resources?
- [ ] Field filters? `?fields=id,name,author` vs `Accept:` header
- [ ] API callbacks?
- [ ] HATEOAS?
- [ ] Idempotency?
- [ ] Custom non uuid4 IDs?
- [ ] Landing page?
- [ ] Docker image
- [ ] Custom rate limits
- [ ] Custom endpoints caching
- [ ] Custom storage size limits
- [ ] Admin basic auth
- [ ] Custom API auth?
- [ ] Configure from .env
