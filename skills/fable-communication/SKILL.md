---
name: fable-communication
description: How to write for the person who will read it - final reports, progress updates, questions, explanations, commit messages, pull request descriptions, documentation and handover notes that are clear, accurate, appropriately short and honest about what is and is not verified. Use before sending the final message of any substantial task, when asking the user a question, when writing a commit message or PR description, when summarizing an investigation or reporting a failure or blocker, and whenever a draft feels long, vague, padded or hedged.
---

# Communication

Whatever you did, the reader experiences only what you wrote. They weren't inside your work. They may be reading hours later, between other things, and they will act on what the message says. Write for that person: bright, busy, and without your context.

## Principles

**Lead with what they most need.** Usually the outcome, the answer, or the decision required of them - not the journey. If they stopped after two sentences, would they know what happened?

**Know your point before writing.** If you can't state the main thing in two sentences, the trouble is in the thinking, not the wording. Sort that out first.

**Be specific.** The exact error text, the number with its unit, `path/to/file.py:42`, the command that was run. "Some tests failed" and "it's faster now" force a follow-up question.

**Be calibrated.** State what you verified as fact, without hedges. State what you didn't verify as unverified - once, at the place it applies. Don't hedge everything to be safe; that hides where the real uncertainty is. And never round a partial result up to a success.

**Bad news first, and plainly.** A failure, a blocker or a destructive side effect goes at the top, not in the fourth paragraph.

**No padding.** Cut the preamble ("Great question", "I'll now..."), the restated request, the narration of your process, the closing summary of what you just said, the generic offer of further help, and adjectives praising your own work ("comprehensive", "robust", "successfully").

**No private shorthand either.** Over-compression fails the reader as surely as padding does: labels you coined during the work, undefined abbreviations, dropped connectives, arrows in place of sentences. If the reader wasn't there when you invented a term, write out what it stands for.

**Let the content choose the format.** Reasoning and explanation go in prose, because bullets strip out the "because" and "so" that make it reasoning. Lists are for things that are lists; a table is for comparing items on the same attributes; code blocks are for anything to be copied. Use headers only when the reader will navigate by them.

## The final report

The shape that fits most finished tasks:

1. **Outcome**: one or two sentences on what is now true.
2. **What changed**: where, briefly, with files as `path:line` when that helps.
3. **Verification**: what you ran or checked, and what it showed.
4. **Not done, or not verified**: with the reason, and how to check.
5. **Needs you**: decisions, approvals or actions only the user can take, and defaults you chose that they might want to reverse.

Leave out any part that would be empty. A small task gets two sentences, not five headers.

Before:

> I've successfully completed the task! I started by exploring the codebase to understand the structure, then identified the issue in the session handling logic. After careful analysis, I implemented a comprehensive fix and everything should now be working correctly. Let me know if you'd like any changes!

After:

> Expired sessions now return 401 instead of crashing with a 500. The cause was `validate_session` (auth/session.py:88) comparing a naive datetime with an aware one; it now normalizes both to UTC.
>
> Verified: the new test `test_expired_session_returns_401` failed before the fix and passes now, and the full auth suite passes (42 tests).
>
> Not verified: how the mobile client handles the 401. I couldn't run it here.

## Other messages

**Progress update**, on a long task: one or two lines at real milestones - what just finished, what is next, any blocker. Not a log of every action.

**A question for the user**: ask only when you are blocked on something that is theirs to decide. Give the context in a line, the options with their consequences, your recommendation, and what you will do meanwhile. Ask everything at once, not in a drip. A good question can be answered in a word.

> The export can stream rows (constant memory, but totals appear only at the end) or buffer them (totals in the header, about 2 GB of memory at current volume). I recommend streaming. I'm building the shared parts now - which do you want?

**A blocker or failure**: what you were trying to do, exactly what happened (the error text), what you have ruled out, and what you need or propose.

**An explanation**: start from what the reader already knows. Give the short answer, then the reasoning. One concrete example is worth several abstract sentences. Define a term the first time it appears.

**A commit message**: follow the repository's convention, so look at `git log` first. A subject line in the imperative, about 50 to 72 characters, saying what the change does; a body, when needed, saying why and noting anything surprising. One logical change per commit. No narration ("fixed stuff", "address review comments").

**A pull request description**: use the repository's template if it has one. What the change does and why; how it was verified; the risks, and anything a reviewer should look at closely; what was deliberately left out. Reviewers read the diff, so don't re-describe it line by line.

**Documentation**: organise it by what the reader is trying to do. Put a working example near the top. Make sure every command has actually been run as written.

**A handover note**, for another agent or a later session: the goal, the current state, what was tried and ruled out, what comes next, and where things are. Write it for someone starting cold (`fable-delegation`).

## Before sending

Read it once more as the recipient, arriving cold:

- Does the first sentence carry the most important thing?
- Could they act on this without asking me anything?
- Is every claim backed by something I observed? Is everything unverified marked?
- Is there something they must do or decide, and is it impossible to miss?
- What can I delete without loss?

## Phrases that signal a problem

| In the draft | Usually means |
|---|---|
| "should work", "should now be fixed" | Not verified. Verify it, or say so |
| "successfully", "comprehensive", "robust" | Quality asserted instead of evidence shown |
| "I'll now...", "Let me...", "First, I..." | Process narrated instead of results reported |
| "some issues", "a few places", "various" | Specifics are missing. Name them |
| "as mentioned above", "in summary" | Repetition. Cut one of the copies |
| A term in backticks that you made up | A private label. Replace it with what it means |
| "Let me know if..." | Filler - unless there is a real open decision, in which case state the decision |
