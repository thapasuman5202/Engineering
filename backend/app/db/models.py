from __future__ import annotations

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, JSON, String, Text, func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    jobs = relationship("Job", back_populates="project", cascade="all, delete-orphan")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(ForeignKey("projects.id"), nullable=False)
    input_data = Column(JSON, nullable=True)
    status = Column(String, nullable=False, server_default="pending")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    project = relationship("Project", back_populates="jobs")
    variants = relationship("Variant", back_populates="job", cascade="all, delete-orphan")


class Variant(Base):
    __tablename__ = "variants"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(ForeignKey("jobs.id"), nullable=False)
    content = Column(JSON, nullable=True)
    score = Column(Float, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    job = relationship("Job", back_populates="variants")
    feedback = relationship("Feedback", back_populates="variant", cascade="all, delete-orphan")


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    variant_id = Column(ForeignKey("variants.id"), nullable=False)
    rating = Column(Integer, nullable=True)
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    variant = relationship("Variant", back_populates="feedback")
    emotion_events = relationship("EmotionEvent", back_populates="feedback", cascade="all, delete-orphan")


class EmotionEvent(Base):
    __tablename__ = "emotion_events"

    id = Column(Integer, primary_key=True, index=True)
    feedback_id = Column(ForeignKey("feedback.id"), nullable=False)
    emotion = Column(String, nullable=False)
    intensity = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    feedback = relationship("Feedback", back_populates="emotion_events")


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(String, primary_key=True, index=True)
    label = Column(String, nullable=False)
    meta = Column("metadata", JSON, nullable=True)
    scores = Column(JSON, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    feedback = relationship("CandidateFeedback", back_populates="candidate", cascade="all, delete-orphan")


class CandidateFeedback(Base):
    __tablename__ = "candidate_feedback"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(ForeignKey("candidates.id"), nullable=False)
    rating = Column(Integer, nullable=True)
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    candidate = relationship("Candidate", back_populates="feedback")
    emotion_events = relationship("CandidateEmotionEvent", back_populates="feedback", cascade="all, delete-orphan")


class CandidateEmotionEvent(Base):
    __tablename__ = "candidate_emotion_events"

    id = Column(Integer, primary_key=True, index=True)
    feedback_id = Column(ForeignKey("candidate_feedback.id"), nullable=False)
    emotion = Column(String, nullable=False)
    intensity = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    feedback = relationship("CandidateFeedback", back_populates="emotion_events")
