from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from typing import List, Dict, Any

from Theyta.Data_Annotation import MainData

app = FastAPI()

# 创建数据库引擎
engine = create_engine('postgresql://username:password@localhost:5432/mydatabase')

# 创建会话
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

class MainDataResponse(BaseModel):
    id: int
    data: str

class AnnotationResponse(BaseModel):
    annotation_id: int
    type: str
    content: str

class MainDataWithAnnotationsResponse(BaseModel):
    maindata_id: int
    data: str
    annotations: List[AnnotationResponse]

@app.get("/maindata/{data}", response_model=List[MainDataResponse])
def query_maindata(data: str):
    # 构建查询
    query = select([MainData.id, MainData.data]).where(MainData.data == data)

    # 执行查询并获取结果
    results = session.execute(query).fetchall()

    # 返回结果
    return [{"id": result.id, "data": result.data} for result in results]

@app.get("/maindata/{column}/{value}", response_model=List[Dict[str, Any]])
def query_maindata(column: str, value: str):
    # 构建查询
    query = select([text(column)]).where(text(f"{column} = :value"))

    # 执行查询并获取结果
    results = session.execute(query, {"value": value}).fetchall()

    # 返回结果
    return [{column: result[0]} for result in results]

@app.get("/maindata/annotations", response_model=List[MainDataWithAnnotationsResponse])
def query_maindata_with_annotations():
    # 构建联结查询
    query = session.query(MainData).options(joinedload(MainData.annotations))

    # 执行查询并获取结果
    results = query.all()

    # 返回结果
    return [{"maindata_id": main_data.id, "data": main_data.data, "annotations": [{"annotation_id": annotation.id, "type": annotation.type, "content": annotation.content} for annotation in main_data.annotations]} for main_data in results]

@app.get("/maindata/columns/{columns}", response_model=List[Dict[str, Any]])
def query_maindata_columns(columns: str):
    # 细粒度的列选择
    if columns == "id,data":
        query = session.query(MainData.id, MainData.data)
    else:
        query = session.query(MainData)

    # 执行查询并获取结果
    results = query.all()

    # 返回结果
    return [dict(result) for result in results]