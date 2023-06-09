from pydantic import BaseModel
from datetime import date


class Result(BaseModel):
    # id: int
    event: str
    gender: str | None = None
    clas_s: str | None = None
    heat: str | None = None
    typ: str | None = None
    wind: str | None = None
    name: str | None = None
    year: str | None = None
    position: str | None = None
    school: str | None = None
    mark: str | None = None
    points: str | None = None


class Record(BaseModel):
    id: int
    mark: str
    athlete: str
    year: int


class Event(BaseModel):
    id: int
    name: str
    record: Record


class Athlete(BaseModel):
    id: int
    firstname: str
    lastname: str
    dob: date | None = None
    events: list[str] = []
    gender: str
