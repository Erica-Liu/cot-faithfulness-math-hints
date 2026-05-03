from dataclasses import dataclass


@dataclass(frozen=True)
class Problem:
    id: str
    domain: str
    problem: str
    correct_answer: str
    misleading_answer: str
    notes: str = ""


CONDITIONS = ["baseline", "correct_hint", "misleading_hint"]
