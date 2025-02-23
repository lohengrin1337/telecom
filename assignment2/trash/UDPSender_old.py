#!/usr/bin/env python3

from socket import *
import time

class UDPSender:
    """ UDP stream sender 
        Capable of sending text messages
        as UDP packet stream of variable
        frequency """

    def __init__(self):
        """ Create UDP socket, and set default properties """
        self._socket = socket(AF_INET, SOCK_DGRAM)
        self._receiver_name = None
        self._receiver_port = None
        self._stream_frequency = 1
        self._timeout = 60
        self._packet_counter = 0
        self._sequence_num = 10000
        self._message = "A" * 1465  # nonsense text mesage, 1465 'A' = 1465 bytes
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
        self._sequence_num += 1
        return str(self._sequence_num) + ";" + self._message + self._msg_terminator

    # def _generate_payload(self):
    #     """ Generate corrupt payload """
    #     self._sequence_num += 1     # increment seq num

    #     if self._sequence_num % 5 == 0:
    #         # self._sequence_num += 1
    #         return str(self._sequence_num) + ";" + self._message

    #     return str(self._sequence_num) + ";" + self._message + self._msg_terminator

    def stream(self):
        """ Send UPD segments at a given frequency """
        if not self._receiver_name or not self._receiver_port:
            raise Exception("Set receiver (name and port) before streaming!")

        print(f"Streaming with {self._stream_frequency}Hz for {self._timeout}s")

        send_interval = 1 / self._stream_frequency
        timeout = time.perf_counter() + self._timeout
        while time.perf_counter() < timeout:
            start = time.perf_counter()

            payload = self._generate_payload()
            self._socket.sendto(payload.encode(), (self._receiver_name, self._receiver_port))
            self._packet_counter += 1

            end = time.perf_counter()
            elapsed = end - start

            # wait approx 1 send interval
            time.sleep(max(0, send_interval - elapsed - 0.000126))

        print(f"Timeout after {self._timeout}s\n{self._packet_counter} packets sent")
        self._close()

    def _close(self):
        self._socket.close()


if __name__ == "__main__":
    rec_name = "127.0.0.1"
    rec_port = 12000
    freq = 15
    timeout = 30

    udp_sender = UDPSender()
    udp_sender.set_receiver(rec_name, rec_port).set_stream_frequency(freq).set_timeout(timeout)
    udp_sender.stream()
