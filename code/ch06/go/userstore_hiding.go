// Chapter 6, §6.2.1 (The Modularity Principle) — information hiding.
// The same UserStore interface with two different secrets; the caller never changes.
// Run: go run userstore_hiding.go
package main

import (
	"fmt"
	"os"
)

type User struct{ ID, Name string }
type UserStore interface { // the promise, spelled out as a type
	Find(id string) User
	Save(record User)
}

type FileStore struct{ dir string } // the secret: one small file per user
func (s FileStore) Find(id string) User {
	name, _ := os.ReadFile(s.dir + "/" + id)
	return User{id, string(name)}
}
func (s FileStore) Save(record User) {
	os.WriteFile(s.dir+"/"+record.ID, []byte(record.Name), 0o644)
}

// MemStore never says "implements UserStore" — Go interfaces are satisfied implicitly.
type MemStore map[string]User          // the new secret: an in-memory table
func (s MemStore) Find(id string) User { return s[id] }
func (s MemStore) Save(record User)    { s[record.ID] = record }

func main() {
	for _, store := range []UserStore{FileStore{os.TempDir()}, MemStore{}} {
		store.Save(User{ID: "u7", Name: "Kati"})
		fmt.Println(store.Find("u7").Name) // Kati — the identical caller, untouched
	}
	os.Remove(os.TempDir() + "/u7") // cleanup
}
