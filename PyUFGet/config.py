import os, sys, logging
UF_DIR = None
UF_DB  = "index.db"
UF_TABLE = "MATRICES"
UF_ROOT_URL = "http://www.cise.ufl.edu/research/sparse"
UF_INDEX_URL = "/".join((UF_ROOT_URL, "mat", "UFget", "matrices", "UFstats.csv"))

if sys.platform == "win32":
    UF_DIR = os.path.join(os.environ["APPDATA"], "PyUFGet")
elif sys.platform == "darwin":
    UF_DIR = os.path.join(os.environ["HOME"], ".PyUFGet")
else:
    UF_DIR = os.path.join("/tmp", "PyUfGet")

UF_DB = os.path.join(UF_DIR, UF_DB)

if not os.access(UF_DIR, os.R_OK | os.W_OK):
    os.makedirs(UF_DIR)

logging.debug("UF_DIR = %s, UF_DB = %s, UF_TABLE = %s, UF_ROOT_URL = %s, UF_INDEX_URL = %s" % (UF_DIR, UF_DB, UF_TABLE, UF_ROOT_URL, UF_INDEX_URL))



