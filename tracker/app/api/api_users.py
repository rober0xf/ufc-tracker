from fastapi import APIRouter, HTTPException
from app.db.database import SessionDep
from app.core.models.models import User

users_router = APIRouter(prefix="/users", tags=["users"])

@users_router.get("/")
def get_users(session: SessionDep):
    users = session.query(User).all()
    return users


@users_router.get("/{id}")
def get_user(id: int, session: SessionDep):
    user = session.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user


@users_router.post("/")
def create_user(user: User, session: SessionDep):
    input_user = session.query(User).filter(User.email == user.email).first()  # if user already exists
    if input_user:
        raise HTTPException(status_code=409, detail="user already exists")

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@users_router.put("/{id}")
def update_user(user: User, id: int, session: SessionDep):
    existing_user = session.query(User).filter(User.id == id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="user not found")

    for key, value in user.dict(exclude_unset=True).items():
        setattr(existing_user, key, value)

    session.commit()
    session.refresh(existing_user)
    return user


@users_router.delete("/{id}")
def delete_user(id: int, session: SessionDep):
    user = session.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    session.delete(user)
    session.commit()
    return {"message": "user deleted"}
