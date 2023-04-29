from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
alembic_version = Table('alembic_version', pre_meta,
    Column('version_num', VARCHAR(length=32), primary_key=True, nullable=False),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=64)),
    Column('email', String(length=120)),
    Column('password_hash', String(length=128)),
    Column('about_me', String(length=140)),
    Column('last_seen', DateTime, default=ColumnDefault(<function datetime.utcnow at 0x000001EFEAE83880>)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['alembic_version'].drop()
    post_meta.tables['user'].columns['about_me'].create()
    post_meta.tables['user'].columns['last_seen'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['alembic_version'].create()
    post_meta.tables['user'].columns['about_me'].drop()
    post_meta.tables['user'].columns['last_seen'].drop()
