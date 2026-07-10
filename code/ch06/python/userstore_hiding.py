# Chapter 6, §6.2.1 (The Modularity Principle) — information hiding.
# The same UserStore interface with two different secrets; the caller never changes.
# Run: python3 userstore_hiding.py
import json, os
import tempfile


# --- Version 1: the secret is a JSON file ---------------------------------
class UserStore:
  def __init__(self, path):
    self._path = path                     # the secret: a JSON file

  def find(self, id):
    return self._load().get(id)

  def save(self, record):
    users = self._load()
    users[record["id"]] = record
    with open(self._path, "w") as f:
      json.dump(users, f)

  def _load(self):
    if not os.path.exists(self._path):
      return {}
    with open(self._path) as f:
      return json.load(f)


with tempfile.TemporaryDirectory() as d:
  store = UserStore(os.path.join(d, "users.json"))
  # The caller — it depends only on the promise:
  store.save({"id": "u7", "name": "Kati"})
  assert store.find("u7")["name"] == "Kati"


# --- Version 2: the secret changes; the promise does not ------------------
class UserStore:
  def __init__(self):
    self._records = {}                    # the new secret: an in-memory table

  def find(self, id):
    return self._records.get(id)

  def save(self, record):
    self._records[record["id"]] = record


store = UserStore()
# The identical caller, untouched:
store.save({"id": "u7", "name": "Kati"})
assert store.find("u7")["name"] == "Kati"

print("both versions satisfy the same caller: OK")
