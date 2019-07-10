#!/usr/bin/env python
# -*- coding=utf-8 -*-


"""
file: recv.py
socket service
"""

import socket
import threading
import time
import sys
import os
import struct
from Util import receive

def socket_service(ip='0.0.0.0', port=6666,imagedir='../images'):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((ip, port))
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print('Waiting connection...')

    while 1:
        conn, addr = s.accept()
        if not os.path.exists(imagedir):
            os.mkdir(imagedir)
        t = threading.Thread(target=deal_data, args=(conn, addr,imagedir))
        t.start()


def deal_data(conn, addr, imagedir='../images'):
    print('Accept new connection from {0}'.format(addr))
    # conn.settimeout(500)
    conn.send(b'Hi, Welcome to the server!')

    while 1:
        fileinfo_size = struct.calcsize('128si')
        buf = conn.recv(fileinfo_size)
        if buf:
            filename, filesize = struct.unpack('128si', buf)
            fn = filename.strip(b'\00')
            # fn = buf.strip('\00')
            file = bytes.decode(fn)
            new_filename = os.path.join(imagedir, file)
            print('file new name is {0}, filesize if {1}'.format(new_filename,
                                                           filesize))

            recvd_size = 0  # 定义已接收文件的大小
            fp = open(new_filename, 'wb')
            print('start receiving...')

            while not recvd_size == filesize:
                if filesize - recvd_size > 1024:
                    data = conn.recv(1024)
                    recvd_size += len(data)
                else:
                    data = conn.recv(filesize - recvd_size)
                    recvd_size = filesize
                fp.write(data)
            fp.close()
            print('end receive...')
        conn.close()
        print(file)
        receive.receive(file, imagedir, '../')
        break


if __name__ == '__main__':
    socket_service(ip='0.0.0.0', port=7777,imagedir='../images')

