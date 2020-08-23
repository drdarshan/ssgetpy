import logging
import os
import sys

logger = logging.getLogger(__name__)

SS_DIR = None
SS_DB = "index.db"
SS_TABLE = "MATRICES"
SS_ROOT_URL = "https://sparse.tamu.edu"
SS_INDEX_URL = "/".join((SS_ROOT_URL, "files", "ssstats.csv"))

if sys.platform == "win32":
    SS_DIR = os.path.join(os.environ["APPDATA"], "ssgetpy")
else:
    SS_DIR = os.path.join(os.environ["HOME"], ".ssgetpy")

SS_DB = os.path.join(SS_DIR, SS_DB)

os.makedirs(SS_DIR, exist_ok=True)


def dump():
    logger.debug(
        dict(
            SS_DIR=SS_DIR,
            SS_DB=SS_DB,
            SS_TABLE=SS_TABLE,
            SS_ROOT_URL=SS_ROOT_URL,
            SS_INDEX_URL=SS_INDEX_URL,
        )
    )
