import argparse
import logging
import sys

from .config import SS_DIR
from .dbinstance import instance

logger = logging.getLogger(__name__)


def search(name_or_id=None, **kwargs):
    """
    Search for matrix/matrices with a given name pattern or numeric ID.
    Optionally, limit search to matrices of a specific data type or
    with the specified range of rows, columns and non-zero values.
    """
    logger.debug("Name or ID = " + str(name_or_id))
    if name_or_id is not None:
        if isinstance(name_or_id, str):
            if "/" in name_or_id:
                group, name = name_or_id.split("/")
                kwargs["group"] = group
                if not name == "" and not name == "*":
                    kwargs["name"] = name
            else:
                kwargs["name"] = name_or_id
        elif isinstance(name_or_id, int):
            kwargs["matid"] = name_or_id
        else:
            raise ValueError(
                "First argument to search " + "must be a string or an integer"
            )

    return instance.search(**kwargs)


def fetch(
    name_or_id=None, format="MM", location=None, dry_run=False, **kwargs
):
    matrices = search(name_or_id, **kwargs)
    if len(matrices) > 0:
        logger.info(
            "Found %d %s"
            % (len(matrices), "entry" if len(matrices) == 1 else "entries")
        )
        for matrix in matrices:
            logger.info(
                "Downloading %s/%s to %s"
                % (
                    matrix.group,
                    matrix.name,
                    matrix.localpath(format, location, extract=True)[0],
                )
            )
            if not dry_run:
                matrix.download(format, location, extract=True)
    return matrices


def cli(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(prog="ssget")

    parser.add_argument(
        "-i",
        "--id",
        action="store",
        type=int,
        dest="matid",
        help="Download a matrix with the given ID.",
    )
    parser.add_argument(
        "-g",
        "--group",
        action="store",
        type=str,
        dest="group",
        help="The matrix group.",
    )
    parser.add_argument(
        "-n",
        "--name",
        action="store",
        type=str,
        dest="name",
        help="The name or a pattern matching the name of the matrix/matrices.",
    )
    parser.add_argument(
        "-d",
        "--data-type",
        action="store",
        type=str,
        dest="dtype",
        help="The element type of the matrix/matrices"
        ", can be one of 'real', 'complex' or 'binary'.",
    )
    parser.add_argument(
        "-f",
        "--format",
        action="store",
        type=str,
        dest="format",
        default="MM",
        help="The format in which to download the matrix/matrices.\
              Can be one of 'MM', 'MAT' or 'RB' for MatrixMarket, \
              MATLAB or Rutherford-Boeing formats respectively.",
    )
    parser.add_argument(
        "-l",
        "--limit",
        action="store",
        type=int,
        default=10,
        dest="limit",
        help="The maximum number of matrices to be downloaded.",
    )
    parser.add_argument(
        "-o",
        "--outdir",
        action="store",
        type=str,
        dest="location",
        help="The directory in the local machine where matrices will be \
              downloaded to. Defaults to "
        + SS_DIR,
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        dest="dry_run",
        default=False,
        help="If True, only print the matrices that will be downloaded \
              but do not actually download them.",
    )

    g = parser.add_argument_group(
        "Size and Non-zero filters",
        "These options may be used to restrict the shape or number "
        + "of non-zero elements of the matrices to be downloaded",
    )

    g.add_argument(
        "--min-rows",
        action="store",
        type=int,
        dest="min_rows",
        help="The minimum number of rows in the matrix/matrices.",
    )
    g.add_argument(
        "--max-rows",
        action="store",
        type=int,
        dest="max_rows",
        help="The maximum number of rows in the matrix/matrices.",
    )
    g.add_argument(
        "--min-cols",
        action="store",
        type=int,
        dest="min_cols",
        help="The minimum number of columns in the matrix/matrices.",
    )
    g.add_argument(
        "--max-cols",
        action="store",
        type=int,
        dest="max_cols",
        help="The maximum number of columns in the matrix/matrices.",
    )
    g.add_argument(
        "--min-nnzs",
        action="store",
        type=int,
        dest="min_nnzs",
        help="The minimum number of non-zero values in the matrix/matrices.",
    )
    g.add_argument(
        "--max-nnzs",
        action="store",
        type=int,
        dest="max_nnzs",
        help="The maximum number of non-zero values in the matrix/matrices.",
    )

    lg = parser.add_argument_group(
        "Logging and verbosity options",
        "These options govern the level of spew from ssgetpy. "
        + "By default, ssgetpy prints a small number of messages "
        + "such as the number of matrices being downloaded and "
        + "where they are being downloaded to. "
        + "To suppress these message, pass --quiet. "
        + "To enable debug diagnostics, pass --verbose.",
    )
    lg.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        dest="verbose",
        default=False,
        help="Enable debug diagnostics.",
    )
    lg.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        dest="quiet",
        default=False,
        help="Do not print any messages to the console.",
    )

    if len(argv) == 0:
        parser.print_help()
        return

    args = parser.parse_args(argv)

    optdict = dict(
        matid=args.matid,
        group=args.group,
        name=args.name,
        rowbounds=(args.min_rows, args.max_rows),
        colbounds=(args.min_cols, args.max_cols),
        nzbounds=(args.min_nnzs, args.max_nnzs),
        dtype=args.dtype,  # isspd     = args.isspd,\
        limit=args.limit,
    )

    if args.quiet:
        pass
    elif args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    name_or_id = None
    if args.matid:
        name_or_id = args.matid
    elif args.name:
        name_or_id = args.matid

    fetch(name_or_id, args.format, args.location, args.dry_run, **optdict)
