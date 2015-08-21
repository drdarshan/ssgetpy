def search(name_or_id = None, **kwargs):
    '''
    Search for matrix/matrices with a given name pattern or numeric ID. Optionally, limit
    search to matrices of a specific data type or with the specified range of rows, columns and non-zero values.    
    '''
    import logging
    logging.debug("Name or ID = " + str(name_or_id))
    if name_or_id is not None:
        if isinstance(name_or_id, str):
            if '/' in name_or_id:
                group, name = name_or_id.split('/')
                kwargs['group'] = group
                if not name == '' and not name == '*':
                    kwargs['name'] = name
            else:
                kwargs['name'] = name_or_id
        elif isinstance(name_or_id, int):
            kwargs['matid'] = name_or_id
        else:
            raise ValueError("First argument to search must be a string or an integer")

    from dbinstance import instance
    return instance.search(**kwargs)

def fetch(name_or_id = None, format = 'MM', location = None, dry_run = False, **kwargs):
    import logging
    matrices = search(name_or_id, **kwargs)
    if len(matrices) > 0:
        logging.info("Found %d %s" % (len(matrices), "entry" if len(matrices) == 1 else "entries"))
        for matrix in matrices:
            logging.info("Downloading %s/%s to %s" % \
                             (matrix.group, matrix.name, matrix.localpath(format, location, extract = True)[0]))
            if not dry_run:
                matrix.download(format, location, extract = True)
    return matrices
        
def cli(argv):
    from optparse import OptionParser, OptionGroup
    from config import UF_DIR
    parser = OptionParser(usage = "Usage: %prog [NameOrID] [options]")

    parser.add_option("-i", "--id", action="store", type="int", dest="matid", help="Download a matrix with the given ID.")
    parser.add_option("-g", "--group", action="store", type="string", dest="group", help="The matrix group.")
    parser.add_option("-n", "--name" , action="store", type="string", dest="name", help="The name or a pattern matching the name of the matrix/matrices.")
    parser.add_option("-d", "--data-type", action="store", type="string", dest="dtype", help="The element type of the matrix/matrices"
                      ", can be one of 'real', 'complex' or 'binary'.")
    parser.add_option("-s", "--spd", action="store_true", dest="isspd", help="Only selects SPD matrices.")    
    parser.add_option("-f", "--format", action="store", type="string", dest="format", default="MM", \
                      help="The format in which to download the matrix/matrices.\
                      Can be one of 'MM', 'MAT' or 'RB' for MatrixMarket, MATLAB or Rutherford-Boeing formats respectively. Defaults to 'MM'.")
    parser.add_option("-l", "--limit", action="store", type="int", dest="limit", help="The maximum number of matrices to be downloaded. Defaults to 10.")
    parser.add_option("-o", "--outdir", action="store", type="string", dest="location", \
                      help="The directory in the local machine where matrices will be downloaded to. Defaults to " + UF_DIR)
    parser.add_option("--dry-run", action="store_true", dest = "dry_run", default=False, help="If True, only print the matrices that will be downloaded but do not actually download them.")
    
    g = OptionGroup(parser, "Size and Non-zero filters", "These options may be used to restrict the shape or number of non-zero elements of the matrices to be downloaded")
    
    g.add_option("--min-rows", action="store", type="int", dest="min_rows", help="The minimum number of rows in the matrix/matrices.")
    g.add_option("--max-rows", action="store", type="int", dest="max_rows", help="The maximum number of rows in the matrix/matrices.")
    g.add_option("--min-cols", action="store", type="int", dest="min_cols", help="The minimum number of columns in the matrix/matrices.")
    g.add_option("--max-cols", action="store", type="int", dest="max_cols", help="The maximum number of columns in the matrix/matrices.")
    g.add_option("--min-nnzs", action="store", type="int", dest="min_nnzs", help="The minimum number of non-zero values in the matrix/matrices.")
    g.add_option("--max-nnzs", action="store", type="int", dest="max_nnzs", help="The maximum number of non-zero values in the matrix/matrices.")

    parser.add_option_group(g)

    lg = OptionGroup(parser, "Logging and verbosity options", "These options govern the level of spew from PyUFGet. By default, PyUFGet prints a small number of messages such as the number of matrices being downloaded and where they are being downloaded to. To suppress these message, pass --quiet. To enable debug diagnostics, pass --verbose.")
    lg.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="Enable debug diagnostics.")
    lg.add_option("-q", "--quiet", action="store_true", dest="quiet", default=False, help="Do not print any messages to the console.")
    
    parser.add_option_group(lg)

    if len(argv) == 0:
        parser.print_help()
        return
    
    options, args = parser.parse_args(argv)

    if len(args) > 1:
        raise ValueError("Too many positional arguments.")

    name_or_id = args[0] if len(args) == 1 else None

    # Convert name_or_id to an integer if possible
    try:
        name_or_id = int(name_or_id)
    except Exception:
        pass

    optdict = dict(matid = options.matid, \
                       group     = options.group, \
                       name      = options.name,\
                       rowbounds = (options.min_rows, options.max_rows),\
                       colbounds = (options.min_cols, options.max_cols),\
                       nzbounds  = (options.min_nnzs, options.max_nnzs),\
                       dtype     = options.dtype,\
                       isspd     = options.isspd)
    if options.limit:
        optdict["limit"] = options.limit

    import logging
    if options.quiet:
        pass
    elif options.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    fetch(name_or_id, options.format, options.location, options.dry_run, **optdict)
