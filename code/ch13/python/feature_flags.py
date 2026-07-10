# §14.3.3 Feature Flags — a release flag, then the same check as a percentage rollout
# (canary deployment's progressive exposure implemented in code).
# Runs standalone: python3 feature_flags.py
from zlib import crc32

def render_new(user_id): return f"new:{user_id}"      # stand-ins for the real pages
def render_old(user_id): return f"old:{user_id}"

def scheduler_page(user_id, flags):
  if flags["new_scheduler"]:                        # release flag: one bit, everyone
    return render_new(user_id)
  return render_old(user_id)

def scheduler_page_rollout(user_id, flags):           # same conditional, new predicate
  if crc32(user_id.encode()) % 100 < flags["new_scheduler_pct"]:  # stable bucket 0..99
    return render_new(user_id)
  return render_old(user_id)

if __name__ == "__main__":
  users = [f"user{i}" for i in range(10_000)]
  assert all(scheduler_page(u, {"new_scheduler": True}).startswith("new") for u in users)
  assert all(scheduler_page(u, {"new_scheduler": False}).startswith("old") for u in users)
  assert all(scheduler_page_rollout(u, {"new_scheduler_pct": 0}).startswith("old")
       for u in users)
  assert all(scheduler_page_rollout(u, {"new_scheduler_pct": 100}).startswith("new")
       for u in users)
  hits = sum(scheduler_page_rollout(u, {"new_scheduler_pct": 3}).startswith("new")
       for u in users)
  print(f"3% rollout reached {hits} of {len(users)} users ({hits / len(users):.1%})")
  # the same user always lands in the same bucket, across runs and processes
  assert (scheduler_page_rollout("user42", {"new_scheduler_pct": 3})
      == scheduler_page_rollout("user42", {"new_scheduler_pct": 3}))
  print("all assertions passed")
