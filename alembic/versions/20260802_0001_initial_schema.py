"""initial schema: users and tasks

Revision ID: 20260802_0001
Revises:
Create Date: 2026-08-02

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20260802_0001"
down_revision = None
branch_labels = None
depends_on = None

task_status_enum = sa.Enum("todo", "in_progress", "done", name="taskstatus")


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    task_status_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", task_status_enum, nullable=False, server_default="todo"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("owner_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("tasks")
    task_status_enum.drop(op.get_bind(), checkfirst=True)
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
