---
name: fable-debugging
description: A systematic method for finding the real cause of a bug instead of guessing - reproduce, read the evidence, form competing hypotheses, run experiments that tell them apart, fix the cause, and prove the fix. Use whenever something does not behave as expected - a failing or flaky test, an error or stack trace, a crash, wrong output, a regression, a performance problem, something that works locally but fails in CI, a build or dependency failure - and especially when a first fix attempt did not work or you notice yourself trying variations. Also use when asked to investigate, diagnose or root-cause an issue.
---

# Debugging

A bug means your model of the system is wrong somewhere. Debugging is the work of finding where. That is why guessing at fixes is slow: each guess tests one idea and teaches little when it fails. The method below is slower for the first five minutes and faster for everything after.

## The method

### 1. Reproduce it

Get the failure to happen on demand, from one command, as quickly and minimally as you can. Until you can, you can't know that anything you did fixed it.

- Capture it exactly: the command, the input, the full error text, the environment.
- Shrink it: the smallest input, the fewest steps, one test instead of the suite.
- Ideally the reproduction is a failing test. It becomes the regression test later.
- If it won't reproduce, that is information. What differs between where it fails and here: data, config, versions, timing, load, state left by earlier runs?

### 2. Read the evidence

- The whole error message and stack trace. Find the first error, not the last - later ones are usually fallout. Find the topmost frame that is in the project's own code.
- The logs just before the failure.
- What changed: `git log`, `git diff`, dependency updates, config, data, environment. A bug that appeared recently was introduced recently, and when a known-good version exists, `git bisect` finds the commit mechanically.

### 3. State the gap

One precise sentence: "Given X, I expected Y, but got Z." Vague problems get vague fixes. Check the expectation as well - sometimes the code is right and the test, the docs or your reading of the spec is wrong.

### 4. Form several hypotheses

List two or three possible causes before testing any. With a single hypothesis you will read every observation as support for it. For each one, say what it predicts that the others don't. Order them by likelihood and by how cheap they are to test.

### 5. Run experiments that tell them apart

- **Design each experiment to rule something out.** Predict the result before you run it. An experiment whose every outcome fits your theory teaches nothing.
- **Change one thing at a time.** With two changes at once you can't attribute the result.
- **Look inside instead of staring.** Print or log the real values at the boundaries between components and compare them with what you believed. The first place where belief and observation part is where the bug lives.
- **Halve the search space.** Bisect commits, the input, the config, the pipeline: check the midpoint and discard the half that is fine.
- **Check what is "obviously true".** Is this code actually running? Is it the version you just edited? Is the config being read? Is a cache, a stale build, an old process or the wrong environment involved? A large share of long debugging sessions end at one of these.

Keep a short log as you go - hypothesis, experiment, result - so that you don't repeat an experiment or walk in a circle.

### 6. Find the root cause

You have it when you can explain every observation, including the odd ones: why it fails here and not there, why it started when it did. If part of the picture is unexplained, you probably have a contributing factor, not the cause. Then ask why once more: why was this bug possible, and is the same mistake present anywhere else?

### 7. Fix the cause, where it originates

The fix belongs where the wrong value or decision is produced, which is often not where the error surfaces. These are not fixes:

- catching or suppressing the error;
- special-casing the failing input;
- a retry or a sleep wrapped around a race;
- a null check added without knowing why the value was null;
- changing the test to match the behavior.

Keep the fix minimal, and don't mix refactoring into it.

### 8. Prove it

- The reproduction from step 1 now passes.
- Where it is cheap, confirm the fix is the reason: take it out and watch the failure come back.
- Run the wider test suite. The fix must not break something else.
- Add a regression test if there isn't one.
- Search for the same pattern in sibling code.
- Remove the instrumentation you added.

If it works now and you don't know why, it isn't fixed. It is hiding.

## When you are stuck

The signal is a third attempt at the same idea, or edits getting smaller and more random. Stop, and do one of these:

- Write two columns: what you have observed, and what you assume. Go and test the assumption you trust most.
- Explain the path from input to failure step by step, in full sentences, saying what each step does. The gap usually shows up in the telling.
- Shrink the reproduction further. Delete code until the failure disappears; the last thing removed matters.
- Take the hypothesis you dismissed seriously for ten minutes.
- Read the documentation or the source of the thing you are calling, instead of inferring how it behaves.
- Ask for what only the user has: the environment, the data, what changed, how they reproduce it. Or get fresh eyes - a subagent briefed with your log (`fable-delegation`), or `fable-agent-council`.

## Where to look first, by symptom

| Symptom | Look first at |
|---|---|
| Fails in CI, passes locally | Versions; environment variables; a clean checkout versus local leftovers; OS, time zone and locale; test order and parallelism; network access |
| Flaky or intermittent | State shared between tests; order dependence; time and timeouts; concurrency; randomness; external services. Run it in a loop to get a failure rate, then isolate |
| Worked before | Bisect, then read the offending commit |
| Wrong output, no error | Trace real values through the pipeline; find the first stage whose output is wrong |
| Slow | Measure before changing anything. Profile, find the dominant cost, and look for repeated work: queries in loops, recomputation, re-rendering |
| Build or dependency error | The first error in the log; lockfile and version mismatches; a clean build; which toolchain version is really in use |
| Only in production | What differs: data shape and volume, config, concurrency, permissions. Add observability instead of guessing |
| "Impossible" behavior | You aren't running what you think you are: a stale build, a cache, the wrong file, branch, process or machine |

## Traps

- Blaming the compiler, the framework or the library first. It is nearly always the project's own code - though do confirm the installed version matches the documentation you are reading.
- Fixing where the error is raised instead of where the bad state was created.
- Ignoring the one observation that doesn't fit. It is usually the clue.
- Trusting a comment, a doc or a variable name over what the code does when run.
- Leaving several speculative changes in place because "one of them helped". Revert the ones that didn't matter.

## Reporting a fix

Give the cause in a sentence, the fix, how you know it works (the reproduction, before and after), and anything still unexplained. If you couldn't find the cause, say what you ruled out and what you would try next. That is far more useful than a fix you don't believe in.
