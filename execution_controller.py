"""
Ensures only safety-approved actions execute.
"""

from safety_layer import enforce


def execute(action: dict, fn):
    decision = enforce(action)

    if decision == "BLOCK":
        return {"status": "blocked"}

    if decision == "REVIEW":
        return {"status": "requires_human_review"}

    return fn()
