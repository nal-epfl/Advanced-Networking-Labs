#!/usr/bin/env python3
"""TLS client used for Lab 3, Part 5.

Usage: python3 Part5_PDC.py <command> <path-to-CA-certificate>
"""

import socket
import ssl
import sys
from time import sleep


HOST = "127.0.0.1"
PORT = 5003
BUFFER_SIZE = 1024
RETRIES_1 = 100


def main() -> None:
    if len(sys.argv) != 3:
        print("usage: %s <command> <path to CA certificate>" % sys.argv[0])
        sys.exit(1)

    command = sys.argv[1]
    ca_certificate = sys.argv[2]

    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations(cafile=ca_certificate)
    context.check_hostname = False
    # uncomment tht following line if you are testing on python version 3.13 or later
    context.verify_flags &= ~ssl.VERIFY_X509_STRICT

    with socket.create_connection((HOST, PORT)) as tcp_socket:
        with context.wrap_socket(tcp_socket, server_hostname=HOST) as tls_socket:
            print("ssl_s1:", tls_socket)

            tls_socket.sendall(command.encode("utf-8"))
            print("sending:", command)

            for _ in range(RETRIES_1):
                data = tls_socket.recv(BUFFER_SIZE)
                if not data:
                    break
                print("User 1 received:", data.decode("utf-8"), "\n")
                sleep(1)


if __name__ == "__main__":
    main()
