from pydantic import BaseModel
from datetime import date


class TrackEvents(BaseModel):
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


class FieldEvents(BaseModel):
    # id: int
    event: str
    gender: str | None = None
    clas_s: str | None = None
    typ: str | None = None
    wind: str | None = None
    name: str | None = None
    year: str | None = None
    position: str | None = None
    school: str | None = None
    series: list | None = None
    mark: str | None = None
    points: str | None = None


class MultiEvent(BaseModel):
    # id: int
    event: str
    gender: str | None = None
    clas_s: str | None = None
    typ: str | None = None
    name: str | None = None
    year: str | None = None
    position: str | None = None
    school: str | None = None
    mark: str | None = None
    points: str | None = None


class Record(BaseModel):
    event: str
    gender: str
    clas_s: str
    mark: str
    athlete: str
    year: str
    school: str


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
