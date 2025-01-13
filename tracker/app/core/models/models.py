from sqlmodel import SQLModel, Field, UniqueConstraint
from datetime import date, datetime
from pydantic import EmailStr


# class for datetime.date and datetime.datetime pydantic compatibility
class BaseModel(SQLModel):
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            date: lambda v: v.isoformat(),  # serialize date to string
            datetime: lambda v: v.isoformat(),  # serialize datetime to string
        }


class Fighter(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    full_name: str = Field(index=True)
    birth_date: date  # pydantic compatible datetime.date
    weight_class: str | None = Field(index=True)
    weight: float  # weight in lbs
    height: float  # height in feet
    wins: int = Field(default=0)
    losses: int = Field(default=0)
    draws: int = Field(default=0)
    no_contests: int = Field(default=0)


class Fight(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    rounds: int = Field(default=3)
    card_id: int = Field(index=True, foreign_key="card.id")
    red_corner: int = Field(foreign_key="fighter.id", index=True)
    blue_corner: int = Field(foreign_key="fighter.id", index=True)
    winner: int | None = Field(foreign_key="fighter.id", index=True)
    outcome: str | None = Field()  # ko, decision, submission


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: EmailStr = Field(index=True, unique=True)
    password: str  # hashed
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Pick(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, foreign_key="user.id")
    fight_id: int = Field(index=True, foreign_key="fight.id")
    pick: int | None = Field(index=True, foreign_key="fighter.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # prevent a user from making multiple picks for the same fight
    __table_args__ = (UniqueConstraint("user_id", "fight_id", name="unique_user_fight_pick"),)


class Card(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    numbered: bool = Field(default=False)
    name: str = Field(index=True)
    date: date
