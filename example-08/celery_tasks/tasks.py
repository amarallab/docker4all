import celery
from dataclasses import dataclass
from typing import List

@dataclass
class ClassHolder():
    name: str
    tasks: List[celery.Task]