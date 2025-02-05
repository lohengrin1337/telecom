#!/usr/bin/env python3

from socket import *

class CustomWebBrowser:
    """ Simple custom web browser
        Author: Olof Jönsson, oljn22 """

    def __init__(self):
        """ Set name, and create TCP socket """
        self._name = "CustomWebBrowser/1.0"
        self._socket = socket(AF_INET, SOCK_STREAM)

    def _connect(self, host, port=80):
        """ Connect to server host"""
        self._socket.connect((host, port))

    def _send(self, header):
        """ Send encoded header into socket """
        print("<<< SENDING REQUEST >>>\n")
        print(header)
        self._socket.send(header.encode())

    def _receive_and_print(self):
        """ Receive response from server host, decode and print """
        response = self._socket.recv(1024)
        print("<<< RECEIVING RESPONSE >>>\n")
        print(response.decode())

    def _close(self):
        """ Close socket """
        self._socket.close()

    def _build_header(
        self,
        host,
        path,
        query,
        method="GET",
        protocol="HTTP/1.1",
        accept="text/html",
        conn="close"
    ):
        """ Build an HTTP header """
        header = f"{method} {path}{query} {protocol}\r\n"
        header += f"Host: {host}\r\n"
        header += f"User-Agent: {self._name}\r\n"
        header += f"Accept: {accept}\r\n"
        header += f"Connection: {conn}\r\n"
        header += "\r\n"

        return header

    def request_page(self, host, path, query):
        """ Request a web resource """
        self._connect(host)
        self._send(self._build_header(host, path, query))
        self._receive_and_print()
        self._close()


if __name__ == "__main__":
    # Resource to request
    host = "www.ingonline.nu"
    path = "/tictactoe/index.php"
    query = "?board=xoxoxoeee"

    # Init browser, and request page
    browser = CustomWebBrowser()
    browser.request_page(host, path, query)
