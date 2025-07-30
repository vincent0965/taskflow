from fastapi  import FastAPI
from sqlalchemy import text
from app.core.database import Base, eng_DB
from app.models import user
from app.routers import auth_router, user_router
from app.utils import create_access_token
from app.config import setting

import asyncio


#測試連線
app = FastAPI()

# @app.get("/db-check")
# def db_check():
#     try:
#         db = SessionLocal()
#         db.execute(text("select 1"))
#         return {"db_status":"success"}
#     except Exception as e:
#         return {"db_status":"fail","error":str(e)}
#     finally:
#         db.close()


async def auto_refresh_token():
    while True:
        new_token = create_access_token(data={"sub":"system_refresh"})
        print(f"[Auto refresh] New Token: {new_token}")
        # test for auto refresh
        await asyncio.sleep(60)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(auto_refresh_token())

def on_startup():
    Base.metadata.create_all(bind=eng_DB)

app.include_router(auth_router.router)
app.include_router(user_router.router)