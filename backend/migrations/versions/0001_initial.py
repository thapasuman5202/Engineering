from __future__ import annotations

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "jobs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("project_id", sa.Integer(), sa.ForeignKey("projects.id"), nullable=False),
        sa.Column("input_data", sa.JSON(), nullable=True),
        sa.Column("status", sa.String(), server_default="pending", nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "variants",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("job_id", sa.Integer(), sa.ForeignKey("jobs.id"), nullable=False),
        sa.Column("content", sa.JSON(), nullable=True),
        sa.Column("score", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "feedback",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("variant_id", sa.Integer(), sa.ForeignKey("variants.id"), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=True),
        sa.Column("comments", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "emotion_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("feedback_id", sa.Integer(), sa.ForeignKey("feedback.id"), nullable=False),
        sa.Column("emotion", sa.String(), nullable=False),
        sa.Column("intensity", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("emotion_events")
    op.drop_table("feedback")
    op.drop_table("variants")
    op.drop_table("jobs")
    op.drop_table("projects")
