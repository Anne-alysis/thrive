"""split out categories

Revision ID: c2ec24b0b990
Revises: 423f2173e37c
Create Date: 2025-04-21 21:44:21.867102

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2ec24b0b990'
down_revision: Union[str, None] = '423f2173e37c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        CREATE TABLE incident.incident_category
        (
            incident_id         uuid,
            category            character varying,
            subcategory         character varying,
            thrive_created_dtm  timestamp with time zone not null default now(),
            thrive_modified_dtm timestamp with time zone not null default now()
        )
    """)

    op.execute("CREATE UNIQUE INDEX on incident.incident_category (incident_id, subcategory)")

    op.execute("""
        ALTER TABLE incident.incident 
        DROP COLUMN category, 
        DROP COLUMN subcategory;
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""DROP TABLE incident.incident_category;""")
    op.execute("""
        ALTER TABLE incident.incident 
            ADD COLUMN category character varying, 
            ADD COLUMN subcategory character varying;
    """)
