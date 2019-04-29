import zipfile
import tarfile
import os

def IsArchive(url):
    if all([(url.find('.zip') == -1), (url.find('.tar') == -1)]):
        return False
    else:
        return True

def ArchiveExtract(dir, file):
    # print("Try to extract file '{}'".format(file))

    if file.endswith("tar.gz"):
        with tarfile.open(file, "r:gz") as pFile:
            pFile.extractall(dir)

    elif file.endswith("zip"):
        with zipfile.ZipFile(file, 'r') as pFile:
            pFile.extractall(dir)

    print(" > '" + os.path.basename(file) + "' succefully extracted to:{}".format(dir))