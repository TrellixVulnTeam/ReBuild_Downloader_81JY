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
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(pFile, dir)

    elif file.endswith("zip"):
        with zipfile.ZipFile(file, 'r') as pFile:
            pFile.extractall(dir)

    print(" > '" + os.path.basename(file) + "' succefully extracted to:{}".format(dir))