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
* ENV variable         : `export POSTGRES_HOST=postgresdb POSTGRES_PORT=5432 POSTGRES_DB=postgres POSTGRES_USER=postgres POSTGRES_PASSWORD=sc1er SECRET_KEY=asjdhasjd`
* Build docker compose : `docker compose build`
* Start docker compose : `docker compose up -d`
* Stop docker compose  :
    - `docker compose down -v`  # to remove volumes too
    - `docker compose down`     # to retain state of postgres


---
Testing APIs both via swagger and curl right now
* we can navigate to swagger at `http://127.0.0.1:8000/docs`
    
* Swagger doesn't allow to test APIs requiring Authorization token via header. So testing via curl
```
    1. Sample API           | `curl -X 'GET' 'http://127.0.0.1:8000/application-info' -H 'accept: application/json'`

    2. Users Create Account | `curl -X 'POST'  'http://127.0.0.1:8000/users/create_account' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"email_id": "user2@example.com", "name": "user2 name", "password": "sdfhsdfs", "is_admin": false}'`

    3. Users Login API      | `curl -X 'POST' 'http://127.0.0.1:8000/users/login' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{ "email": "user2@example.com", "password": "sdfhsdfs" }'`
        - Response: `{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InVzZXIyQGV4YW1wbGUuY29tIn0.e-nKJxWTjnjgEoMd8lT31jgga40mtaBqmV7WeouyS8o"}`

    4. Users Suspend API    | `curl --location 'http://127.0.0.1:8000/users/suspend_user' --header 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InVzZXIzQGV4YW1wbGUuY29tIn0.N3LMRxhKqsR4SfttRFnHoTZjGXGDUKbtD8kTKKAQp9s' --header 'Content-Type: application/json' --data-raw '{ "suspend_email": "user2@example.com" }'`
        - Response: Returns appropriate error if invalid token or not-admin. If admin suspends user - `is_active: true`
    
    5. Items AddItem API    | `curl --location 'http://127.0.0.1:8000/shop/add_item' --header 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InVzZXIzQGV4YW1wbGUuY29tIn0.N3LMRxhKqsR4SfttRFnHoTZjGXGDUKbtD8kTKKAQp9s' --header 'Content-Type: application/json' --data '{ "item_name": "bottle", "item_details": "A green bottle", "stock": 3, "cost": 12.56 }'`
        - Response: Only admin can add items

    6 Items ListItems API  | `curl --location 'http://127.0.0.1:8000/shop/item_list' --header 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InVzZXIxQGV4YW1wbGUuY29tIn0.8d5Xn3qxJEahbkZCnV4Ww0IWe5bLAUkKWCYDkigD0ao'`
        - Response: List of items for any user who is active
```
* Will be creating a postman collection and sharing
---


## What's pending
* Introduce stock and cost constraints within items table; Index user_ref field in carts; modify_cart as transaction; only list items with non-zero stock
* Adding tests
* If possible, CICD via github actions
* Pending documentation: HowTo of everything including how to secure and scale this application
