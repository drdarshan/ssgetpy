'''
The `csvindex` module parses the UFStats.csv file and generate entries for each row in a Matrix database
'''

def getdtype(real, logical):
    '''
    Converts a (real, logical) pair into one of the three types, 'real', 'complex' and 'binary'
    '''
    return 'binary' if logical else ('real' if real else 'complex')
    
def gen_rows(csvfile):
    '''
    Creates a generator that returns a single row in the matrix database.
    '''
    import csv
    reader = csv.reader(csvfile)
    matid = 0
    for line in reader:
        matid  += 1
        group   = line[0]
        name    = line[1]
        rows    = int(line[2])
        cols    = int(line[3])
        nnz     = int(line[4])
        real    = bool(int(line[5]))
        logical = bool(int(line[6]))
        is2d3d  = bool(int(line[7]))
        isspd   = bool(int(line[8]))
        psym    = float(line[9])
        nsym    = float(line[10])
        kind    = line[11]
        yield matid, group, name, rows, cols, nnz, getdtype(real, logical), is2d3d, isspd, psym, nsym, kind
                        
def generate():
    from config import UF_INDEX_URL
    import urllib2
    csvfile = urllib2.urlopen(UF_INDEX_URL)

    import logging
    # Read the number of entries
    logging.info("Number of entries in the CSV file: " + csvfile.readline())
    # Read the last modified date
    logging.info("Last modified date: " + csvfile.readline())
    
    return gen_rows(csvfile)
