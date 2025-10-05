import logging
import select

from script.sieve.sievesocket import SieveSocket
from script.websocket import WebSocket


class MessagePump:
  def __init__(self, websocket: WebSocket, sieve_socket: SieveSocket):
    self._websocket = websocket
    self._sieve_socket = sieve_socket

  def wait(self):
    ready_to_read, _ready_to_write, in_error \
      = select.select([self._websocket, self._sieve_socket], [], [self._websocket, self._sieve_socket])

    if self._websocket in in_error:
      raise Exception("Reading websocket connection failed")

    if self._sieve_socket in in_error:
      raise Exception("Reading Sieve socket connection failed")

    return ready_to_read

  def run(self) -> None:
    while True:
      sockets = self.wait()

      if self._websocket in sockets:
        data = self._websocket.recv()

        if data == b'':
          logging.info("Websocket terminated")
          return

        logging.debug(data)
        self._sieve_socket.send(data)

      if self._sieve_socket in sockets:
        data = self._sieve_socket.recv()

        if data == b'':
          logging.info("Sieve socket terminated")
          return

        logging.debug(data)
        self._websocket.send(data)
