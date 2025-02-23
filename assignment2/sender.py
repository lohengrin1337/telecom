#!/usr/bin/env python3

from abc import ABC, abstractmethod
import time

class Sender(ABC):
    """ Abstract stream sender.
        Capable of sending text messages
        as packet stream of variable
        frequency.
        Subclasses must implement _create_socket(), _connect() and _send()
        differently depending on socket type. """

    def __init__(self):
        """ Create socket, set defaults """
        self._socket = None
        self._receiver_name = None
        self._receiver_port = None
        self._stream_frequency = 1
        self._timeout = 60
        self._packet_counter = 0
        self._sequence_num = 10000
        self._message = "A" * 1465  # nonsense text mesage, 1465 'A' = 1465 bytes
        self._msg_terminator = "####"

        self._create_socket()

    @abstractmethod
    def _create_socket():
        """ Assign a socket of some type to _socket """
        pass

    def set_receiver(self, name, port):
        self._receiver_name = name
        self._receiver_port = port
        return self

    def set_stream_frequency(self, freq):
        self._stream_frequency = freq
        return self

    # def set_timeout(self, timeout):
    #     self._timeout = timeout     # seconds
    #     return self

    def _generate_payload(self):
        """ Generate corrupt payload """
        self._sequence_num += 1     # increment seq num

        if self._sequence_num % 5 == 0:
            # self._sequence_num += 1
            return str(self._sequence_num) + ";" + self._message

        return str(self._sequence_num) + ";" + self._message + self._msg_terminator

    def stream(self):
        """ Send UPD segments at a given frequency """
        if not self._receiver_name or not self._receiver_port:
            raise Exception("Set receiver (name and port) before streaming!")

        try:
            # Establish connection (tcp only)
            self._connect()

            print(f"Streaming at {self._stream_frequency}Hz for {self._timeout}s")

            send_interval = 1 / self._stream_frequency
            timeout = time.perf_counter() + self._timeout
            while time.perf_counter() < timeout:
                start = time.perf_counter()

                payload = self._generate_payload()
                self._send(payload)
                self._packet_counter += 1

                end = time.perf_counter()
                elapsed = end - start

                # wait approx 1 send interval
                time.sleep(max(0, send_interval - elapsed - 0.000126))

        except ConnectionError as e:
            print(f"CONNECTION ERROR: {e}")
        finally:
            self._close()
            self._print_status()

    @abstractmethod
    def _connect():
        """ Must be implemented by subclass using tcp socket """
        pass

    def _generate_payload(self):
        """ Generate a 1475 byte payload with a seq num, a nonsense message and a terminator
            '10001;AAAAAAA....####' """
        self._sequence_num += 1
        return str(self._sequence_num) + ";" + self._message + self._msg_terminator

    @abstractmethod
    def _send():
        """ Socket specific method to be implemented by subclass """
        pass

    def _close(self):
        self._socket.close()
        print("Socket closed")

    def _print_status(self):
        print(f"{self._packet_counter} packets sent")

