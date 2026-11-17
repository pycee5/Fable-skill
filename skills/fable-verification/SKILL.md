---
name: fable-verification
description: How to prove work is correct before calling it done - choosing the right evidence for each kind of task, writing tests that can actually fail, reviewing your own diff, and reporting precisely what was and was not verified. Use before reporting any non-trivial task as complete, when writing or reviewing tests, when fixing a bug (reproduce first), when refactoring (prove behavior is unchanged), when checking data analysis, scripts, migrations, documentation or research answers, and whenever direct verification seems impossible because there is no environment, credential or test suite. Use it any time you are about to write that something works, passes or is fixed.
---

# Verification

To verify is to go looking for the observation that would prove you wrong, and fail to find it. A check that cannot fail tells you nothing. Neither does re-reading your own code and finding it convincing: you wrote it, so of course it reads as right. Ask what you would see if this were broken, then go and look for exactly that.

## The ladder of evidence

From weakest to strongest:

1. It looks right when I read it.
2. It compiles, type-checks and lints.
3. Tests I wrote alongside it pass.
4. The project's existing tests pass.
5. I exercised the real behavior end to end and saw the right result.
6. I saw it fail before the change and succeed after, under the same conditions.
7. An independent check agrees: a second method, a reviewer who didn't write it, a known-good reference.

Decide which rung the task needs - higher for anything risky - and say in your report which rung you reached. Most false "done" claims are evidence from rungs 1 to 3 reported as if it were rung 5.

## Evidence by kind of work

| Work | Evidence that counts |
|---|---|
| Bug fix | A reproduction that fails before and passes after; a regression test; the wider suite still green |
| New feature | Each acceptance criterion exercised through the real entry point (UI, CLI, HTTP), including its error paths |
| Refactor | The same tests pass before and after without being edited. No tests? Write characterization tests first, or diff the outputs on real inputs |
| UI | Rendered and looked at, at several widths and in each theme; states clicked through; keyboard used (`fable-ui-design`) |
| Data analysis | Row counts in and out reconcile; totals match a known figure; nulls and duplicates accounted for; joins didn't multiply rows; a few records traced by hand; the headline number recomputed a second way |
| Script or automation | A dry run; a run on a copy or a sample; a second run (is it idempotent?); an interruption midway (what state is left?) |
| Migration | Run on a copy; counts and checksums reconcile; rollback tested; the application works against the new shape |
| Config or infrastructure | Confirmed as loaded and in effect in the running system, not merely present in the file |
| Performance | Measured before and after, in the same conditions, over several runs; the number reported with its spread |
| Documentation | Your own instructions followed literally from a clean state; every command pasted and run; links resolve |
| Research or factual answer | Each claim traced to a source you opened; the source says what you say it says, and is current; inference labelled as inference |

## Tests worth having

- **See it fail first.** Write the test before the fix, or break the code on purpose and confirm the test notices. A test never seen failing may be testing nothing.
- **Test behavior, not implementation**: inputs and observable outputs, through the public interface. Tests coupled to internals break on every refactor and stop being trusted.
- **Cover the edges**, which is where the bugs are: zero, one, many; empty and missing; boundaries and just past them; malformed input; the error path; the exact case from the bug report.
- **Mock only at the system's edge**: network, clock, filesystem, third parties. A test that mocks the thing it is testing passes by construction.
- **Deterministic and independent**: no real time, randomness or network, and no reliance on test order.
- **One reason to fail**, and a name that states the behavior: `rejects_expired_token`, not `test_auth_2`.
- **Follow the project's conventions**: its framework, layout, fixtures and helpers.
- Don't chase coverage numbers with tests that assert nothing, and don't snapshot large outputs nobody will read when they change.

## Lines not to cross

These turn a red check green without making the work correct, and they destroy the check's value for everyone who comes after:

- editing, deleting, skipping or loosening a failing test so that it passes;
- hard-coding the expected output, or special-casing the test's input;
- catching an error to silence it;
- reporting a pass from a run made before your last edit;
- writing "tests pass" when only some were run. Say which.

If a test is itself wrong, changing it can be right - but say so explicitly in the report, with the reason. That is a decision the user should see.

**Failures that were already there**: when it is cheap, run the checks before you change anything, so that you know the baseline. Report pre-existing failures separately. Don't fix them silently, and don't let them hide yours.

## Reviewing your own diff

Read `git diff` (or re-read the document) from top to bottom, as a reviewer who expects problems. For each hunk:

- Does the task require it? If not, take it out.
- What input breaks it?
- What else depended on the old behavior? Search for the uses.
- Is anything left behind: debug output, commented-out code, a TODO, a stub, a hard-coded value?
- Is anything missing: a new file not added, a test, a doc or config update, a migration?

Then ask the question that finds the most bugs: if this is wrong, where is it most likely wrong? Go and test that place specifically.

For high-stakes work, get independence: a reviewer subagent that sees only the diff and the requirements, not your reasoning (`fable-delegation`).

## When you can't verify directly

No environment, no credentials, it needs production, there is nothing to run it on. Don't give up, and don't pretend.

1. **Close as much of the gap as you can**: static checks, a dry run, a smaller local reproduction, a unit test around the piece you can isolate, a careful trace of the code path with concrete values.
2. **Try to make it runnable** - install the dependency, start the service, write the tiny harness - before concluding that it can't be run. "Couldn't run the tests" should be a finding with a reason, not a default.
3. **State the remainder precisely**: what is unverified, why, and the exact command or steps by which the user can verify it.

## Reporting verification

Say what you did, not how you feel about it:

> Verified: `pytest tests/auth` - 42 passed, including the new `test_rejects_expired_token`, which failed before the fix. A real request to `/me` with an expired token against the dev server returned 401.
>
> Not verified: behavior behind the production load balancer (no access). To check: request `/me` there with an expired token and expect 401.

"Should work", "looks good" and "I believe" are signs that the checking hasn't been done yet.
