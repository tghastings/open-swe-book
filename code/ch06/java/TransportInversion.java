// Chapter 6, §6.5.3 (A Development View: Module Hierarchies) — dependency inversion.
// The application layer owns the Transport interface; WebSocketTransport and a test
// fake both conform to it from below.
// Run: java TransportInversion.java
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.io.UncheckedIOException;
import java.util.ArrayList;
import java.util.Map;

public class TransportInversion {
  public static void main(String[] args) {
    var fake = new FakeTransport();
    new MessageRouter(fake).route(Map.of("to", "eloise", "body", "you are on call"));
    System.out.println(fake); // [eloise:you are on call]

    // The real implementation conforms too — fed a stand-in stream here so the
    // file runs without a network.
    var sock = new ByteArrayOutputStream();
    new MessageRouter(new WebSocketTransport(sock))
        .route(Map.of("to", "eloise", "body", "hi"));
    System.out.println(sock); // eloise:hi
  }
}

interface Transport {                        // owned by the application layer
  void deliver(String to, String body);
}
record MessageRouter(Transport transport) {  // application code sees only the interface
  void route(Map<String, String> message) {
    transport.deliver(message.get("to"), message.get("body"));
  }
}
record WebSocketTransport(OutputStream socket) implements Transport { // infrastructure,
  public void deliver(String to, String body) {                      // from below
    try { socket.write((to + ":" + body).getBytes()); }
    catch (IOException e) { throw new UncheckedIOException(e); }
  }
}
class FakeTransport extends ArrayList<String> implements Transport { // a two-line double
  public void deliver(String to, String body) { add(to + ":" + body); }
}
