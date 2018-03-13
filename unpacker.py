import zipfile
import tarfile
import os

def ArchiveExtract(dir, file):
    if file.endswith("tar.gz"):
        with tarfile.open(file, "r:gz") as pFile:
            pFile.extractall(dir)

    elif file.endswith("zip"):
        with zipfile.ZipFile(file, 'r') as pFile:
            pFile.extractall(dir)

    print(" > '" + os.path.basename(file) + "' succefully extracted to: " + dir)