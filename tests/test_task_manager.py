import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Base, Task
from src.task_manager import TaskManager
from src.schemas import NewTaskInfo, UpdatedTaskInfo, Status
import datetime


DATABASE_URL = 'sqlite:///./test.db'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class TestTaskManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Base.metadata.create_all(bind=engine)

    @classmethod
    def tearDownClass(cls) -> None:
        Base.metadata.drop_all(bind=engine)

    def setUp(self) -> None:
        self.db = SessionLocal()
        self.task_manager = TaskManager(db=self.db)

    def tearDown(self) -> None:
        self.db.close()

    def test_create_task(self):
        new_task = NewTaskInfo(
            task_name="test task",
            registration_date=datetime.date.today(),
            deadline_date=datetime.date.today() + datetime.timedelta(days=1),
            status=Status.not_yet
        )
        created_task = self.task_manager.create_task(task=new_task)
        self.assertIsNotNone(created_task.id)
        self.assertEqual(created_task.task_name, new_task.task_name)
        self.assertEqual(created_task.registration_date, new_task.registration_date)
        self.assertEqual(created_task.deadline_date, new_task.deadline_date)
        self.assertEqual(created_task.status, new_task.status)

    def test_get_task(self):
        tasks = self.task_manager.get_tasks()
        self.assertIsInstance(tasks, list)

    def test_update_task(self):
        new_task = NewTaskInfo(
            task_name="test to be updated",
            registration_date=datetime.date.today(),
            deadline_date=datetime.date.today() + datetime.timedelta(days=1),
            status=Status.not_yet
        )
        created_task = self.task_manager.create_task(task=new_task)
        update_data = UpdatedTaskInfo(
            task_name="test updated",
            deadline_date=datetime.date.today() + datetime.timedelta(days=2),
            status=Status.in_progress
        )
        updated_task = self.task_manager.update_task(id=created_task.id, task=update_data)
        self.assertEqual(updated_task.task_name, update_data.task_name)
        self.assertEqual(updated_task.status, update_data.status)

    def test_delete_task(self):
        new_task = NewTaskInfo(
            task_name="test to be updated",
            registration_date=datetime.date.today(),
            deadline_date=datetime.date.today() + datetime.timedelta(days=1),
            status=Status.not_yet
        )
        created_task = self.task_manager.create_task(task=new_task)
        response = self.task_manager.delete_task(id=created_task.id)
        self.assertEqual(response, {"ok": True})
        self.assertIsNone(self.db.query(Task).filter(Task.id == created_task.id).first())
