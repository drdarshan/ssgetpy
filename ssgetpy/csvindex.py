"""
The `csvindex` module parses the SSStats.csv file and
generates entries for each row in a Matrix database
"""

import csv
import logging

import requests

from .config import SS_INDEX_URL

logger = logging.getLogger(__name__)


def getdtype(real, logical):
    """
    Converts a (real, logical) pair into one of the three types:
    'real', 'complex' and 'binary'
    """
    return "binary" if logical else ("real" if real else "complex")


def gen_rows(csvrows):
    """
    Creates a generator that returns a single row in the matrix database.
    """
    reader = csv.reader(csvrows)
    matid = 0
    for line in reader:
        matid += 1
        group = line[0]
        name = line[1]
        rows = int(line[2])
        cols = int(line[3])
        nnz = int(line[4])
        real = bool(int(line[5]))
        logical = bool(int(line[6]))
        is2d3d = bool(int(line[7]))
        isspd = bool(int(line[8]))
        psym = float(line[9])
        nsym = float(line[10])
        kind = line[11]
        yield matid, group, name, rows, cols, nnz, getdtype(
            real, logical
        ), is2d3d, isspd, psym, nsym, kind


def generate():
    response = requests.get(SS_INDEX_URL)
    lines = response.iter_lines()

    # Read the number of entries
    logger.info(f"Number of entries in the CSV file: {next(lines)}")
    # Read the last modified date
    logger.info(f"Last modified date: {next(lines)}")

    return gen_rows(line.decode("utf-8") for line in lines)
