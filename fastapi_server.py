import datetime

from fastapi import FastAPI, HTTPException, Path, Body, Depends
from sqlalchemy.orm import Session
from models import create_db, SessionLocal, Task
from pydantic import BaseModel


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TaskCreate(BaseModel):
    task_name: str
    registration_date: datetime.date
    deadline_date: datetime.date
    status: str

class TaskUpdate(BaseModel):
    task_name: str
    deadline_date: datetime.date
    status: str

@app.post('/tasks', response_model=TaskCreate)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get('/tasks/')
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks

@app.put('/tasks/{id}', response_model=TaskUpdate)
def update_task(id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail='Task not found')
    for var, value in task.model_dump().items():
        setattr(db_task, var, value)
    db.commit()
    return db_task

@app.delete('/tasks/{id}')
def delete_task(id: int, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail='Task not found')
    db.delete(db_task)
    db.commit()
    return {"ok": True}

@app.on_event("startup")
def startup_event():
    create_db()
