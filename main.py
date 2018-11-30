#!/usr/bin/env python3

import socket
import sys
from parser import Parser, EndOfSimulation, SyntaxErr, LexerError


with socket.socket() as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('localhost', 10000))

    sock.listen(1)

    end = False

    conn, addr = sock.accept()

    with conn:

        parser = Parser()

        while not end:
            data = conn.recv(1024)
            if not data:
                continue
            try:
                conn.sendall(parser.parse(data.decode('utf-8')).encode())
            except EndOfSimulation:
                end = True
            except SyntaxErr:
                conn.sendall('Input malformado 2'.encode())
            except LexerError:
                conn.sendall('Input malformado 1'.encode())
