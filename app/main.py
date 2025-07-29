from fastapi  import FastAPI
from sqlalchemy import text
from app.core.database import Base, eng_DB
from app.models import user
from app.routers import auth_router, user_router


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

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=eng_DB)

app.include_router(auth_router.router)
app.include_router(user_router.router)


