#!/usr/bin/env python3

from socket import *
import time

class UDPSender:
    """ UDP stream sender 
        Capable of sending text messages
        as UDP packet stream of variable
        frequency """

    def __init__(self):
        """ Create UDP socket """
        self._socket = socket(AF_INET, SOCK_DGRAM)
        self._receiver_name = None
        self._receiver_port = None
        self._stream_frequency = 1
        self._timeout = 60
        self._sequence_num = 10000
        self._message = "A" * 1465  # nonsense text mesage
        self._msg_terminator = "####"

    def set_receiver(self, name, port):
        self._receiver_name = name
        self._receiver_port = port
        return self

    def set_stream_frequency(self, freq):
        self._stream_frequency = freq
        return self

    def set_timeout(self, timeout):
        self._timeout = timeout     # seconds
        return self

    def _generate_payload(self):
        """ Generate a 1475 byte payload with a seq num, a nonsense message and a terminator
            '10001;AAAAAAA....####' """
        self._sequence_num += 1     # increment seq num
        return str(self._sequence_num) + ";" + self._message + self._msg_terminator

    def stream(self):
        """ Send UPD segments at a given frequency """
        if not self._receiver_name or not self._receiver_port:
            raise Exception("Set receiver (name and port) before streaming!")

        timeout = time.time() + self._timeout
        while time.time() < timeout:
            payload = self._generate_payload()
            self._socket.sento(payload.encode(), (self._receiver_name, self._receiver_port))
            # print(f"receiver: {self._receiver_name}, {self._receiver_port}\nfreq: {self._stream_frequency}\ntimeout: {self._timeout}\npayload: {payload}\n")

            time.sleep(1 / self._stream_frequency)

        print("timeout")
        self._close()

    def _close(self):
        self._socket.close()


if __name__ == "__main__":
    rec_name = "127.0.0.1"
    rec_port = 12000
    freq = 1
    timeout = 3

    udp_sender = UDPSender()
    udp_sender.set_receiver(rec_name, rec_port).set_stream_frequency(freq).set_timeout(timeout)
    udp_sender.stream()
