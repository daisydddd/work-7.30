from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
import psycopg2
from typing import List

app = FastAPI()

# 创建数据库引擎
engine = create_engine('postgresql://daisy:Ding20010111@localhost:5432/postgres')

# 创建会话
SessionLocal = sessionmaker(bind=engine)

class Item(BaseModel):
    id: int
    data: str

class TableListResponse(BaseModel):
    tables: List[str]

class ImportResponse(BaseModel):
    message: str

@app.get("/tables", response_model=TableListResponse)
def get_tables():
    try:
        # Establish a connection to the PostgreSQL database
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="postgres",
            user="daisy",
            password="Ding20010111"
        )

        # Create a cursor object to interact with the database
        cur = conn.cursor()

        # 查询数据库中的表名
        cur.execute("""SELECT table_name FROM information_schema.tables
                    WHERE table_schema = 'public'""")
        tables = cur.fetchall()

        # Close the cursor and connection
        cur.close()
        conn.close()

        return {"tables": [table[0] for table in tables]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/import/csv", response_model=ImportResponse)
def import_csv(file: str):
    try:
        # 读取 CSV 文件
        df_csv = pd.read_csv(file)

        # 将数据存储到数据库
        df_csv.to_sql('table_name_csv', engine, if_exists='replace', index=False)

        return {"message": "CSV data imported successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/import/excel", response_model=ImportResponse)
def import_excel(file: str):
    try:
        # 读取 Excel 文件
        df_excel = pd.read_excel(file)

        # 将数据存储到数据库
        df_excel.to_sql('table_name_excel', engine, if_exists='replace', index=False)

        return {"message": "Excel data imported successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))