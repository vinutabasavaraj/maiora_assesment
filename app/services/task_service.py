from sqlalchemy.orm import Session
from app.common.connect_db import get_db
from fastapi import APIRouter, Depends, HTTPException
from app.models.task_models import User, Tasks, Messages



def create_task(db,task):
    task_data = Tasks(title = task.title, description=task.description,completed=task.completed,extension=task.extension,owner_id=task.owner_id)
    db.add(task_data)
    db.commit()
    db.refresh(task_data)
    return task_data

def get_task(db, task_id):
    return db.query(Tasks).filter(Tasks.id == task_id).first()

def update_task(db, task_id, updated_task):
    existing_task = db.query(Tasks).filter(Tasks.id == task_id).first()
    existing_task.title = updated_task.title
    existing_task.description = updated_task.description
    existing_task.due_date = updated_task.due_date
    existing_task.priority = updated_task.priority
    existing_task.assigned_team_members = updated_task.assigned_team_members
    db.commit()
    db.refresh(existing_task)
    return existing_task

def delete_task(db, task_id):
    task = db.query(Tasks).filter(Tasks.id == task_id).first()
    db.delete(task)
    db.commit()
    return task
