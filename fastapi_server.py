from fastapi import FastAPI, HTTPException, Path, Body, Depends
from sqlalchemy.orm import Session

from src.models import create_db, SessionLocal, Task
from src.schemas import NewTaskInfo, UpdatedTaskInfo
from src.task_manager import TaskManager

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/tasks', response_model=NewTaskInfo)
def create_task(task: NewTaskInfo, db: Session = Depends(get_db)):
    task_manager = TaskManager(db)
    return task_manager.create_task(task=task)

@app.get('/tasks/')
def get_tasks(db: Session = Depends(get_db)):
    task_manager = TaskManager(db)
    return task_manager.get_tasks()

@app.put('/tasks/{id}', response_model=UpdatedTaskInfo)
def update_task(id: int, task: UpdatedTaskInfo, db: Session = Depends(get_db)):
    task_manager = TaskManager(db)
    return task_manager.update_task(id=id, task=task)

@app.delete('/tasks/{id}')
def delete_task(id: int, db: Session = Depends(get_db)):
    task_manager = TaskManager(db)
    return task_manager.delete_task(id=id)

@app.on_event("startup")
def startup_event():
    create_db()
