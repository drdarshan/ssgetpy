def extract(bundle):
    import gzip
    import os
    import tarfile
    basedir, filename = os.path.split(bundle)
    tarfilename = os.path.join(basedir, '.'.join((filename.split('.')[0], 'tar')))
    gzfile = gzip.open(bundle, 'rb')
    with open(tarfilename, 'wb') as outtarfile:
        import shutil
        shutil.copyfileobj(gzfile, outtarfile)
    gzfile.close()    
    tarfile.open(tarfilename).extractall(basedir)
    os.unlink(tarfilename)
    os.unlink(bundle)
    
    
