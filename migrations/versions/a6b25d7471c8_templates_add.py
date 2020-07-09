"""templates_add

Revision ID: a6b25d7471c8
Revises: 4f11161cb5a8
Create Date: 2020-07-04 11:16:44.593980

"""
from alembic import op
import sqlalchemy as sa

from yacht import db
from yacht.api.docker.models import Template


# revision identifiers, used by Alembic.
revision = 'a6b25d7471c8'
down_revision = 'ffb46bba46c4'
branch_labels = None
depends_on = None


def upgrade():
    # push to new revision
    templ = Template(
        title='Untitled Template',
        url='https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Template/template.json')
    db.session.add(templ)
    db.session.commit()


def downgrade():
    Template.query.delete()
    db.session.commit()
