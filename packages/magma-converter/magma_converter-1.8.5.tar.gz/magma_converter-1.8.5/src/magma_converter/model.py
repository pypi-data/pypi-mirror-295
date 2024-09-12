from playhouse.migrate import *
from .config import config
import os
import datetime


def database(db_name: str = 'magma.db') -> str:
    """Database location

    Args:
        db_name: database name. Default magma.db

    Returns:
        str: Database location
    """
    database_dir = config['DATABASE_LOCATION']
    if not os.path.isdir(database_dir):
        os.makedirs(database_dir)
    return os.path.join(database_dir, db_name)


db = SqliteDatabase(database=database(), pragmas={
    'foreign_keys': 1,
    'journal_mode': 'wal',
    'cache_size': -32 * 1000
})


class MagmaBaseModel(Model):
    created_at = DateTimeField(default=datetime.datetime.now(tz=datetime.timezone.utc))
    updated_at = DateTimeField(default=datetime.datetime.now(tz=datetime.timezone.utc))

    class Meta:
        database = db


class Station(MagmaBaseModel):
    nslc = CharField(index=True, unique=True, max_length=14)
    network = CharField(index=True)
    station = CharField(index=True)
    channel = CharField(index=True)
    location = CharField()

    class Meta:
        table_name = 'stations'


class Sds(MagmaBaseModel):
    nslc = ForeignKeyField(Station, field='nslc', backref='sds')
    date = DateField(index=True)
    start_time = DateTimeField(index=True, null=True)
    end_time = DateTimeField(index=True, null=True)
    completeness = FloatField()
    sampling_rate = FloatField()
    file_location = CharField()
    file_size = BigIntegerField()

    class Meta:
        table_name = 'sds'
        indexes = (
            (('nslc', 'date'), True),
        )
