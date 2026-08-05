from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


def get_tasks(db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> list[Task]:
    return (
        db.query(Task)
        .filter(Task.owner_id == owner_id)
        .order_by(Task.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_task(db: Session, task_id: int, owner_id: int) -> Task | None:
    return db.query(Task).filter(Task.id == task_id, Task.owner_id == owner_id).first()


def create_task(db: Session, task_in: TaskCreate, owner_id: int) -> Task:
    db_task = Task(**task_in.model_dump(), owner_id=owner_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, db_task: Task, task_in: TaskUpdate) -> Task:
    for field, value in task_in.model_dump(exclude_unset=True).items():
        setattr(db_task, field, value)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, db_task: Task) -> None:
    db.delete(db_task)
    db.commit()
