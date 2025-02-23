from typing import List, Dict
from pydantic import BaseModel

class LearningProfile(BaseModel):
    skill_level: str
    learning_style: str
    goals: List[str]
    previous_knowledge: Dict[str, str]
    preferred_pace: str

class LearningPlan(BaseModel):
    topics: List[str]
    exercises: List[str]
    timeline: str
    milestones: List[str]
    adaptations: Dict[str, str]