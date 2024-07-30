from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from Theyta.Data_Annotation import MainData

app = FastAPI()

# 创建数据库引擎
engine = create_engine('postgresql://username:password@localhost:5432/mydatabase')

# 创建会话
Session = sessionmaker(bind=engine)
session = Session()

@app.get("/maindata/{data}")
def query_maindata(data: str):
    # 构建查询
    query = select([MainData.data]).where(MainData.data == data)

    # 执行查询并获取结果
    results = session.execute(query)

    # 返回结果
    return {"results": [result for result in results]}

@app.get("/maindata/annotations")
def query_maindata_with_annotations():
    # 构建联结查询
    query = session.query(MainData).options(joinedload(MainData.annotations))

    # 执行查询并获取结果
    results = query.all()

    # 返回结果
    return {"results": [{"maindata_id": main_data.id, "data": main_data.data, "annotations": [{"annotation_id": annotation.id, "type": annotation.type, "content": annotation.content} for annotation in main_data.annotations]} for main_data in results]}

@app.get("/maindata/columns/{columns}")
def query_maindata_columns(columns: str):
    # 细粒度的列选择
    query = session.query(MainData.id, MainData.data) if columns == "id,data" else session.query(MainData)

    # 执行查询并获取结果
    results = query.all()

    # 返回结果
    return {"results": [result for result in results]}