---
name: fable-token-efficiency
description: How to get the same quality of work for far fewer tokens - targeted reading and searching, bounded command output, batched tool calls, lean replies, sensible use of subagents and durable notes for long sessions. Use in any long or multi-step session, when working in a large codebase or with big files, logs or datasets, when the user mentions cost, usage limits, context limits or speed or wants things kept cheap, when context is filling up or has been compacted, and when designing prompts or agents whose running cost matters. It also lists the false economies that save tokens but cost correctness.
---

# Token Efficiency

Tokens are money and time, and they are also attention: a context full of irrelevant output makes the relevant parts harder to use, and a long context gets compacted, losing detail you then pay to rediscover. So efficiency improves quality as well as cost - up to the point where it starts cutting into understanding or verification. That point is the line to hold.

**The rule: spend freely on thinking and checking; economise on reading, repeating and talking.**

## Where tokens go

1. **Tool output**: file reads, command output, search results. Usually the largest share, and the easiest to cut.
2. **Re-sent context**: everything already in the conversation is carried into every later turn. Something bulky loaded early is paid for again and again.
3. **Your own output**: the most expensive tokens, and the slowest.
4. **Subagents**: each starts from nothing and builds a context of its own.
5. **Rework**: the largest waste of all - a wrong approach, a misread requirement, a debugging loop. An hour of flailing costs more than any amount of careful reading, which makes the playbook's planning and verification the main token-saving device you have.

Rough sizes, to calibrate: a line of code is on the order of ten tokens, so a 2,000-line file is around 20,000. A verbose build or test log can be several times that.

## Reading

- **Locate, then read.** Search for the symbol or string (grep, glob, a code index), then read only the relevant range of the file.
- **Read what you will change properly.** Economise on exploration, not on the target: skimming the function you are about to edit is a false economy.
- **Don't re-read what you have.** If a file is in context and unchanged, use it. After an edit succeeds, trust the tool's result rather than reading the file back.
- **Big files, logs and data: count, sample, filter.** `wc -l` first; then `head` and `tail`; `grep -n` with a little context; `jq` or `awk` to pull out the fields you need. Never print a whole log or dataset into the conversation.
- **Ask structure questions of structure tools** where they exist - a language server, a code graph, `git grep` - instead of reading files to work out who calls what.

## Commands

- **Bound the output of anything that might be long**: `| head -50`, `| tail -30`, `--quiet`, `--oneline`, `--stat`, `--name-only`, `-n 20`.
- **Tests**: run the narrowest set that covers the change first, with a reporter that shows only failures. Run the full suite once at the end.
- **Noisy tools**: turn off progress bars and banners (`--no-progress`, `-q`, `CI=1`).
- **Large output you may need again**: redirect it to a file in a scratch directory and search within it.
- **Diffs**: `git diff --stat` for the shape, then the specific files.

Don't trim so hard that you cut off the error. When a command fails, the full message is the thing most worth its tokens.

## Calls and turns

- **Batch independent calls** into one turn: several searches or reads together, not one per turn. Fewer round trips means less re-sent context and less waiting.
- **Chain dependent shell steps** with `&&` when you don't need to look in between.
- **Don't poll.** Wait for a background task's completion notice instead of checking on it.
- **Stop exploring once you can act.** Context beyond the point of sufficiency is cost with no benefit.

## Delegation

A subagent keeps its reading out of your context and returns only the conclusion. That is worth it for broad searches and bulk reading where you need the answer, not the raw material. It is not free - the agent starts cold - so:

- don't delegate what takes you two or three calls, or what depends on context only you hold;
- ask for conclusions with `path:line` references and a stated length limit, and no file dumps;
- use the smallest model that does the subtask well - mechanical search and extraction rarely need the strongest;
- respect session rules about spawning agents: where it is restricted, do the work inline.

More in `fable-delegation`.

## Your own output

- Answer first. No preamble, no restating the request, no announcing what you are about to do, no recap of what you just said.
- Don't paste back code that is already in a file; refer to it as `path:line`.
- Make targeted edits rather than rewriting whole files.
- Don't create documents, summaries or reports nobody asked for.
- Match length to the question. A one-line question gets a short answer.

## Long sessions

- **Keep durable notes** during multi-hour work: the task list, plus a short notes file for decisions, findings and the commands that worked. After a compaction, notes are far cheaper than rediscovery.
- **Leave the start of the conversation alone.** Prompt caching makes repeated context cheap only while the beginning is unchanged, so avoid anything that rewrites early context.
- **Separate tasks, separate sessions.** When the user moves to unrelated work, suggest a fresh session or clearing the context. An old task's context costs something on every turn of the new one.

## When you are designing a prompt or an agent

The same principles apply to systems you build. Keep stable instructions and tool definitions at the front, so that they cache. Retrieve what is relevant instead of stuffing everything in. Summarise or drop old history. Cap output length. Route easy steps to a smaller model and hard ones to a stronger one. Batch work that isn't urgent. Check current pricing, limits and caching rules in the provider's documentation rather than from memory.

## False economies

Savings that cost more than they save:

| Don't | Because |
|---|---|
| Skip verification | An unverified "done" that turns out wrong costs a whole extra round |
| Skim the code you are about to change | Edits made without context get redone |
| Cut off error output | The message you trimmed was the answer |
| Skip the plan | Rework is the most expensive thing there is |
| Under-brief a subagent | It will spend far more than the words you saved, on the wrong thing |
| Write a report so terse it needs a follow-up question | The follow-up costs more than the sentence would have |
| Guess an API instead of looking it up | One lookup is cheaper than a failed run and a fix |

## Quick reference

| Instead of | Do |
|---|---|
| Reading a whole file to find one function | Search for it, then read that range |
| `cat big.log` | `grep -n -m 20 ERROR big.log`; `tail -50 big.log` |
| The full test suite after every edit | The relevant tests each time; the full suite at the end |
| One tool call per turn | Independent calls together |
| Re-reading a file after editing it | Trusting the edit result |
| Pasting new code into the reply | `path:line` and a sentence |
| Printing a whole JSON response | `jq` the fields you need |
| `git log` | `git log --oneline -15` |
