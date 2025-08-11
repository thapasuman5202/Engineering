from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Dict, List, Protocol
from uuid import uuid4

from pydantic import BaseModel

from app.models import SiteContext, Weights, VariantOut


@dataclass
class Proposal:
    type: str
    data: Dict[str, str]


@dataclass
class Candidate:
    id: str
    label: str
    metadata: Dict[str, str]


class DesignState(BaseModel):
    site: SiteContext | None = None
    seed: int = 0
    candidates: List[Candidate] = []


class Agent(Protocol):
    name: str

    def propose(self, state: DesignState) -> Proposal:
        ...


class AestheticsAgent:
    name = "aesthetics"

    def propose(self, state: DesignState) -> Proposal:
        color = random.choice(["red", "blue", "green"])
        return Proposal(type=self.name, data={"color": color})


class SustainabilityAgent:
    name = "sustainability"

    def propose(self, state: DesignState) -> Proposal:
        system = random.choice(["solar", "geothermal"])
        return Proposal(type=self.name, data={"energy": system})


class CostAgent:
    name = "cost"

    def propose(self, state: DesignState) -> Proposal:
        level = random.choice(["low", "medium", "high"])
        return Proposal(type=self.name, data={"cost_level": level})


class AccessibilityAgent:
    name = "accessibility"

    def propose(self, state: DesignState) -> Proposal:
        feature = random.choice(["ramp", "elevator"])
        return Proposal(type=self.name, data={"feature": feature})


class StructuralAgent:
    name = "structural"

    def propose(self, state: DesignState) -> Proposal:
        system = random.choice(["steel", "timber"])
        return Proposal(type=self.name, data={"structure": system})


class Synthesizer:
    @staticmethod
    def merge(proposals: List[Proposal], state: DesignState) -> Candidate:
        meta: Dict[str, str] = {}
        for p in proposals:
            meta.update(p.data)
        label = "_".join(f"{k}:{v}" for k, v in meta.items())
        return Candidate(id=str(uuid4()), label=label, metadata=meta)


class Critic:
    @staticmethod
    def review(candidate: Candidate, state: DesignState) -> List[str]:
        return []


def score_candidate(candidate: Candidate, weights: Weights) -> Dict[str, float]:
    # simple random scores for demonstration
    scores = {
        "aesthetic": random.random(),
        "sustainability": random.random(),
        "cost": random.random(),
        "accessibility": random.random(),
        "emotion": random.random(),
    }
    scores["composite"] = sum(scores[k] * getattr(weights, k) for k in weights.model_fields)
    return scores


def run_generation(n: int, weights: Weights) -> List[VariantOut]:
    state = DesignState()
    agents: List[Agent] = [
        AestheticsAgent(),
        SustainabilityAgent(),
        CostAgent(),
        AccessibilityAgent(),
        StructuralAgent(),
    ]

    variants: List[VariantOut] = []
    for _ in range(n):
        proposals = [a.propose(state) for a in agents]
        candidate = Synthesizer.merge(proposals, state)
        scores = score_candidate(candidate, weights)
        variant = VariantOut(
            id=candidate.id,
            label=candidate.label,
            metadata=candidate.metadata,
            score=scores,
            rank=0,
            assets=[],
        )
        variants.append(variant)
    # assign ranks based on composite score
    variants.sort(key=lambda v: v.score.get("composite", 0), reverse=True)
    for idx, v in enumerate(variants, start=1):
        v.rank = idx
    return variants
