from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.crud import task as crud_task
from app.db.session import get_db
from app.models.user import User
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskOut])
def list_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return crud_task.get_tasks(db, owner_id=current_user.id, skip=skip, limit=limit)


@router.post("", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return crud_task.create_task(db, task_in, owner_id=current_user.id)


@router.get("/{task_id}", response_model=TaskOut)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = crud_task.get_task(db, task_id, owner_id=current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int,
    task_in: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = crud_task.get_task(db, task_id, owner_id=current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return crud_task.update_task(db, task, task_in)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = crud_task.get_task(db, task_id, owner_id=current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    crud_task.delete_task(db, task)
