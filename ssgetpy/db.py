import datetime
import logging

from .config import SS_DB, SS_TABLE
from .matrix import Matrix, MatrixList

logger = logging.getLogger(__name__)


def _from_timestamp(timestamp):
    if hasattr(datetime.datetime, "fromisoformat"):
        return datetime.datetime.fromisoformat(timestamp)
    return datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")


class MatrixDB:
    def __init__(self, db=SS_DB, table=SS_TABLE):
        import sqlite3

        self.db = db
        self.matrix_table = table
        self.update_table = "update_table"
        self.conn = sqlite3.connect(self.db)
        self._create_table()

    def _get_nrows(self):
        return int(
            self.conn.execute(
                "SELECT COUNT(*) FROM %s" % self.matrix_table
            ).fetchall()[0][0]
        )

    nrows = property(_get_nrows)

    def _get_last_update(self):
        last_update = self.conn.execute(
            "SELECT MAX(update_date) " + f"from {self.update_table}"
        ).fetchall()[0][0]
        return (
            _from_timestamp(last_update)
            if last_update
            else datetime.datetime.utcfromtimestamp(0)
        )

    last_update = property(_get_last_update)

    def _drop_table(self):
        self.conn.execute("DROP TABLE IF EXISTS %s" % self.matrix_table)
        self.conn.execute(f"DROP TABLE IF EXISTS {self.update_table}")
        self.conn.commit()

    def _create_table(self):
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS %s (
                             id INTEGER PRIMARY KEY,
                             matrixgroup TEXT,
                             name TEXT,
                             rows INTEGER,
                             cols INTEGER,
                             nnz INTEGER,
                             dtype TEXT,
                             is2d3d INTEGER,
                             isspd INTEGER,
                             psym REAL,
                             nsym REAL,
                             kind TEXT)"""
            % self.matrix_table
        )

        self.conn.execute(
            f"CREATE TABLE IF NOT EXISTS {self.update_table} "
            + "(update_date TIMESTAMP)"
        )
        self.conn.commit()

    def insert(self, values):
        self.conn.executemany(
            "INSERT INTO %s VALUES(?,?,?,?,?,?,?,?,?,?,?,?)"
            % self.matrix_table,
            values,
        )
        self.conn.execute(
            f"INSERT INTO {self.update_table} " + "VALUES (datetime('now'))"
        )
        self.conn.commit()

    def refresh(self, values):
        self._drop_table()
        self._create_table()
        self.insert(values)

    def dump(self):
        return self.conn.execute(
            "SELECT * from %s" % self.matrix_table
        ).fetchall()

    @staticmethod
    def _is_constraint(field, value):
        return value and "(%s = '%s')" % (field, value)

    @staticmethod
    def _like_constraint(field, value):
        return value and "(%s LIKE '%%%s%%')" % (field, value)

    @staticmethod
    def _sz_constraint(field, bounds):
        if bounds is None or (bounds[0] is None and bounds[1] is None):
            return None
        constraints = []
        if bounds[0] is not None:
            constraints.append("%s >= %d" % (field, bounds[0]))
        if bounds[1] is not None:
            constraints.append("%s <= %d" % (field, bounds[1]))
        return " ( " + " AND ".join(constraints) + " ) "

    @staticmethod
    def _bool_constraint(field, value):
        if value is None:
            return None
        elif value:
            return "(%s = 1)" % field
        else:
            return "(%s = 0)" % field

    def search(
        self,
        matid=None,
        group=None,
        name=None,
        rowbounds=None,
        colbounds=None,
        nzbounds=None,
        dtype=None,
        is2d3d=None,
        isspd=None,
        kind=None,
        limit=10,
    ):

        querystring = "SELECT * FROM %s" % self.matrix_table

        mid_constraint = MatrixDB._is_constraint("id", matid)
        grp_constraint = MatrixDB._is_constraint("matrixgroup", group)
        nam_constraint = MatrixDB._like_constraint("name", name)
        row_constraint = MatrixDB._sz_constraint("rows", rowbounds)
        col_constraint = MatrixDB._sz_constraint("cols", colbounds)
        nnz_constraint = MatrixDB._sz_constraint("nnz", nzbounds)
        dty_constraint = MatrixDB._is_constraint("dtype", dtype)
        geo_constraint = MatrixDB._bool_constraint("is2d3d", is2d3d)
        spd_constraint = MatrixDB._bool_constraint("isspd", isspd)
        knd_constraint = MatrixDB._like_constraint("kind", kind)

        constraints = list(
            filter(
                lambda x: x is not None,
                (
                    mid_constraint,
                    grp_constraint,
                    nam_constraint,
                    row_constraint,
                    col_constraint,
                    nnz_constraint,
                    dty_constraint,
                    geo_constraint,
                    spd_constraint,
                    knd_constraint,
                ),
            )
        )

        if any(constraints):
            querystring += " WHERE " + " AND ".join(constraints)

        querystring += " LIMIT (%s)" % limit

        logger.debug(querystring)

        return MatrixList(
            Matrix(*x) for x in self.conn.execute(querystring).fetchall()
        )
