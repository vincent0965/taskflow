from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pathlib import Path

import os

# 載入檔案
load_dotenv()

# 連接DB
DATABASE_URL = os.getenv("DATABASE_URL")

# 建立資料庫
eng_DB = create_engine(
    DATABASE_URL,
    echo = True,
    future = True
)

# 建立DB session
SessionLocal = sessionmaker( autocommit=False, autoflush=False, bind=eng_DB)

# 建立Base class
Base = declarative_base()








