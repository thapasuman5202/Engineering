from __future__ import annotations

import asyncio
import random
from dataclasses import dataclass
from typing import Dict, List, Protocol
from uuid import uuid4

from pydantic import BaseModel

from app.models import SiteContext, Weights, VariantOut, FeedbackIn
from app.db.session import SessionLocal
from app.db.models import (
    Base,
    Candidate as DBCandidate,
    CandidateFeedback,
    CandidateEmotionEvent,
)


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
    """Mutable state shared across rounds of generation."""

    context: SiteContext | None = None
    feedback: List[FeedbackIn] = []
    emotion_stats: Dict[str, float] = {}
    seed: int = 0
    candidates: List[Candidate] = []


class Agent(Protocol):
    name: str

    async def propose(self, state: DesignState) -> Proposal:
        ...


class AestheticsAgent:
    name = "aesthetics"

    async def propose(self, state: DesignState) -> Proposal:
        await asyncio.sleep(0)
        color = random.choice(["red", "blue", "green"])
        return Proposal(type=self.name, data={"color": color})


class SustainabilityAgent:
    name = "sustainability"

    async def propose(self, state: DesignState) -> Proposal:
        await asyncio.sleep(0)
        system = random.choice(["solar", "geothermal"])
        return Proposal(type=self.name, data={"energy": system})


class CostAgent:
    name = "cost"

    async def propose(self, state: DesignState) -> Proposal:
        await asyncio.sleep(0)
        level = random.choice(["low", "medium", "high"])
        return Proposal(type=self.name, data={"cost_level": level})


class AccessibilityAgent:
    name = "accessibility"

    async def propose(self, state: DesignState) -> Proposal:
        await asyncio.sleep(0)
        feature = random.choice(["ramp", "elevator"])
        return Proposal(type=self.name, data={"feature": feature})


class StructuralAgent:
    name = "structural"

    async def propose(self, state: DesignState) -> Proposal:
        await asyncio.sleep(0)
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

    session = SessionLocal()
    # Ensure tables exist for candidate persistence
    engine = session.get_bind()
    Base.metadata.create_all(
        bind=engine,
        tables=[
            DBCandidate.__table__,
            CandidateFeedback.__table__,
            CandidateEmotionEvent.__table__,
        ],
    )
    variants: List[VariantOut] = []

    async def generate_round() -> VariantOut:
        # gather proposals concurrently
        proposals = await asyncio.gather(*(a.propose(state) for a in agents))
        candidate = Synthesizer.merge(list(proposals), state)
        Critic.review(candidate, state)
        scores = score_candidate(candidate, weights)
        state.candidates.append(candidate)

        # persist candidate
        db_cand = DBCandidate(
            id=candidate.id,
            label=candidate.label,
            meta=candidate.metadata,
            scores=scores,
        )
        session.add(db_cand)
        session.commit()

        return VariantOut(
            id=candidate.id,
            label=candidate.label,
            metadata=candidate.metadata,
            score=scores,
            rank=0,
            assets=[],
        )

    async def run_loop():
        for _ in range(n):
            variant = await generate_round()
            variants.append(variant)

    asyncio.run(run_loop())
    session.close()

    variants.sort(key=lambda v: v.score.get("composite", 0), reverse=True)
    for idx, v in enumerate(variants, start=1):
        v.rank = idx
    return variants
