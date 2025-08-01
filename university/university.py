from dataclasses import dataclass


@dataclass
class Speciality:
    id: str
    name: str
    url: str


@dataclass
class University:
    id: str
    name: str
    specialties: dict
