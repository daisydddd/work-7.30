from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, joinedload
import pandas as pd
import psycopg2

app = FastAPI()
# 2.实现数据导入功能:
# 创建数据库引擎
engine = create_engine('postgresql://daisy:Ding20010111@localhost:5432/postgres')

# 创建会话
Session = sessionmaker(bind=engine)
session = Session()

class Item(BaseModel):
    id: int
    data: str

@app.get("/tables")
def get_tables():
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

    return {"tables": tables}

@app.post("/import/csv")
def import_csv(file: str):
    # 读取 CSV 文件
    df_csv = pd.read_csv(file)

    # 将数据存储到数据库
    df_csv.to_sql('table_name_csv', engine, if_exists='replace', index=False)

    return {"message": "CSV data imported successfully"}

@app.post("/import/excel")
def import_excel(file: str):
    # 读取 Excel 文件
    df_excel = pd.read_excel(file)

    # 将数据存储到数据库
    df_excel.to_sql('table_name_excel', engine, if_exists='replace', index=False)

    return {"message": "Excel data imported successfully"}

# 3.实现数据注释功能:


