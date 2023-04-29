#!flask/bin/python
import imp
# import importlib.util
from migrate.versioning import api
from app import db
from config import Config

migration = Config.SQLALCHEMY_MIGRATE_REPO + '\\versions\\%03d_migration.py' % (
        api.db_version(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_REPO) + 1)
tmp_module = imp.new_module('old_model')
# tmp_spec = importlib.util.find_spec('old_model')
# tmp_module = importlib.util.module_from_spec(tmp_spec)
old_model = api.create_model(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_REPO)
exec(old_model, tmp_module.__dict__)
script = api.make_update_script_for_model(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_REPO,
                                          tmp_module.meta, db.metadata)
open(migration, "wt").write(script)
api.upgrade(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_REPO)
print('New migration saved as ' + migration)
print(
    'Current database version: ' + str(api.db_version(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_REPO)))
