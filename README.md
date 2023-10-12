# Shopping Cart 

## Choices - Python and FastAPI. And Why?
* Choice of programming Language: Python (Comfortble using python to build web-apps)
* Choice of API framework: FastAPI as its a high-performance web framework for building APIs with Python and its on par with NodeJS and Go for high performance compared to other python web frameworks.

## Design
* FastAPI web app to serve user, item and cart APIs making up the shopping cart app
* Choice of RDBMS: PostgresSQL with tables - users, items and carts
* The web ap with be containarized along with Postgres image and run via docker-compose. 
* The setup is of single node right now, will elaborate on how to scale the above setup for performance and scale in a section below later.

## How to setup and test the APIs
* Working directory    : `src`
* ENV variable         : `export POSTGRES_HOST=postgresdb POSTGRES_PORT=5432 POSTGRES_DB=postgres POSTGRES_USER=postgres POSTGRES_PASSWORD=sc1er SECRET_KEY=asjdhasjd APP_WORKERS=2`
* Build docker compose : `docker compose build`
* Start docker compose : `docker compose up -d`
* Stop docker compose  :
    - `docker compose down -v`  # to remove volumes too
    - `docker compose down`     # to retain state of postgres


---
Testing APIs both via swagger and curl right now
* we can navigate to swagger at `http://127.0.0.1:8000/docs` or `http://127.0.0.1:8000/redoc`
* We can test APIs which don't need header authorization via swagger. Otherwise they are a good place to check input output schemas.
    
* Swagger doesn't allow to test APIs requiring Authorization token via header. So everything testing via curl
```
    1. Initialize tables API
        - Request: curl -X 'GET' 'http://127.0.0.1:8000/initialize-tables' -H 'accept: application/json'
        - Response: {"Message": "Tables initialized - users, items and carts"}

    2. Users Create Account
        - Request: curl -X 'POST'  'http://127.0.0.1:8000/users/create_account' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"email_id": "user2@example.com", "name": "user2 name", "password": "sdfhsdfs", "is_admin": false}'
        - Response: { "email_id": "user5@example.com", "name": "string5", "id": 6, "is_admin": false }

    3. Users Login API
        - Reqiest: curl -X 'POST' 'http://127.0.0.1:8000/users/login' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{ "email": "user2@example.com", "password": "sdfhsdfs" }'
        - Response: {"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InVzZXIyQGV4YW1wbGUuY29tIn0.e-nKJxWTjnjgEoMd8lT31jgga40mtaBqmV7WeouyS8o"}

    4. Users Suspend API
        -Request: curl --location 'http://127.0.0.1:8000/users/suspend_user' --header 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InVzZXIzQGV4YW1wbGUuY29tIn0.N3LMRxhKqsR4SfttRFnHoTZjGXGDUKbtD8kTKKAQp9s' --header 'Content-Type: application/json' --data-raw '{ "suspend_email": "user2@example.com" }'
        - Response: {"Message": "Suspended <user2@example.com> !"} | Otherwise returns appropriate error if invalid token or not-admin. If admin suspends user - `is_active: true`
    
    5. Items AddItem API
        - Request | curl --location 'http://127.0.0.1:8000/shop/add_item' --header 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InVzZXIzQGV4YW1wbGUuY29tIn0.N3LMRxhKqsR4SfttRFnHoTZjGXGDUKbtD8kTKKAQp9s' --header 'Content-Type: application/json' --data '{ "item_name": "bottle", "item_details": "A green bottle", "stock": 3, "cost": 12.56 }'
        - Response: { "item_name": "bottle", "item_details": "A green bottle", "stock": 3, "cost": 12.56 } | Only admin can add items

    6. Items ListItems API
        - Request: curl --location 'http://127.0.0.1:8000/shop/item_list' --header 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InVzZXIxQGV4YW1wbGUuY29tIn0.8d5Xn3qxJEahbkZCnV4Ww0IWe5bLAUkKWCYDkigD0ao'
        - Response: [{Item}] 

    7. Cart of the User API
        - Request | curl --location 'http://127.0.0.1:8000/shop/cart/get_cart' --header 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InVzZXIxMkBleGFtcGxlLmNvbSJ9.e-l02S3NtYIw7ZzT3OtSGQgbjYOBRlfu67M-8PEaTgk'
        - Response: {"user_ref": 1, "items_ref": {}, "id": 1}

    8. Cart Add Item API 
        - Request: curl --location 'http://127.0.0.1:8000/shop/cart/add_item' --header 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGV4YW1wbGUuY29tIn0.gEPbdGuHi7yzL8JtI5QBTTrZVsAxlrfgvXyxX1aewaw' --header 'Content-Type: application/json' --data '{ "item_id": 1 }'
        - Response: { "user_ref": 1, "items_ref": { "1": 3 }, "id": 1 }

    9. Cart Remove Item API
        - Request: curl --location 'http://127.0.0.1:8000/shop/cart/remove_item' --header 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGV4YW1wbGUuY29tIn0.gEPbdGuHi7yzL8JtI5QBTTrZVsAxlrfgvXyxX1aewaw' --header 'Content-Type: application/json' --data '{ "item_id": 1 }'
        - Response: { "user_ref": 1, "items_ref": { "1": 2 }, "id": 1 }
```
* postman-collection is attached in the email.
---


## How to scale this. A short note.

    - Any RDBMS(PostgresSQL here) should be a muti-node distributed setup. 
        - Data sharded across the nodes for better performance
        - Each primary shard with a replica for high availability
        - Something like this (https://vitess.io/) to scale MySQL

    - As the web-app itself is containarized, it can be deployed on kubernetes to scale on demand.

## Couldn't add these because of the lack of time
* More tests and CICD via github actions
