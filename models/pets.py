from dataclasses import dataclass
from typing import List

@dataclass
class Category:
    id: int
    name: str

@dataclass
class Tag:
    id: int
    name: str

@dataclass
class Pet:
    id: int
    category: Category
    name: str
    photoUrls: List[str]
    tags: List[Tag]
    status: str
