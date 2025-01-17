from fastapi import APIRouter, HTTPException
from app.db.database import SessionDep
from app.core.models.models import Fighter
from datetime import datetime

fighters_router = APIRouter(prefix="/fighters", tags=["fighters"])

# get all fighters
@fighters_router.get("/")
def get_fighters(session: SessionDep):
    fighters = session.query(Fighter).all()
    return fighters


# get fighter by id
@fighters_router.get("/{id}")
def get_fighter_by_id(session: SessionDep, id: int):
    fighter = session.query(Fighter).filter(Fighter.id == id).first()
    if not fighter:
        raise HTTPException(status_code=404, detail="fighter not found")
    return fighter


# add fighter
@fighters_router.post("/")
def create_fighter(session: SessionDep, fighter: Fighter):
    if isinstance(fighter.birth_date, str):
        fighter.birth_date = datetime.strptime(fighter.birth_date, "%Y-%m-%d").date()

    # to not include the id
    payload_fighter = Fighter(
        full_name=fighter.full_name,
        birth_date=fighter.birth_date,
        weight_class=fighter.weight_class,
        weight=fighter.weight,
        height=fighter.height,
        wins=fighter.wins,
        losses=fighter.losses,
        draws=fighter.draws,
        no_contest=fighter.no_contests
    )

    session.add(payload_fighter)
    session.commit()
    session.refresh(payload_fighter)  # refresh object to get id
    return payload_fighter


# update fighter
@fighters_router.put("/{id}")
def update_fighter(session: SessionDep, id: int, fighter: Fighter):
    if isinstance(fighter.birth_date, str):
        fighter.birth_date = datetime.strptime(fighter.birth_date, "%Y-%m-%d").date()

    existing_fighter = session.query(Fighter).filter(Fighter.id == id).first()
    if not existing_fighter:
        raise HTTPException(status_code=404, detail="fighter not found")

    # update manually the fields. pydantic way
    for key, value in fighter.dict(exclude_unset=True).items():
        setattr(existing_fighter, key, value)

    session.commit()
    session.refresh(existing_fighter)
    return fighter


# delete fighter
@fighters_router.delete("/{id}")
def delete_fighter(session: SessionDep, id: int):
    fighter = session.query(Fighter).filter(Fighter.id == id).first()
    if not fighter:
        raise HTTPException(status_code=404, detail="fighter not found")

    session.delete(fighter)
    session.commit()
    return {"message": "fighter deleted"}
