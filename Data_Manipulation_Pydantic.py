from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from typing import Any

from Theyta.Data_Annotation import MainData

app = FastAPI()

# 创建数据库引擎
engine = create_engine('postgresql://username:password@localhost:5432/mydatabase')

# 创建会话
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

class MainDataItem(BaseModel):
    data: str

class ResponseMessage(BaseModel):
    message: str

@app.put("/maindata/{id}", response_model=ResponseMessage)
def update_maindata(id: int, item: MainDataItem):
    # 找到要更新的对象
    main_data_to_update = session.query(MainData).filter(MainData.id == id).first()
    if main_data_to_update is None:
        raise HTTPException(status_code=404, detail="Item not found")
    # 更新对象的属性
    main_data_to_update.data = item.data
    # 提交更改
    session.commit()
    return ResponseMessage(message="Data updated successfully")

@app.delete("/maindata/{id}", response_model=ResponseMessage)
def delete_maindata(id: int):
    # 找到要删除的对象
    main_data_to_delete = session.query(MainData).filter(MainData.id == id).first()
    if main_data_to_delete is None:
        raise HTTPException(status_code=404, detail="Item not found")
    # 删除对象
    session.delete(main_data_to_delete)
    # 提交更改
    session.commit()
    return ResponseMessage(message="Data deleted successfully")