// Chapter 6, §6.5.3 (A Development View: Module Hierarchies) — dependency inversion.
// The application layer owns the Transport interface; WebSocketTransport and a test
// fake both conform to it from below.
// Run: go run transport_inversion.go
package main

import (
	"bytes"
	"fmt"
	"io"
)

type Transport interface { // owned by the application layer
	Deliver(to, body string)
}

type MessageRouter struct{ transport Transport } // sees only the interface
func (r MessageRouter) Route(message map[string]string) {
	r.transport.Deliver(message["to"], message["body"])
}

type WebSocketTransport struct{ sock io.Writer } // infrastructure, conforming from below
func (t WebSocketTransport) Deliver(to, body string) {
	t.sock.Write([]byte(to + ":" + body))
}

// FakeTransport never says "implements Transport" — satisfying it is enough.
type FakeTransport struct{ sent []string }       // a two-line test double
func (t *FakeTransport) Deliver(to, body string) { t.sent = append(t.sent, to+":"+body) }

func main() {
	fake := &FakeTransport{}
	MessageRouter{fake}.Route(map[string]string{"to": "eloise", "body": "you are on call"})
	fmt.Println(fake.sent) // [eloise:you are on call]

	// The real implementation conforms too — fed a stand-in writer here so the
	// file runs without a network.
	var sock bytes.Buffer
	router := MessageRouter{WebSocketTransport{&sock}}
	router.Route(map[string]string{"to": "eloise", "body": "hi"})
	fmt.Println(sock.String()) // eloise:hi
}
