# Architecture templates

Use the lightest one that carries the decision. A two-way door rarely needs any of these; a one-way door usually deserves the decision record.

## Decision record (ADR)

```markdown
# ADR-NNN: <the decision, in a few words>

Status: proposed | accepted | superseded by ADR-XXX
Date: YYYY-MM-DD

## Context
The need, the constraints and the numbers. What makes this a decision
rather than an obvious choice.

## Decision
What we will do, in one or two sentences. Then the detail.

## Alternatives considered
For each: what it is, what it would make easy, and why it was not chosen.

## Consequences
What becomes easier. What becomes harder. What we are now committed to.
Risks accepted, and how each is watched or mitigated.

## Revisit when
The observation that would mean this decision should be reopened.
```

## Options table

Rows are the ranked qualities from the forces list, most important first, followed by the three rows that are always worth filling in.

```markdown
|                      | Option A | Option B | Do the least |
|----------------------|----------|----------|--------------|
| <top-ranked quality> |          |          |              |
| <second quality>     |          |          |              |
| <third quality>      |          |          |              |
| New moving parts     |          |          |              |
| Reversibility        |          |          |              |
| What it makes hard   |          |          |              |
```

## Lightweight design doc

```markdown
# <feature or system>

## Problem and goals
## Non-goals
## Forces
Requirements with numbers; qualities, ranked; constraints. Assumptions marked as such.
## Current state
## Proposed design
- Components and their responsibilities
- Data model and ownership
- Contracts (APIs, events)
- Failure handling
- Security
## Alternatives
## Walk-throughs
Main path; a failure; ten times the load; a likely change request.
## Rollout
Incremental steps, each deployable and reversible.
## Open questions
```
