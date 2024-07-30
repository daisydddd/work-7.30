from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

app = FastAPI()

# 创建数据库引擎
engine = create_engine('postgresql://username:password@localhost:5432/mydatabase')

# 创建会话
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# 主数据表
class MainData(Base):
    __tablename__ = 'main_data'
    id = Column(Integer, primary_key=True)
    data = Column(String)

# 注释表
class Annotation(Base):
    __tablename__ = 'annotation'
    id = Column(Integer, primary_key=True)
    type = Column(String)  # 注释类型，如 'column' 或 'table'
    content = Column(String)  # 注释内容
    main_data_id = Column(Integer, ForeignKey('main_data.id'))  # 关联到主数据表的外键

    main_data = relationship('MainData', backref='annotations')  # 建立关联

Base.metadata.create_all(engine)

class AnnotationItem(BaseModel):
    type: str
    content: str
    main_data_id: int

@app.post("/annotations")
def create_annotation(annotation: AnnotationItem):
    new_annotation = Annotation(type=annotation.type, content=annotation.content, main_data_id=annotation.main_data_id)
    session.add(new_annotation)
    session.commit()
    return {"message": "Annotation created successfully"}

@app.get("/annotations/{annotation_id}")
def read_annotation(annotation_id: int):
    annotation = session.query(Annotation).filter(Annotation.id == annotation_id).first()
    return {"annotation": {"type": annotation.type, "content": annotation.content, "main_data_id": annotation.main_data_id}}