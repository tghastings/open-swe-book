# Chapter 6, §6.5.3 (A Development View: Module Hierarchies) — dependency inversion.
# The application layer owns the Transport interface; WebSocketTransport and a test
# fake both conform to it from below.
# Run: python3 transport_inversion.py
from typing import Protocol


class Transport(Protocol):                 # owned by the application layer
  def deliver(self, to: str, body: str) -> None: ...


class MessageRouter:                       # application code sees only the interface
  def __init__(self, transport: Transport):
    self._transport = transport

  def route(self, message: dict) -> None:
    self._transport.deliver(message["to"], message["body"])


class WebSocketTransport:                  # infrastructure, conforming from below
  def __init__(self, socket):
    self._socket = socket

  def deliver(self, to: str, body: str) -> None:
    self._socket.send(f"{to}:{body}".encode())


class FakeTransport(list):                 # a two-line test double
  def deliver(self, to, body): self.append((to, body))


fake = FakeTransport()
MessageRouter(fake).route({"to": "eloise", "body": "you are on call"})
assert fake == [("eloise", "you are on call")]


# The real implementation conforms too — fed a stand-in socket here so the
# file runs without a network.
class RecordingSocket(list):
  def send(self, data): self.append(data)


sock = RecordingSocket()
MessageRouter(WebSocketTransport(sock)).route({"to": "eloise", "body": "hi"})
assert sock == [b"eloise:hi"]

print("fake and websocket transports both satisfy MessageRouter: OK")
