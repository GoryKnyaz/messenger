from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
alembic_version = Table('alembic_version', pre_meta,
    Column('version_num', VARCHAR(length=32), primary_key=True, nullable=False),
)

followers = Table('followers', post_meta,
    Column('follower_id', Integer),
    Column('followed_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['alembic_version'].drop()
    post_meta.tables['followers'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['alembic_version'].create()
    post_meta.tables['followers'].drop()
