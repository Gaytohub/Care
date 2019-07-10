import os
import zipfile


def decompress(filename, imagedir, outdir):
    print(imagedir+'/'+filename)
    file_zip = zipfile.ZipFile(imagedir+'/'+filename, 'r')
    for file in file_zip.namelist():
        file_zip.extract(file, outdir)
    file_zip.close()
    os.remove(imagedir+'/'+filename)


def receive(filename, imagedir='../images', outdir='../'):
    print(filename)
    if os. path.exists(imagedir+'/'+filename):
        decompress(filename, imagedir, outdir)
        return True
    else:
        return False


if __name__ == '__main__':
    receive('123', '../images', '../')