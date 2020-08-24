import gzip
import os
import shutil
import tarfile


def extract(bundle):
    basedir, filename = os.path.split(bundle)
    tarfilename = os.path.join(
        basedir, ".".join((filename.split(".")[0], "tar"))
    )
    gzfile = gzip.open(bundle, "rb")
    with open(tarfilename, "wb") as outtarfile:
        shutil.copyfileobj(gzfile, outtarfile)
    gzfile.close()
    tarfile.open(tarfilename).extractall(basedir)
    os.unlink(tarfilename)
    os.unlink(bundle)
