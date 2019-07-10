import os
import zipfile
import socket
import struct
import sys


def compress(imagedir,userid):
    f = zipfile.ZipFile(imagedir+'/'+userid+'.zip', 'w', zipfile.ZIP_DEFLATED)
    for file in os.listdir(imagedir+'/'+userid):
        f.write(imagedir+'/'+userid + '/'+file)
    f.close()


def send(userid, imagedir='../images'):
    # imagedir = 'image'
    if os.path.exists(os.path.join(imagedir, userid)):
        compress(imagedir, userid)
        return True
    else:
        return False


def socket_client(filepath, ip='127.0.0.1', port=6666):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    print(s.recv(1024))
    if os.path.isfile(filepath):
        # 定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
        fileinfo_size = struct.calcsize('128si')
        # 定义文件头信息，包含文件名和文件大小

        fhead = struct.pack('128si', str.encode(os.path.basename(filepath)), os.stat(filepath).st_size)

        s.send(fhead)
        # s.send(b'%s')
        print('client filepath: {0}'.format(filepath))

        fp = open(filepath, 'rb')
        while 1:
            data = fp.read(1024)
            if not data:
                print('{0} file send over...'.format(filepath))
                break
            s.send(data)
    s.close()
# filepath='../image/123.zip'
# print(type(os.stat('../image/123.zip').st_size))
# struct.pack('i',os.path.getsize(filepath))
# fhead = struct.pack('128s', b'123.zip')
# print(type(os.path.getsize(filepath)))
# # fhead = struct.pack('128si', '123.zip', os.path.getsize(filepath))
# print(type(os.stat('../image/123.zip').st_size))
# fhead = struct.pack('128si', str.encode(os.path.basename(filepath))  , os.stat(filepath).st_size)