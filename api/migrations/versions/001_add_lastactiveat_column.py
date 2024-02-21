from alembic import op
import sqlalchemy as sa
from datetime import datetime

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('users', sa.Column('lastactiveat', sa.DateTime, nullable=True, default=datetime.utcnow))

def downgrade():
    op.drop_column('users', 'lastactiveat')
