"""users add

Revision ID: 818196691937
Revises: 6db5a6ca7997
Create Date: 2020-07-12 12:11:34.144960

"""
from alembic import op
import sqlalchemy as sa


from yacht import db
from yacht.api.models import User

# revision identifiers, used by Alembic.
revision = '818196691937'
down_revision = '6db5a6ca7997'
branch_labels = None
depends_on = None


def upgrade():
    user = User(
        username='user',
        password='pass')
    db.session.add(user)
    db.session.commit()


def downgrade():
    User.query.delete()
    db.session.commit()
