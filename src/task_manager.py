from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.schemas import NewTaskInfo, UpdatedTaskInfo
from src.models import Task

class TaskManager:
    def __init__(self, db: Session):
        self.db = db

    def create_task(self, task: NewTaskInfo):
        db_task = Task(**task.model_dump())
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def get_tasks(self):
        return self.db.query(Task).all()

    def update_task(self, id: int, task: UpdatedTaskInfo):
        db_task = self.db.query(Task).filter(Task.id == id).first()
        if not db_task:
            raise HTTPException(status_code=404, detail='Task not found.')
        for var, value in task.model_dump().items():
            setattr(db_task, var, value)
        self.db.commit()
        return db_task

    def delete_task(self, id: int):
        db_task = self.db.query(Task).filter(Task.id == id).first()
        if not db_task:
            raise HTTPException(status_code=404, detail='Task not found.')
        self.db.delete(db_task)
        self.db.commit()
        return {"ok": True}
