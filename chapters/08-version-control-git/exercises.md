# Chapter 8 — Exercises

Exercises are graded by depth: **[warm‑up]** checks understanding, **[analysis]** asks you to
reason about how Git behaves and how a team should use it.

## Concepts

1. **[warm‑up]** In one or two sentences each, define *working tree*, *staging area (index)*,
   and *repository*, and name the command that moves a change from each one to the next.

2. **[warm‑up]** Explain, in your own words, why creating a branch in Git is nearly
   instantaneous when creating one in an older tool like Subversion was slow. Your answer
   should use the phrase "a branch is a pointer."

3. **[warm‑up]** A classmate says, "Git stores the diffs between versions of my files." Correct
   the statement and explain what Git actually stores, and why the distinction matters.

4. **[warm‑up]** Distinguish `git fetch` from `git pull`. Which one changes the files in your
   working tree, and which one does not?

5. **[warm‑up]** Give one example each of a file that *should* be committed to a repository and
   a file that should be listed in `.gitignore`, and say why.

## Analysis

6. **[analysis]** You run `git add report.py`, then edit `report.py` again, then `git commit`.
   Which version of `report.py` is in the commit — the one you staged or the one now in your
   working tree? Explain using the three-areas model, and say what `git status` would show
   between the second edit and the commit.

7. **[analysis]** A teammate accidentally ran `git reset --hard` and believes a morning's
   committed work is gone forever. Explain why it very likely is *not* gone, name the command
   you would use to find it, and outline the recovery. Then state the one situation in which
   work genuinely is unrecoverable.

8. **[analysis]** Draw (by hand or in Mermaid) the commit graph for this sequence: commit A on
   `main`; branch `feature` off A; commit B on `feature`; switch to `main` and commit C; then
   merge `feature` into `main`. Label the merge commit and its parents, and explain why this
   is a three-way merge rather than a fast-forward.

9. **[analysis]** You resolve a merge conflict, but you accidentally leave one `=======` marker
   line in the file, run `git add`, and commit. What happens, and at which later stage
   (Chapter 9 review, Chapter 14 CI, or production) is this most likely to be caught? What
   habit would have prevented it?

10. **[analysis]** Your team keeps hitting large, painful merge conflicts near every deadline.
    Using the causes of conflicts from §8.5, propose three concrete changes to how the team
    works that would make conflicts smaller and rarer, and justify each in terms of *branch
    lifetime* or *overlap*.

11. **[analysis]** Explain the Golden Rule of Rebasing and construct a short scenario in which
    breaking it damages a teammate's repository. Then describe a use of rebase that is
    perfectly safe, and say what distinguishes the two.

12. **[analysis]** Your instructor requires that `main` be a protected branch. Explain what a
    protected branch is, list two rules a team might require before a merge is allowed, and
    connect each rule to a practice from another chapter (code review in §9.3, continuous
    integration in §14.2).

13. **[warm-up]** In Markdown (§8.7), write the source for: a top-level heading, a sentence
    with one **bold** and one *italic* word, a three-item bulleted list, a link, and a fenced
    code block with a language tag. Explain what the blank-line rule is and give one example
    where forgetting it breaks the output.

14. **[analysis]** Draft a `README.md` for your team project that answers every field in
    §8.7.3 (name and purpose, team, setup, run locally, run tests, deployment link, known
    limitations, AI-use log link). Then write a pull request description for one real change,
    using the *What changed / Why / How to test* structure from §8.7.4, and explain why each
    section helps the reviewer.
