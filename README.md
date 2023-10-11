# Shopping Cart 

## Choices - Python and FastAPI. And Why?
Choice of programming Language: Python (Comfortble using python to build apps)
Choice of API framework: FastAPI as its a high-performance web framework for building APIs with Python and its on par with NodeJS and Go for high performance compared to other python web frameworks.

## Quick explanation of design - will elaborate
    - FastAPI web app to serve user, item and cart APIs making up the shopping cart app
    - Choice of RDBMS: PostgresSQL with tables - users, items and carts
    - The web ap with be containarized along with Postgres image and run via docker-compose
        - The setup is of single node right now, will elaborate on how to scale the above setup for performance and scale in a section below later

## Current Local setup as I build this and continue testing
    - Code path           : `./src`
    - Virtual ENV         : `virtualenv --python=/usr/bin/python3.8 shopcart`
    - Source virtual env  : `source shopcart/bin/activate`
    - Insall dependencies : `pip install -r requirements.txt`
    - Start Postgres      : `docker compose up -d`  (docker-compose.yml)
    - Create tables       : 
        ```
        - psql -h 127.0.0.1 -U postgres
        - DROP TABLE IF EXIST users;
        - CREATE TABLE users (id SERIAL PRIMARY KEY, email_id VARCHAR(255) NOT NULL, pwd_hash VARCHAR(255) NOT NULL, name VARCHAR(255) NOT NULL, is_active BOOLEAN DEFAULT TRUE, is_admin BOOLEAN DEFAULT FALSE, UNIQUE(email_id));
        - DROP TABLE IF EXIST items;
        - CREATE TABLE items (id SERIAL PRIMARY KEY, item_name VARCHAR(255) NOT NULL, item_details VARCHAR(255) NOT NULL, stock INT NOT NULL, cost FLOAT);
        - Yet to start with carts table and respective APIs
        ```
    - Set ENV variable    : `export POSTGRES_HOST=localhost POSTGRES_PORT=5432 POSTGRES_DB=postgres POSTGRES_USER=postgres POSTGRES_PASSWORD=sc1er SECRET_KEY=asjdhasjd`
    - Start App           : `uvicorn main_app:app --reload`

    **NOTE** Will be contanarizing the app and add it as a service within docker-compose to start the whole setup with just `docker compose up -d`


    Testing APIs both via swagger and curl right now:
        - we can navigate to swagger at `http://127.0.0.1:8000/docs`
        - ![swagger image](https://github.com/figsbt/shopping-cart/blob/master/src/swagger.png?raw=true)
        - **Note** Swagger doesn't to test APIs requirent Authorization token via header so testing via curl
            - Sample requests
            - Sample | 
        - Will be creating a postman collection and sharing


##  What's completed
    - Web app with API support for all usermanagement which includes 
        - API to create_account both admin and normal user
        - API for users to login
        - API to suspend_users (only admins can)
        - API for admins to add items
        - API for users to list items
    - Custom RBAC support to distinguish admin / not-admin roles
    - Code tree
    ```
        ├── README.md
        └── src
            ├── app_routers
            │   ├── enforce_roles.py
            │   ├── __init__.py
            │   ├── shop_router.py
            │   └── user_router.py
            ├── docker-compose.yml
            ├── __init__.py
            ├── main_app.py
            ├── models_schemas
            │   ├── __init__.py
            │   ├── shop_ms.py
            │   └── users_ms.py
            ├── rdb_store
            │   ├── dbops.py
            │   ├── __init__.py
            │   ├── shop.py
            │   └── users.py
            ├── requirements.txt
            └── settings.py
    ```


## What's pending
    - Introduce stock and cost constraints within items table
    - Cart APIs for both adding items(if stock) and removing them from cart
    - Containarizing the entire setup via docker-compose
    - Adding tests
    - Pending documentation: HowTo of everything
