"""user roles

Revision ID: 772691495db1
Revises: 827f75c29143
Create Date: 2026-06-01 16:03:10.537584

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "772691495db1"
down_revision: Union[str, Sequence[str], None] = "827f75c29143"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

user_role = sa.Enum(
    "ADMIN",
    "MANAGER",
    "AGENT",
    "VIEWER",
    name="userrole",
)


def upgrade() -> None:
    user_role.create(op.get_bind())

    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(
            sa.Column(
                "role",
                user_role,
                nullable=False,
                server_default="AGENT",
            )
        )


def downgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_column("role")

    user_role.drop(op.get_bind())
