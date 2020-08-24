"""
The `dbinstance` module creates a singleton `MatrixDB` database
instance, populating it from ssstats.csv if necessary.
"""
import datetime
import logging

from . import csvindex
from .db import MatrixDB

logger = logging.getLogger(__name__)


instance = MatrixDB()

if instance.nrows == 0 or (
    datetime.datetime.utcnow() - instance.last_update
) > datetime.timedelta(days=90):
    logger.info("{Re}creating index from CSV file...")
    instance.refresh(csvindex.generate())
