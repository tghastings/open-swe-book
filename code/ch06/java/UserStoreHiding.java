// Chapter 6, §6.2.1 (The Modularity Principle) — information hiding.
// The same UserStore interface with two different secrets; the caller never changes.
// Run: java UserStoreHiding.java
import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.Map;

public class UserStoreHiding {
  public static void main(String[] args) throws IOException {
    Path dir = Files.createTempDirectory("users");

    UserStore store = new FileUserStore(dir);   // or new MemoryUserStore() — can't tell
    store.save(new User("u7", "Kati"));         // the identical caller, untouched
    System.out.println(store.find("u7").name()); // Kati

    // The identical caller again, against the other secret:
    store = new MemoryUserStore();
    store.save(new User("u7", "Kati"));
    System.out.println(store.find("u7").name()); // Kati

    Files.deleteIfExists(dir.resolve("u7"));    // cleanup
    Files.deleteIfExists(dir);
  }
}

interface UserStore {                          // the promise, spelled out as a type
  User find(String id);
  void save(User record);
}
record User(String id, String name) {}

record FileUserStore(Path dir) implements UserStore { // the secret: one file per user
  public User find(String id) {
    try { return new User(id, Files.readString(dir.resolve(id))); }
    catch (IOException e) { return null; }     // unknown id — no such file
  }
  public void save(User record) {
    try { Files.writeString(dir.resolve(record.id()), record.name()); }
    catch (IOException e) { throw new UncheckedIOException(e); }
  }
}

class MemoryUserStore implements UserStore {   // the new secret: an in-memory table
  private final Map<String, User> records = new HashMap<>();
  public User find(String id) { return records.get(id); }
  public void save(User record) { records.put(record.id(), record); }
}
