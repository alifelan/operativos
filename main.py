#!/usr/bin/env python3

import socket
import sys

unsupported = False
end = False

def process_SVC(call: str) -> str:
    separated = call.split(' ')
    global end
    global unsupported
    end = end or separated[0] == 'End'
    unsupported = unsupported or separated[0] == 'Politicas' and (separated[2] != 'RR' or separated[4] != 'MFU')
    if unsupported:
        return 'Politica de scheduling o de manejo de memoria no soportada'
    return 'Dummy message'


with socket.socket() as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('localhost', 10000))

    sock.listen(1)

    conn, addr = sock.accept()

    with conn:

        while not end:
            data = conn.recv(1024)
            if not data:
                continue
            conn.sendall(process_SVC(data.decode('utf-8')).encode())
