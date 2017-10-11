import datetime
import os

import peewee
from playhouse.db_url import connect


DB = connect(
    os.environ.get(                                         #how to connect the blog database to the server
        'DATABASE_URL',
        'postgres://localhost:5432/Weather'
    )