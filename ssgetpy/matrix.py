import os
import time

import requests
from tqdm.auto import tqdm

from . import bundle
from .config import SS_DIR, SS_ROOT_URL


class MatrixList(list):
    def _repr_html_(self):
        body = "".join(r.to_html_row() for r in self)
        return f"<table>{Matrix.html_header()}<tbody>{body}</tbody></table>"

    def __getitem__(self, expr):
        result = super().__getitem__(expr)
        return MatrixList(result) if isinstance(expr, slice) else result

    def download(self, format="MM", destpath=None, extract=False):
        with tqdm(total=len(self), desc="Overall progress") as pbar:
            for matrix in self:
                matrix.download(format, destpath, extract)
                pbar.update(1)


class Matrix:
    """
    A `Matrix` object represents an entry in the SuiteSparse matrix collection.
    It has the following attributes:
    `id`   : The unique identifier for the matrix in the database.
    `group`: The name of the group this matrix belongs to.
    `name` : The name of this matrix.
    `rows` : The number of rows.
    `cols` : The number of columns.
    `nnz`  : The number of non-zero elements.
    `dtype`: The datatype of non-zero elements: `real`, `complex` or `binary`
    `is2d3d`: True if this matrix comes from a 2D or 3D discretization.
    `isspd` : True if this matrix is symmetric, positive definite
    `kind`  : The underlying problem domain
    """

    attr_list = [
        "Id",
        "Group",
        "Name",
        "Rows",
        "Cols",
        "NNZ",
        "DType",
        "2D/3D Discretization?",
        "SPD?",
        "Pattern Symmetry",
        "Numerical Symmetry",
        "Kind",
        "Spy Plot",
    ]

    @staticmethod
    def html_header():
        return (
            "<thead>"
            + "".join(f"<th>{attr}</th>" for attr in Matrix.attr_list)
            + "</thead>"
        )

    def __init__(
        self,
        identifier,
        group,
        name,
        rows,
        cols,
        nnz,
        dtype,
        is2d3d,
        isspd,
        psym,
        nsym,
        kind,
    ):
        self.id = identifier
        self.group = group
        self.name = name
        self.rows = rows
        self.cols = cols
        self.nnz = nnz
        self.dtype = dtype
        self.is2d3d = not not is2d3d
        self.isspd = not not isspd
        self.psym = psym
        self.nsym = nsym
        self.kind = kind

    def to_tuple(self):
        """
        Returns the fields in a `Matrix` instance in a tuple.
        """
        return (
            self.id,
            self.group,
            self.name,
            self.rows,
            self.cols,
            self.nnz,
            self.dtype,
            self.is2d3d,
            self.isspd,
            self.psym,
            self.nsym,
            self.kind,
            self.icon_url(),
        )

    def _render_item_html(self, key, value):
        if key == "Spy Plot":
            return f'<img src="{value}">'
        if key == "Group":
            return f'<a href="{self.group_info_url()}" target="_blank">{value}</a>'
        if key == "Name":
            return f'<a href="{self.matrix_info_url()}" target="_blank">{value}</a>'
        if key in ("Pattern Symmetry", "Numerical Symmetry"):
            return f"{value:0.2}"
        if key in ("2D/3D Discretization?", "SPD?"):
            return "Yes" if value else "No"

        return str(value)

    def to_html_row(self):
        return (
            "<tr>"
            + "".join(
                f"<td>{self._render_item_html(key, value)}</td>"
                for key, value in zip(Matrix.attr_list, self.to_tuple())
            )
            + "</tr>"
        )

    def _filename(self, format="MM"):
        if format == "MM" or format == "RB":
            return self.name + ".tar.gz"
        elif format == "MAT":
            return self.name + ".mat"
        else:
            raise ValueError("Format must be 'MM', 'MAT' or 'RB'")

    def _defaultdestpath(self, format="MM"):
        return os.path.join(SS_DIR, format, self.group)

    def icon_url(self):
        return "/".join((SS_ROOT_URL, "files", self.group, self.name + ".png"))

    def group_info_url(self):
        return "/".join((SS_ROOT_URL, self.group))

    def matrix_info_url(self):
        return "/".join((SS_ROOT_URL, self.group, self.name))

    def url(self, format="MM"):
        """
        Returns the URL for this `Matrix` instance.
        """
        fname = self._filename(format)
        directory = format.lower() if format == "MAT" else format
        return "/".join((SS_ROOT_URL, directory, self.group, fname))

    def localpath(self, format="MM", destpath=None, extract=False):
        destpath = destpath or self._defaultdestpath(format)

        # localdestpath is the directory containing the unzipped files
        # in the case of MM and RB (if extract is true) or
        # the file itself in the case of MAT (or if extract is False)
        localdest = os.path.join(destpath, self._filename(format))
        localdestpath = (
            localdest
            if (format == "MAT" or not extract)
            else os.path.join(destpath, self.name)
        )

        return localdestpath, localdest

    def download(self, format="MM", destpath=None, extract=False):
        """
        Downloads this `Matrix` instance to the local machine,
        optionally unpacking any TAR.GZ files.
        """
        # destpath is the directory containing the matrix
        # It is of the form ~/.PyUFGet/MM/HB
        destpath = destpath or self._defaultdestpath(format)

        # localdest is matrix file (.MAT or .TAR.GZ)
        # if extract = True, localdestpath is the directory
        # containing the unzipped matrix
        localdestpath, localdest = self.localpath(format, destpath, extract)

        if not os.access(localdestpath, os.F_OK):
            # Create the destination path if necessary
            os.makedirs(destpath, exist_ok=True)

            response = requests.get(self.url(format), stream=True)
            content_length = int(response.headers["content-length"])

            with open(localdest, "wb") as outfile, tqdm(
                total=content_length, desc=self.name, unit="B"
            ) as pbar:
                for chunk in response.iter_content(chunk_size=4096):
                    outfile.write(chunk)
                    pbar.update(4096)
                    time.sleep(0.1)

            if extract and (format == "MM" or format == "RB"):
                bundle.extract(localdest)

        return localdestpath, localdest

    def __str__(self):
        return str(self.to_tuple())

    def __repr__(self):
        return "Matrix" + str(self.to_tuple())

    def _repr_html_(self):
        return (
            f"<table>{Matrix.html_header()}"
            + f"<tbody>{self.to_html_row()}</tbody></table>"
        )
