import os
from fastapi import FastAPI
from app_routers import user_router, shop_router


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    pass

@app.get("/initialize-tables")
async def application_intro():
    os.system(f"PGPASSWORD={os.getenv('POSTGRES_PASSWORD')} psql -h {os.getenv('POSTGRES_HOST')} -U postgres -q -f init.sql")
    return {
        "Message": "Tables initialized - users, items and carts"
    }


app.include_router(user_router.router, prefix="/users", tags=["Users"])
app.include_router(shop_router.router, prefix="/shop", tags=["Shop"])


@app.on_event("shutdown")
async def shutdown_event():
    pass
