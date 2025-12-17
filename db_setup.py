import os
from sqlmodel import Field, Relationship, UniqueConstraint, SQLModel, create_engine
from dotenv import load_dotenv
from datetime import date, datetime

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("No DATABASE_URL found! Did you create the .env file?")

engine = create_engine(DATABASE_URL, echo=True)

class Game(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    date_added: date
    start_date: date
    url: str
    price: int
    listed_odds: float
    top_prize: float

    start_prize_ct: int
    start_prize_sum: float
    start_tic_ct: int

    start_top_pz_ct: int

    start_odds_win: float
    start_odds_profit: float

    start_ev: float
    start_net_ev: float
    start_adj_ev: float

    snapshots: list["Snapshot"] = Relationship(back_populates="game", cascade_delete=True)

class Snapshot(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    gid: int = Field(index=True, foreign_key="game.id")
    timestamp: datetime

    cur_odds_win: float
    cur_odds_profit: float

    cur_unclaim_win_ct: int
    cur_claim_win_ct: int
    cur_prize_sum: float

    cur_top_pz_ct: int
    top_pz_percent_remaining: float

    num_tix_bought: int
    num_tix_left: int
    percent_tix_sold: float
    percent_tix_left: float

    ev_now: float
    ev_net_now: float
    ev_adj_now: float
    ev_lift: float

    jp_rich: float

    game: Game = Relationship(back_populates="snapshots")
    prizes: list["Prize"] | None = Relationship(back_populates="snapshot", cascade_delete=True)


class Prize(SQLModel, table=True):
    __table_args__ = ( # table args lets us pass arguments to the Table constructor with sqlAlchemy
        UniqueConstraint("sid", "value", name="unique_prize_per_snap"),
    )

    id: int | None = Field(default=None, primary_key=True)
    sid: int = Field(index=True, foreign_key="snapshot.id")
    value: float
    start_ct: int
    unclaimed_ct: int
    start_odds: float
    cur_odds: float
    depletion_rate: float
    depletion_prop: float
    ev_start: float
    ev_now: float

    snapshot: Snapshot = Relationship(back_populates="prizes")


def create_tables():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_tables()

