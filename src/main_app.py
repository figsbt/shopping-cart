from fastapi import FastAPI
from rdb_store.dbops import reset_db_on_startup
from app_routers import user_router, shop_router


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    reset_db_on_startup()

@app.get("/application-info")
async def application_intro():
    return {
        "Intro": "A shopping-cart application."
    }


app.include_router(user_router.router, prefix="/users", tags=["Users"])
app.include_router(shop_router.router, prefix="/shop", tags=["Shop"])


@app.on_event("shutdown")
async def shutdown_event():
    pass
