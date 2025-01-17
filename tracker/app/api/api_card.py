from fastapi import APIRouter, HTTPException
from app.db.database import SessionDep
from app.core.models.models import Card
from datetime import datetime

cards_router = APIRouter(prefix="/cards", tags=["cards"])

@cards_router.get("/")
def get_cards(session: SessionDep):
    cards = session.query(Card).all()
    return cards


@cards_router.get("/numerated")
def get_cards_numerated(session: SessionDep):
    cards = session.query(Card).filter(Card.numbered.is_(True)).all()
    return cards


@cards_router.get("/{id}")
def get_card(id: int, session: SessionDep):
    card = session.query(Card).filter(Card.id == id).first()
    if not card:
        raise HTTPException(status_code=404, detail="card not found")
    return card


@cards_router.post("/")
def create_card(card: Card, session: SessionDep):
    # cast the date from string to datetype
    if isinstance(card.date, str):
        card.date = datetime.strptime(card.date, "%Y-%m-%d").date()

    # json card
    payload_card = Card(
        name=card.name,
        numbered=card.numbered,
        date=card.date,
    )

    session.add(payload_card)
    session.commit()
    session.refresh(payload_card)
    return payload_card


@cards_router.put("/{id}")
def update_card(id: int, card: Card, session: SessionDep):
    if isinstance(card.date, str):
        card.date = datetime.strptime(card.date, "%Y-%m-%d").date()

    existing_card = session.query(Card).filter(Card.id == id).first()
    if not existing_card:
        raise HTTPException(status_code=404, detail="card not found")

    for key, value in card.dict(exclude_unset=True).items():
        setattr(existing_card, key, value)

    session.commit()
    session.refresh(existing_card)
    return existing_card


@cards_router.delete("/{id}")
def delete_card(id: int, session: SessionDep):
    card = session.query(Card).filter(Card.id == id).first()
    if not card:
        raise HTTPException(status_code=404, detail="card not found")

    session.delete(card)
    session.commit()
    return {"message": "card deleted"}
