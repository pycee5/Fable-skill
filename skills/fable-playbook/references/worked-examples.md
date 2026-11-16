# Worked examples

Five tasks of different size and kind, showing what the loop looks like in practice. They illustrate proportion - how much process each size gets - and are not templates to copy.

## Trivial: "Rename the `tmp` variable in `parse_row` to `fields`"

- **Size**: trivial. No written plan.
- **Do**: read the function; rename every occurrence inside it. Check the name isn't also used in a string, a template or a nested function that should stay as it is.
- **Verify at the same scale**: re-read the function; run that module's tests, or at least a syntax or type check.
- **Report**: one line. "Renamed `tmp` to `fields` in `parse_row` (4 occurrences); the module's tests pass."

## Small: "The CSV export writes dates in US format; make them ISO"

- **Understand**: the goal is unambiguous, machine-readable dates in the export. Done means an exported file shows `2025-03-09`. Is the column a date or a timestamp? The code can answer that - look. It holds dates, so no time zone question arises.
- **Ground**: find the export code. Find how other exports format dates: there is a shared date helper used by the JSON export. Does anything read this CSV back in - an import path, a fixture, a downstream script? Search.
- **Plan (in your head)**: use the shared helper; update the test fixture; run the export tests; generate a real export and look at it.
- **Verify**: tests pass. Open the generated file and look at the column. The search for consumers of the old format found one fixture (updated) and an importer that accepts both formats.
- **Report**: the outcome, the one thing you checked that the user might not have thought of (the importer), and what was run.

## Substantial: "Add rate limiting to the public API"

- **Understand**: the goal is protecting the service from abusive clients without hurting normal ones. Unstated: the limit, what it is counted per, and the response when exceeded. Ambiguity order: the repo's config and docs say nothing; there is a conventional answer for the shape (per API key, HTTP 429 with a `Retry-After` header); the actual number is a product decision. So ask once, with a recommendation - "100 requests a minute per key, 429 with Retry-After; I'll make it configurable with that default unless you say otherwise" - and continue with everything that doesn't depend on the number.
- **Ground**: how middleware is structured here; how errors are shaped; how middleware tests are written; and how the service is deployed. If it runs as several instances, in-memory counters are wrong.
- **Riskiest assumption**: that a store shared across instances is available. Check that first.
- **Plan**:
  1. Confirm the deployment topology and the shared store -> know whether in-memory is acceptable
  2. The limiter as a pure function of (key, time, state), with unit tests for the window edges -> tests pass
  3. Wire it into one route, end to end -> a loop of real requests gets 429 after the limit
  4. Apply to all public routes; exempt health checks -> route table reviewed
  5. Configuration and docs for the limit -> documented; default matches what the user was told
  6. Full suite; two keys hammered at once -> one limited, the other unaffected
- **Verify**: the standard pass, plus the edges specific to this feature: the window boundary, a request with no API key, and the store being unavailable. That last one forces a decision - fail open or fail closed - which goes in the report for the user.
- **Report**: what was built; the defaults chosen and the fail-open decision, flagged; what was exercised; what wasn't (for example, not tested against a real multi-instance deployment).

## High-stakes: "Split the `name` column on the users table into first and last name"

- **Size**: high-stakes. It changes stored data, it is hard to reverse, and splitting names is lossy.
- **Understand**: why is the split wanted - sorting, personalisation, an integration that requires it? The reason decides how to treat names that don't split cleanly (single names, several family names). That policy is the user's call: ask before designing.
- **Ground**: every reader and writer of `name` (code, reports, exports, other services); the row count; real examples of awkward values; how migrations are run and rolled back in this project.
- **Plan** as expand, migrate, contract - each step deployable and reversible:
  1. Add the new nullable columns; write both old and new on every write -> deployed; new rows populated
  2. Backfill in batches, preceded by a dry run that reports clean splits, ambiguous cases and empties -> the user sees the ambiguous sample before the real run
  3. Switch readers over one at a time -> each verified
  4. Only after a soak period and explicit confirmation: stop writing `name`; drop it later still
- **Verification is its own step**: counts reconcile (rows in equals rows out); twenty records checked by hand, including the awkward ones; rollback rehearsed on a copy before production is touched.
- **Before anything irreversible** - the production backfill, dropping the column - state the plan, show the dry-run numbers, and get confirmation.
- If the user has no firm view on the ambiguous-name policy, that is a good question for `fable-agent-council`.

## Not code: "What were the top causes of support tickets last quarter?"

- **Understand**: the goal is deciding where to spend engineering effort. "Top" by count or by time to resolve? Default to count and say so. Done means a ranked list in which every number can be traced back to tickets.
- **Ground**: look at the data before choosing a method. Which columns exist; what date range is really present; how causes are recorded (a reliable tag, or free text); duplicates and blanks.
- **Plan**:
  1. Load and sanity-check: row count, date range, share of blanks -> matches what the export claims to contain
  2. Categorise: use the existing tags if they are reliable; otherwise define categories from a sample and state the definitions
  3. Count and rank
  4. Cross-check
- **Verify**: the categories sum to the total, with "uncategorised" reported rather than hidden; ten tickets read from the top category to confirm they belong there; the headline figure recomputed a second way.
- **Report**: the ranked list first. Then the method in two sentences, the caveats (say, 18% uncategorised; tags unreliable before March), and what would sharpen the answer.
