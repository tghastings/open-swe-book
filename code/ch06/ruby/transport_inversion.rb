# Chapter 6, §6.5.3 (A Development View: Module Hierarchies) — dependency inversion.
# The application layer owns the deliver method; WebSocketTransport and a test
# fake both conform to it from below.
# Run: ruby transport_inversion.rb
require "stringio"

class MessageRouter                    # application code sees only the deliver method
  def initialize(transport) = @transport = transport
  def route(message) = @transport.deliver(message["to"], message["body"])
end

class WebSocketTransport               # infrastructure, conforming from below.
  def initialize(socket) = @socket = socket        # No Transport type to declare —
  def deliver(to, body) = @socket.write("#{to}:#{body}")  # any object that answers
end                                                       # deliver will do.

class FakeTransport < Array            # a two-line test double
  def deliver(to, body) = push([to, body])
end

fake = FakeTransport.new
MessageRouter.new(fake).route({ "to" => "eloise", "body" => "you are on call" })
raise unless fake == [["eloise", "you are on call"]]

# The real implementation conforms too — fed a stand-in socket here so the
# file runs without a network.
sock = StringIO.new
MessageRouter.new(WebSocketTransport.new(sock)).route({ "to" => "eloise", "body" => "hi" })
raise unless sock.string == "eloise:hi"

puts "fake and websocket transports both satisfy MessageRouter: OK"
