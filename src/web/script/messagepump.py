import select
import logging

class MessagePump:


  def wait(self, websocket, sievesocket):

    ready_to_read, _ready_to_write, in_error \
      = select.select([websocket, sievesocket], [], [websocket, sievesocket])

    if websocket in in_error:
      raise Exception("Reading websocket connection failed")

    if sievesocket in in_error:
      raise Exception("Reading Sieve socket connection failed")

    return ready_to_read

  def run(self, websocket, sievesocket) -> None:

    while True:
      sockets = self.wait(websocket, sievesocket)

      if websocket in sockets:
        data = websocket.recv()

        if data == b'':
          logging.info("Websocket terminated")
          return

        logging.debug(data)
        sievesocket.send(data)

      if sievesocket in sockets:
        data = sievesocket.recv()

        if data == b'':
          logging.info("Sieve socket terminated")
          return

        logging.debug(data)
        websocket.send(data)
