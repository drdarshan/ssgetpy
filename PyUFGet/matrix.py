class Matrix(object):
    '''
    A `Matrix` object represents a single matrix in the University of Florida sparse matrix collection. It has the following attributes:
    `id`   : The unique identifier for the matrix in the database.
    `group`: The name of the group this matrix belongs to.
    `name` : The name of this matrix.
    `rows` : The number of rows.
    `cols` : The number of columns.
    `nnz`  : The number of non-zero elements.
    `dtype`: The datatype of the non-zero elements, `real`, `complex` or `binary`.
    `is2d3d`: True if this matrix comes from a 2D or 3D discretization.
    `isspd` : True if this matrix is symmetric, positive definite
    `kind`  : The underlying problem domain
    '''
    def __init__(self, identifier, group, name, \
                     rows, cols, nnz, dtype,\
                     is2d3d, isspd, psym, nsym, kind):
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

    def tuple(self):
        '''
        Returns the fields in a `Matrix` instance in a tuple.
        '''
        return self.id, self.group, self.name, self.rows, self.cols, self.nnz, self.dtype, self.is2d3d, self.isspd, self.psym, self.nsym, self.kind

    def _filename(self, format = 'MM'):
        if format == 'MM' or format == 'RB':
            return self.name + ".tar.gz"
        elif format == 'MAT':
            return self.name + ".mat"
        else:
            raise ValueError("Format must be 'MM', 'MAT' or 'RB'")

    def _defaultdestpath(self, format = 'MM'):
        from config import UF_DIR
        import os
        return os.path.join(UF_DIR, format, self.group)

    def url(self, format = 'MM'):
        '''
        Returns the URL for this `Matrix` instance.
        '''
        from config import UF_ROOT_URL
        fname = self._filename(format)
        directory = format.lower() if format == 'MAT' else format
        return "/".join((UF_ROOT_URL, directory, self.group, fname))

    
    def localpath(self, format = 'MM', destpath = None, extract = False):
        destpath = destpath or self._defaultdestpath(format)

        # localdestpath is the directory containing the unzipped files
        # in the case of MM and RB (if extract is true) or the file it self in the case of MAT (or if extract is False)
        import os
        localdest     = os.path.join(destpath, self._filename(format))
        localdestpath = localdest if (format == "MAT" or not extract) else os.path.join(destpath, self.name)

        return localdestpath, localdest

    def download(self, format = 'MM', destpath = None, extract = False):
        '''
        Downloads this `Matrix` instance to the local machine, optionally unpacking any TAR.GZ files.
        '''
        # destpath is the directory containing the matrix
        # It is of the form ~/.PyUFGet/MM/HB
        destpath = destpath or self._defaultdestpath(format)

        # localdest is matrix file (.MAT or .TAR.GZ)
        # if extract = True, localdestpath is the directory containing the unzipped matrix
        localdestpath, localdest = self.localpath(format, destpath, extract)

        import os
        if not os.access(localdestpath, os.F_OK):
            # Create the destination path if necessary
            if not os.access(destpath, os.W_OK):
                os.makedirs(destpath)

            import urllib2, shutil
            infile = urllib2.urlopen(urllib2.Request(self.url(format)))
            # Use SHUTIL to download the file in chunks
            with open(localdest, "wb") as outfile:
                shutil.copyfileobj(infile, outfile)
            infile.close()
            if extract and (format == "MM" or format == "RB"):
                import bundle
                bundle.extract(localdest)

        return localdestpath, localdest

    def __str__(self):
        return str(self.tuple())

    def __repr__(self):
        return "Matrix" + str(self.tuple())
