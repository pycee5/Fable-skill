---
name: fable-delegation
description: How to hand work to subagents so that it comes back right - deciding what is worth delegating, writing a brief that gives a cold-start agent everything it needs, running agents in parallel without collisions, and verifying what they return before relying on it. Use whenever you are about to spawn a subagent, split a task across parallel agents, launch a broad search or exploration, request an independent review, or act on a result that another agent produced. Also use when a delegated task came back wrong, shallow or off-target, which usually means the brief was the problem.
---

# Delegation

A subagent is a capable colleague who walks in knowing nothing: not the user's request, not what you have read, not what you already tried, not what "done" means here. Everything it gets right will come from your brief, and most of what it gets wrong will come from what the brief left out. Delegation is a writing task first.

## Whether to delegate

Delegate when:

- **The work is parallel**: independent pieces that don't need each other's results.
- **The reading is bulky but the answer is small**: a broad search, a survey of many files, a dig through logs. You want the conclusion, not the raw material, in your context.
- **You need independence**: a reviewer who didn't write the code and hasn't absorbed your reasoning.
- **It needs a different toolset or specialization** that a particular agent type has.

Do it yourself when:

- it takes two or three tool calls;
- it depends on context you would need paragraphs to transfer;
- the steps are sequential, each depending on the last;
- you would have to redo the work to trust the result;
- the session's instructions or the user restrict spawning agents. That restriction applies to every skill, this one included.

Never delegate the understanding. You stay responsible for the synthesis and the decision. "Investigate and then fix whatever you find" hands the judgment to the party with the least context.

## The brief

Cover these in sentences, not fragments. Three or four paragraphs is normal for real work.

1. **Goal and purpose**: what you want and what it serves. An agent that knows why can make the small decisions correctly.
2. **What done looks like**: the stopping condition. Without one it will stop too early or not at all.
3. **What is already known**: what you have established, what you have ruled out, what was tried and why it failed. Otherwise it will re-verify or repeat it.
4. **What makes it hard**: the obvious-but-wrong approach, the subtle trap. This is where a brief's words are best spent. An agent that isn't told will often solve an easier version of the problem and report success.
5. **Constraints**: scope; what must not be touched; read-only or not; interfaces that must not change; no pushing, deploying or messaging; any preferences inherited from the user.
6. **Where to look**: paths, entry points, commands that work in this project.
7. **What to return**: the shape that makes your next step easy. Conclusion first; evidence as `path:line`; verified facts marked apart from inferences; open questions; a length limit.

If the user's exact words matter to the task, quote them instead of paraphrasing.

Weak:

> Find out why the checkout tests are flaky and fix it.

Strong:

> I'm trying to make CI reliable. `tests/checkout/test_payment.py::test_refund_partial` fails roughly one run in five on CI and never locally. Your job is to find the cause, not to fix it yet.
>
> What I know: it fails with `AssertionError: expected 2 ledger rows, got 1` (verified in three CI logs). It is not the known Redis timeout; those runs show no timeout. I suspect test-order dependence or a missing await but have confirmed neither. Retrying the test is not an acceptable answer - I want the actual cause.
>
> Constraints: read-only. Don't modify files and don't push. You can run tests: `pytest tests/checkout -p no:randomly` runs them in fixed order, and `--randomly-seed=N` reproduces a given ordering.
>
> Return: the cause in one or two sentences; the evidence (file:line, and the command that demonstrates it); whether you reproduced the failure, yes or no; and anything you couldn't determine. Under 300 words.

## Running agents in parallel

- **Launch independent agents together**, in one message, so that they really do run concurrently.
- **Give each a separate territory.** Two agents editing the same files will overwrite each other. Partition by file or directory, or isolate them in separate worktrees, and tell each what the others are doing.
- **Fix the interfaces first.** If the pieces must fit together, decide the contract - function signatures, data shapes, file names - before anyone starts, and put it in every brief.
- **Don't wait idly, and don't poll.** Carry on with work that doesn't depend on them; you will be told when they finish. Never report a result that hasn't arrived.
- **Follow up in place.** If an agent's answer needs a correction or a further step, continue that agent with its context instead of starting a fresh one cold.
- **Size the model to the task.** Mechanical search and extraction can go to a smaller, cheaper model. Judgment, design and review deserve the strongest one available.

## When it comes back

Treat the result as evidence from a witness, not as fact. Delegated work can quietly solve an easier problem, report success on something that failed, invent a detail, or go beyond its scope.

- **Read what it actually did**, not only its summary: the diff, the commands, the output.
- **Check in proportion to the stakes.** A file listing needs a glance. A claimed root cause for a production bug needs you to open the cited lines and re-run the demonstrating command.
- **Run the checks yourself** for anything you will report as verified. "The agent said the tests pass" is hearsay until you have seen it.
- **Look for scope overrun**: files changed that weren't in the brief; actions that weren't authorized.
- **When agents disagree**, don't average them or take the majority. Find the evidence that settles it.

In your own report to the user, don't present a subagent's claim as verified unless you verified it.

## When a delegation fails

If the result is shallow, off-target or wrong, the usual cause is the brief: a missing stopping condition, an unstated constraint, an unnamed difficulty. Fix the brief and continue the agent with the correction, instead of repeating the same request and hoping. If it fails twice, do the task yourself; by then you have spent more than it would have cost.
