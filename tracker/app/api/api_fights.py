from fastapi import APIRouter, HTTPException
from app.db.database import SessionDep
from app.core.models.models import Fight


fights_router = APIRouter(prefix="/fights", tags=["fights"])

@fights_router.get("/")
def get_fights(session: SessionDep):
    fights = session.query(Fight).all()
    return fights


@fights_router.get("/{id}")
def get_fight(id: int, session: SessionDep):
    fight = session.query(Fight).filter(Fight.id == id).first()
    if not fight:
        raise HTTPException(status_code=404, detail="fight not found")
    return fight


@fights_router.post("/")
def create_fight(session: SessionDep, fight: Fight):
    session.add(fight)
    session.commit()
    session.refresh(fight)
    return fight


@fights_router.put("/{id}")
def update_fight(session: SessionDep, id: int, fight: Fight):
    existing_fight = session.query(Fight).filter(Fight.id == id).first()
    if not existing_fight:
        raise HTTPException(status_code=404, detail="fight not found")

    # update manually the fields. pydantic way
    for key, value in fight.dict(exclude_unset=True).items():
        setattr(existing_fight, key, value)

    session.commit()
    session.refresh(existing_fight)
    return existing_fight


@fights_router.delete("/{id}")
def delete_fight(session: SessionDep, id: int):
    fight = session.query(Fight).filter(Fight.id == id).first()
    if not fight:
        raise HTTPException(status_code=404, detail="fight not found")

    session.delete(fight)
    session.commit()
    return {"message": "fight deleted"}
