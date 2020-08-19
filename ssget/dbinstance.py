'''
The `dbinstance` module creates a singleton `MatrixDB` database instance, populating
it from UFStats.csv if necessary. 
'''
import logging
logger = logging.getLogger(__name__)

from .db import MatrixDB
from . import csvindex


instance = MatrixDB()

if instance.nrows == 0:
    logger.info("Creating index from CSV file...")
    
    instance.insert(csvindex.generate())
