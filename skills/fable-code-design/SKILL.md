---
name: fable-code-design
description: How to design code at the level of functions, types, modules and interfaces so that it is correct, simple and fits the codebase it lives in. Use whenever writing or changing code - implementing a feature, adding a function or class, designing an API or data type, choosing names, deciding how to handle errors, refactoring, or reviewing code quality - even for small changes, because most design damage is done in small changes. For system-level structure (services, data stores, boundaries across a codebase) use fable-code-architecture instead.
---

# Code Design

Good code design is mostly restraint: the smallest change that is fully correct, written the way this codebase already writes things. The reader of your code is someone fixing a bug in it a year from now, with no memory of this task. Design for them.

## Before writing

1. **Read the neighbourhood.** The file you are changing, its callers, its tests, and one sibling that does something similar. Note the local conventions: naming, error style, file layout, test style, how dependencies are passed in.
2. **Write the call site first.** Sketch how the new thing will be used before deciding how it works. An interface designed from the caller's side is nearly always simpler than one that grows out of the implementation.
3. **Get the data shape right.** Decide what the data is - its types, its invariants, who owns it - before the functions. When the data structures are right the code tends to be obvious; when they are wrong, no amount of clever code rescues it.

## Principles, in priority order

When they conflict, the earlier one wins.

### 1. Correct, including the unhappy paths

Handle the cases the requirements imply: empty, missing, malformed, duplicate, too large, and failure of whatever you call. Code that handles only the happy path isn't finished.

### 2. Consistent with the codebase

Local consistency beats your preference, and beats general best practice. Use the existing patterns, helpers, libraries and vocabulary. If the codebase returns result types, don't throw; if it has a repository layer, don't query from the handler. A second way of doing something is a cost paid by every later reader. If an existing pattern is actually harmful, say so and ask - don't start a quiet migration.

### 3. Simple

- Build what the requirement needs now. No options nobody asked for, no extension points for imagined futures, no abstraction with a single implementation.
- Wait for the third occurrence before abstracting. Two similar blocks are cheaper than the wrong abstraction, which is very hard to remove once things depend on it.
- Prefer plain data and plain functions to class hierarchies, plain control flow to cleverness, and the standard library to a new dependency.
- Simple is not the same as short. A dense one-liner is not simpler than four clear lines.

### 4. Hard to misuse

- **Narrow interface, deep implementation.** A module should hide a decision. If callers must know how it works inside in order to call it correctly, the interface is leaking.
- **Make illegal states unrepresentable.** Prefer a type that cannot hold a bad value to a check that catches one: an enum instead of a string; one `status` field instead of three booleans that can contradict each other; a required parameter instead of an optional one with a magic default.
- **Parse at the boundary.** Convert untrusted input into a well-typed value once, at the edge; inside, trust the type. Don't re-validate the same thing at every layer.
- **No flag parameters that select behavior.** `render(doc, true, false)` is unreadable where it is called. Make two functions, or pass a named option.
- **One source of truth.** Store each fact once and compute the rest. Duplicated state drifts.

### 5. Easy to read

- **Names** say what a thing is or does, in the domain's vocabulary, with one word per concept used everywhere. Length in proportion to scope. No abbreviations a newcomer would have to ask about. Booleans read as assertions (`isExpired`), functions as actions (`parseHeader`).
- **Functions** do one thing, at one level of abstraction. Keep computation apart from I/O: a core that takes values and returns values, wrapped in a thin shell that reads and writes. That shape is also what makes code testable.
- **Control flow**: early returns for the exceptional cases, the main path left unindented. State in the smallest scope that works; immutable values by default.
- **Comments** explain why: a constraint, a non-obvious decision, a trap. Not what the code already says, and not the history of your change ("added for the login bug" belongs in the commit message). Don't leave commented-out code.

## Errors

- Handle each failure where something useful can be done about it. Elsewhere, let it propagate, with context added.
- Validate at trust boundaries: user input, network, files, other services. Don't add defensive checks for states that internal code can't produce - they hide bugs and bury the logic. If you want the invariant documented, assert it.
- Fail early and loudly. Never swallow an error (`catch {}`, `except: pass`), return a made-up default, or log and carry on into corrupted state.
- An error message says what happened, includes the offending value, and says what was expected - enough for someone to act on without a debugger.
- Release what you acquired on every path: files, locks, connections, transactions.

## Changing existing code

- **The smallest diff that is fully right.** Don't reformat, rename or reorganise what you weren't asked to touch. It buries the real change and creates merge conflicts.
- **Keep refactoring and behavior change apart** - separate steps, ideally separate commits. Mixed together, neither can be reviewed or verified.
- **Preserve behavior you weren't asked to change**, including odd behavior. Find out why a strange line exists (history, tests, callers) before removing it.
- **Change all of it.** When a signature, name or contract changes, find every use: callers, tests, types, docs, config, serialized data.
- **Compatibility is a decision.** Don't break a public contract silently; equally, don't add shims and fallbacks for callers that don't exist.
- **Remove what your change made dead**, in the same change.

## Easy to get wrong by default

- **Injection**: never build SQL, shell commands, file paths or HTML by concatenating untrusted input. Use query parameters, argument arrays, path joins with a containment check, and escaping.
- **Secrets**: never in code, logs, error messages or commits.
- **Authorization**: checked on the server at every entry point, not only hidden in the UI.
- **Accidental cost**: a query inside a loop, a nested loop over large inputs, a whole file or table read into memory. Avoid these by default; beyond that, measure before optimizing.
- **Time, money, text**: time zones and daylight saving, floating-point currency, unicode and encodings. Use the proper types and libraries.
- **Concurrency**: shared mutable state, check-then-act races, retries of operations that aren't idempotent.
- **Dependencies**: adding one is a design decision. Prefer what the project already has; check that a new one is maintained, compatibly licensed and worth its weight.

## Tests are design feedback

If something is hard to test, the design is telling you it has hidden inputs or does too much. Fix the design rather than reaching for heavier mocks. Test behavior through the public interface, so that the tests survive refactoring. More in `fable-verification`.

## Review your own design

Before calling it done, read the diff and ask:

- Could a newcomer follow this without me explaining it?
- Is anything here that the requirements didn't ask for?
- Does it look like the code around it?
- What happens with empty, missing, huge or malformed input, and when the thing I call fails?
- Can a caller use this wrongly? Could the types prevent that?
- Did I change every use of what I changed?
- Is there now any dead code, duplicated logic or second source of truth?

## Smells and what they usually mean

| Smell | Usual cause | Move |
|---|---|---|
| A function needs a comment for each block | It does several things | Split it along the comments |
| Many parameters, or several booleans | A missing concept | Introduce a type, or split the function |
| The same edit needed in many places | Knowledge duplicated | One source of truth |
| A `utils` / `helpers` / `manager` that keeps growing | No real home was found | Put each function beside the data it works on |
| Deep nesting | Exceptional cases mixed into the main path | Guard clauses; extract |
| Mocks everywhere in a test | Logic tangled with I/O | Pure core, thin shell |
| A wrapper that only forwards | An abstraction with no decision inside it | Delete it |
| "Just in case" branches | An unclear contract | Decide the contract and assert it |
