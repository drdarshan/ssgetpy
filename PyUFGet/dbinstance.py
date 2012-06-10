'''
The `dbinstance` module creates a singleton `MatrixDB` database instance, populating
it from UFStats.csv if necessary. 
'''
from db import MatrixDB

instance = MatrixDB()

if instance.nrows == 0:
    import logging
    logging.info("Creating index from CSV file...")
    
    import csvindex
    instance.insert(csvindex.generate())
