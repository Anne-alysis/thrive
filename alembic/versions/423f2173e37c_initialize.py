"""initialize

Revision ID: 423f2173e37c
Revises: 
Create Date: 2025-04-12 15:14:03.691261

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '423f2173e37c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""CREATE extension if NOT EXISTS "uuid-ossp";""")

    op.execute("""CREATE SCHEMA thrive_user;""")
    op.execute("""CREATE SCHEMA incident;""")

    op.execute("""
        CREATE TABLE thrive_user.user
        (
            user_id             serial primary key,
            first_name          character varying,
            last_name           character varying,
            signup_at           timestamp with time zone not null,
            last_activity_at    timestamp with time zone not null,
            thrive_created_dtm  timestamp with time zone not null,
            thrive_modified_dtm timestamp with time zone not null
        )
    """)

    op.execute("""
        CREATE TABLE thrive_user.activity
        (
            user_id     integer,
            activity_at timestamp with time zone not null,
            activity    character varying        not null
        )
    """)

    op.execute ("""
        CREATE TABLE incident.incident
        (
            incident_id         uuid                     not null primary key default uuid_generate_v4(),
            user_id             integer                  not null,
            incident_at         timestamp with time zone,
            category            character varying,
            sub_category        character varying,
            description         character varying,
            thrive_created_dtm  timestamp with time zone not null,
            thrive_modified_dtm timestamp with time zone not null
        );
    """)

    # normally, these would probably be normalized in some way with keys instead of text, but this is just a sample
    op.execute("""
        CREATE TABLE incident.category
        (
            category            character varying not null,
            sub_category        character varying not null,
            description         character varying,
            thrive_created_dtm  timestamp with time zone not null,
            thrive_modified_dtm timestamp with time zone not null
        )
    """)



def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""DROP SCHEMA incident CASCADE;""")
    op.execute("""DROP SCHEMA thrive_user CASCADE;""")

