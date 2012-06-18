import os, sys
UF_DIR = None
UF_DB  = "index.db"
UF_TABLE = "MATRICES"
UF_ROOT_URL = "http://www.cise.ufl.edu/research/sparse"
UF_INDEX_URL = "/".join((UF_ROOT_URL, "mat", "UFget", "matrices", "UFstats.csv"))

if sys.platform == "win32":
    UF_DIR = os.path.join(os.environ["APPDATA"], "PyUFGet")
else:
    UF_DIR = os.path.join(os.environ["HOME"], ".PyUFGet")

UF_DB = os.path.join(UF_DIR, UF_DB)

if not os.access(UF_DIR, os.R_OK | os.W_OK):
    os.makedirs(UF_DIR)

def dump():
    import logging
    logging.debug(dict(UF_DIR=UF_DIR, UF_DB=UF_DB, UF_TABLE=UF_TABLE, UF_ROOT_URL=UF_ROOT_URL, UF_INDEX_URL=UF_INDEX_URL))



