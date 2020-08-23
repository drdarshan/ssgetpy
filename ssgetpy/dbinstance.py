'''
The `dbinstance` module creates a singleton `MatrixDB` database instance, populating
it from UFStats.csv if necessary. 
'''
import datetime
import logging
logger = logging.getLogger(__name__)

from .db import MatrixDB
from . import csvindex


instance = MatrixDB()

if instance.nrows == 0 or \
   (datetime.datetime.utcnow() - instance.last_update) > datetime.timedelta(days=90):
    logger.info("{Re}creating index from CSV file...")
    instance.refresh(csvindex.generate())
