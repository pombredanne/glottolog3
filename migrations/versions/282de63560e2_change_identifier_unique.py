# coding=utf-8
"""change identifier unique

Revision ID: 282de63560e2
Revises: d262a0299e2
Create Date: 2014-10-28 11:54:43.489000

"""

# revision identifiers, used by Alembic.

revision = '282de63560e2'
down_revision = 'd262a0299e2'

import datetime

from alembic import op
import sqlalchemy as sa

TABLE = 'identifier'
OLD = ['name', 'type', 'description']
NEW = ['name', 'type', 'description', 'lang']


def replace_unique(table, before, after):
    conn = op.get_bind()

    select_name = sa.text('SELECT c.conname FROM pg_constraint AS c '
        'JOIN pg_class AS r ON r.oid = c.conrelid '
        'WHERE r.relname = :table '
        'AND pg_get_constraintdef(c.oid) = :definition', conn)

    before_name = select_name.scalar(table=table,
        definition='UNIQUE (%s)' % ', '.join(before))

    if before_name:
        op.drop_constraint(before_name, table)

    has_after = select_name.scalar(table=table,
        definition='UNIQUE (%s)' % ', '.join(after))

    if not has_after:
        after_name = '%s_%s_key' % (table, '_'.join(after))
        op.create_unique_constraint(after_name, table, after)


def upgrade():
    replace_unique(TABLE, OLD, NEW)
    
    
def downgrade():
    replace_unique(TABLE, NEW, OLD)

