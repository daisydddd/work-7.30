from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy.ext.declarative import declarative_base
from typing import List

app = FastAPI()

# 创建数据库引擎
engine = create_engine('postgresql://username:password@localhost:5432/mydatabase')

# 创建会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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

# Pydantic 模型
class AnnotationItem(BaseModel):
    type: str
    content: str
    main_data_id: int

class AnnotationResponse(BaseModel):
    id: int
    type: str
    content: str
    main_data_id: int

    class Config:
        orm_mode = True

# 依赖项
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/annotations", response_model=AnnotationResponse)
def create_annotation(annotation: AnnotationItem, db: Session = Depends(get_db)):
    new_annotation = Annotation(
        type=annotation.type,
        content=annotation.content,
        main_data_id=annotation.main_data_id
    )
    db.add(new_annotation)
    db.commit()
    db.refresh(new_annotation)
    return new_annotation

@app.get("/annotations/{annotation_id}", response_model=AnnotationResponse)
def read_annotation(annotation_id: int, db: Session = Depends(get_db)):
    annotation = db.query(Annotation).filter(Annotation.id == annotation_id).first()
    if annotation is None:
        raise HTTPException(status_code=404, detail="Annotation not found")
    return annotation

@app.get("/annotations", response_model=List[AnnotationResponse])
def read_annotations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    annotations = db.query(Annotation).offset(skip).limit(limit).all()
    return annotations