# §14.3.3 Feature Flags — a release flag, then the same check as a percentage rollout,
# Ruby variant. Zlib.crc32 computes the same CRC-32 as Python's zlib.crc32, so the two
# variants put every user in the same bucket.
# Runs standalone: ruby feature_flags.rb
require "zlib" # CRC-32: stable, and the same buckets as the Python version

def render_new(user_id) = "new:#{user_id}"           # stand-ins for the real pages
def render_old(user_id) = "old:#{user_id}"

def scheduler_page(user_id, flags)
  if flags["new_scheduler"]                          # release flag: one bit, everyone
    return render_new(user_id)
  end
  render_old(user_id)
end

def scheduler_page_rollout(user_id, flags)           # same conditional, new predicate
  if Zlib.crc32(user_id) % 100 < flags["new_scheduler_pct"] # stable bucket 0..99
    return render_new(user_id)
  end
  render_old(user_id)
end

users = (0...10_000).map { |i| "user#{i}" }
raise unless users.all? { |u| scheduler_page(u, { "new_scheduler" => true }).start_with?("new") }
raise unless users.all? { |u| scheduler_page(u, { "new_scheduler" => false }).start_with?("old") }
raise unless users.all? { |u| scheduler_page_rollout(u, { "new_scheduler_pct" => 0 }).start_with?("old") }
raise unless users.all? { |u| scheduler_page_rollout(u, { "new_scheduler_pct" => 100 }).start_with?("new") }
hits = users.count { |u| scheduler_page_rollout(u, { "new_scheduler_pct" => 3 }).start_with?("new") }
puts format("3%% rollout reached %d of %d users (%.1f%%)", hits, users.length, hits / 100.0)
# the same user always lands in the same bucket, across runs and processes
raise unless scheduler_page_rollout("user42", { "new_scheduler_pct" => 3 }) ==
             scheduler_page_rollout("user42", { "new_scheduler_pct" => 3 })
puts "all assertions passed"
