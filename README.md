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
git clone https://github.com/cuamckuu/getREST.git
cd getREST
make build run  # Will build docker image and run it on port 7777
```

# TODO

- [X] Generate token API
- [X] Endpoint for GET resource
- [X] Endpoint for POST resource
- [X] Endpoint for DELETE
- [X] Endpoint for PUT
- [X] Endpoint for PATCH
- [X] Add tests for CRUD
- [X] Add persistent storage (montydb)
- [X] Docker image
- [ ] Configure from .env
- [ ] Add tests for errors
- [ ] User Dashboard for token
- [ ] Admin dashboard for tokens
- [ ] Token (custom) TTL
- [ ] Protected API
- [ ] Versioning?
- [ ] Nested resources?
- [ ] Field filters? `?fields=id,name,author`
- [ ] API callbacks or redirrects?
- [ ] HATEOAS?
- [ ] Idempotency?
- [ ] Custom IDs?
- [ ] Landing page?
- [ ] Custom rate limits
- [ ] Custom endpoints caching `POST /api/123/cats/config/cache`?
- [ ] Custom storage size limits `POST /api/123/cats/config/size`?
- [ ] Admin basic auth
- [ ] Custom API auth? `POST /api/123/cats/config/auth`?
- [ ] HTTPS?
- [ ] Auto OpenApi docs?
- [ ] XML responses?
- [ ] CSV responses?
- [ ] Pagination
- [ ] Validation? `POST /api/123/cats/config/validator`?

Notes:
- Good rest example with HATEOAS, Filters, Sorting, Pagination: https://habr.com/ru/post/276731/
- Another one: https://github.com/typicode/json-server
