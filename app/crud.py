from sqlalchemy.orm import Session
from . import models, schemas

def get_all_todos(db: Session):
    return db.query(models.Todo).all()

def get_todo(db: Session, id: int):
    return db.query(models.Todo).filter(models.Todo.id == id).first()

def create_todo(db: Session, todo: schemas.TodoCreate):
    db_todo = models.Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def update_todo(db: Session, id: int, todo: schemas.TodoUpdate):
    db_todo = get_todo(db, id)
    if db_todo:
        db_todo.title = todo.title
        db_todo.completed = todo.completed
        db.commit()
        db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, id: int):
    db_todo = get_todo(db, id)
    if db_todo:
        db.delete(db_todo)
        db.commit()

def filter_todos(db: Session, status: str):
    if status == "completed":
        return db.query(models.Todo).filter(models.Todo.completed == True).all()
    elif status == "pending":
        return db.query(models.Todo).filter(models.Todo.completed == False).all()
    return get_all_todos(db)
