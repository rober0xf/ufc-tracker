from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_session
from app.core.models.models import Pick

picks_router = APIRouter(prefix="/picks", tags=["picks"])

@picks_router.get("/{id}")
def get_pick(id: int, session: Session = Depends(get_session)):
    pick = session.query(Pick).filter(Pick.id == id).first()
    if not pick:
        raise HTTPException(status_code=404, detail="pick not found")
    return pick


@picks_router.post("/")
def create_pick(pick: Pick, session: Session = Depends(get_session)):
    payload_pick = Pick(
        pick=pick.pick,
        user_id=pick.user_id,
        fight_id=pick.fight_id
    )
    session.add(payload_pick)
    session.commit()
    session.refresh(payload_pick)
    return payload_pick


@picks_router.put("/{id}")
def update_pick(id: int, pick: Pick, session: Session = Depends(get_session)):
    existing_pick = session.query(Pick).filter(Pick.id == id).first()
    if not existing_pick:
        raise HTTPException(status_code=404, detail="pick not found")

    for key, value in pick.dict(exclude={"id"}, exclude_unset=True).items():
        setattr(existing_pick, key, value)

    session.commit()
    session.refresh(existing_pick)
    return existing_pick


@picks_router.delete("/{id}")
def delete_pick(id: int, session: Session = Depends(get_session)):
    pick = session.query(Pick).filter(Pick.id == id).first()
    if not pick:
        raise HTTPException(status_code=404, detail="pick not found")
    session.delete(pick)
    session.commit()
    return {"message": "pick deleted"}
