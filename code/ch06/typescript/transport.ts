import * as assert from "node:assert";

interface Transport { deliver(to: string, body: string): void; }
interface Message { to: string; body: string; }
interface Socket { send(data: string): void; }

class MessageRouter {                     // application code sees only the interface
  private transport: Transport;
  constructor(transport: Transport) { this.transport = transport; }
  route(message: Message) { this.transport.deliver(message.to, message.body); }
}

class WebSocketTransport implements Transport {   // infrastructure, from below
  private socket: Socket;
  constructor(socket: Socket) { this.socket = socket; }
  deliver(to: string, body: string) { this.socket.send(`${to}:${body}`); }
}

class FakeTransport implements Transport {        // a two-line test double
  sent: [string, string][] = [];
  deliver(to: string, body: string) { this.sent.push([to, body]); }
}

const fake = new FakeTransport();
new MessageRouter(fake).route({ to: "eloise", body: "you are on call" });
assert.deepStrictEqual(fake.sent, [["eloise", "you are on call"]]);
