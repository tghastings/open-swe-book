// Chapter 6, §6.5.3 (A Development View: Module Hierarchies) — dependency inversion.
// The application layer owns the deliver() shape; WebSocketTransport and a test
// fake both conform to it from below.
// Run: node transport_inversion.js
const assert = require("node:assert");

class MessageRouter {                  // application code sees only the deliver() shape
  constructor(transport) { this.transport = transport; }
  route(message) { this.transport.deliver(message.to, message.body); }
}

class WebSocketTransport {             // infrastructure, conforming from below.
  constructor(socket) { this.socket = socket; }      // No Transport type to declare —
  deliver(to, body) { this.socket.send(`${to}:${body}`); } // any deliver()-shaped
}                                                          // object will do.

class FakeTransport extends Array {    // a two-line test double
  deliver(to, body) { this.push([to, body]); }
}

const fake = new FakeTransport();
new MessageRouter(fake).route({ to: "eloise", body: "you are on call" });
assert.deepStrictEqual([...fake], [["eloise", "you are on call"]]);

// The real implementation conforms too — fed a stand-in socket here so the
// file runs without a network.
class RecordingSocket extends Array {
  send(data) { this.push(data); }
}
const sock = new RecordingSocket();
new MessageRouter(new WebSocketTransport(sock)).route({ to: "eloise", body: "hi" });
assert.deepStrictEqual([...sock], ["eloise:hi"]);

console.log("fake and websocket transports both satisfy MessageRouter: OK");
