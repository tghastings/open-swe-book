# Chapter 6, §6.2.1 (The Modularity Principle) — information hiding.
# The same UserStore surface with two different secrets; the caller never changes.
# Run: ruby userstore_hiding.rb
require "json"

class UserStore                        # the secret: a JSON file
  def initialize(path) = @path = path
  def find(id) = load[id]
  def save(record)
    File.write(@path, JSON.dump(load.merge(record["id"] => record)))
  end
  private def load
    File.exist?(@path) ? JSON.parse(File.read(@path)) : {}
  end
end

class MemoryUserStore                  # the new secret: an in-memory table.
  def initialize = @records = {}       # There is no interface to declare or
  def find(id) = @records[id]          # implement — any object that answers
  def save(record) = @records[record["id"]] = record   # find/save will do.
end

[UserStore.new("users.json"), MemoryUserStore.new].each do |store|
  store.save({ "id" => "u7", "name" => "Kati" })  # the identical caller, untouched
  raise unless store.find("u7")["name"] == "Kati"
end

File.delete("users.json")                         # cleanup
puts "both versions satisfy the same caller: OK"
