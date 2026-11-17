---
name: fable-code-architecture
description: How to make and evaluate system-level structural decisions - module and service boundaries, data models and storage, API contracts, technology choices, dependency direction, failure handling and migration paths. Use when starting a new project or service, adding a feature that spans several modules, choosing a framework, database, queue or cache, restructuring or splitting a codebase, planning a migration or rewrite, judging whether an existing architecture is sound, or writing a design doc or ADR. Use it before writing code whenever a decision would be expensive to reverse later. For design inside a single module or function use fable-code-design.
---

# Code Architecture

Architecture is the set of decisions that are expensive to change later: the data model, the boundaries between parts, the contracts between them, where state lives, and what the system depends on. The work is to find which decisions those are in this system, deliberate properly on them, and decide everything else quickly.

The commonest architectural failure is not too little structure but too much: machinery built for scale, flexibility or failure modes the system never had. The second commonest is ignoring the architecture that already exists.

## The process

### 1. Write down the forces

An architecture is an answer; get the question first. Find out, or ask, and mark assumptions where you can't:

- **What it must do**: the core use cases, a sentence each.
- **Scale, in numbers**: users, requests per second, data volume, growth - today and a plausible two years out. "Scalable" is not a requirement; "200 requests a second and 50 GB" is.
- **Qualities, ranked**: which of correctness, latency, availability, cost, time to ship, security and ease of change matter most here? They trade against each other, so the order matters.
- **Constraints**: team size and skills, the existing stack, the deployment environment, compliance, budget, deadline.

If an unknown force would change the answer, ask the user before designing.

### 2. Map what exists

In an existing system, before proposing anything: the modules and which way their dependencies point; where each kind of data lives and who writes it; how a request flows end to end; how it is deployed; the conventions the code follows. Extend the grain of what is there. A second architecture living inside the first is worse than either. If the existing structure is the real problem, say so explicitly and propose the migration as a decision of its own.

### 3. Find the expensive decisions

Sort the decisions in front of you:

- **One-way doors**: the data model and schema, public API contracts, service boundaries, the primary datastore, the consistency model, the auth and tenancy model - anything other teams or customers will come to depend on. Slow down here.
- **Two-way doors**: internal structure behind a stable interface, a wrapped library, naming, file layout. Take the conventional option and move on.

### 4. Generate real alternatives

At least two designs that differ in kind, plus the "do the least" option: extend what exists and add no new moving parts. Compare them against the ranked qualities in a small table. Write down what each makes easy and what it makes hard - every architecture makes something hard.

### 5. Choose, and prefer boring

Defaults that are right until a stated requirement says otherwise:

| Prefer | Until you can point to |
|---|---|
| A modular monolith | Parts that must scale or deploy independently, or teams that can't share a release |
| One relational database | An access pattern it measurably can't serve |
| A synchronous call | Work that is slow, bursty, or must outlive the caller |
| A library | A need for independent deployment or isolation |
| Technology the team already runs | A capability it lacks and the requirements need |
| A managed service | A cost or control problem at your actual scale |

Every queue, cache, service split or extra datastore adds failure modes, operational work and consistency problems. Each must be justified by a specific item in the forces list - not by what larger companies do, and not by what might be needed one day.

### 6. Walk it through

This is how an architecture is verified before it is built. Trace, step by step through the components:

- the main use case, end to end;
- a failure: a dependency is down, slow, or returns garbage halfway through;
- growth: ten times the load or the data - what breaks first?
- a likely change request - how many places change?
- security: where does untrusted input enter, and what checks it?

Gaps show up here: data with no owner, an operation that needs two things to be atomic, a dependency cycle. Fix the design and walk it again.

### 7. Record it and plan the path

Write the decision down - context, decision, alternatives, consequences, and what would make you revisit it. Templates are in `references/templates.md`. Then plan an incremental path: a thin vertical slice through every layer first, then widen. For a one-way door with real tradeoffs, consider `fable-agent-council` before committing, and put the decision in front of the user.

## What good structure looks like

**Boundaries**

- Divide by what changes together - usually a business capability - not only by technical layer. A feature that touches every directory signals a boundary in the wrong place.
- A module's responsibility fits in one sentence without "and". Its internals can change without its neighbours noticing.
- Modules talk through narrow, explicit interfaces - not by reaching into each other's tables, internals or globals.
- Dependencies point one way, toward the stable, domain-level code. Business rules don't import the web framework or the database driver; the outer layers depend on the core. No cycles.

**Data**

- Model the data first: entities, relationships, invariants, lifecycle. Data outlives code, so be most conservative here.
- Each piece of data has exactly one owner that writes it. Everyone else asks the owner, or reads a copy they know to be a copy.
- Know which operations must be atomic, and keep each inside one transaction boundary. If an invariant spans two stores or two services you have signed up for distributed consistency: avoid it, or design for it explicitly.
- Choose indexes and storage shape from the real access patterns. Plan how the schema will evolve: additive changes; expand, then contract.

**Contracts**

- APIs and events are promises. Design them deliberately: consistent naming and error model, pagination for anything that grows, idempotency for anything that may be retried, versioning before the first outside consumer.
- Don't let internals leak into a contract: the database's shape, library types, the meaning of internal ids.

**Failure**

For every call that leaves the process, decide what happens when it is slow, down, wrong, or succeeds twice. A timeout on everything. Retries only with backoff, and only for idempotent operations. A degraded mode where one is possible. Bounded queues, so that overload produces backpressure rather than collapse. And enough logs, metrics and traces to work out what happened at 3 a.m.

**Security**

Draw the trust boundaries. Authenticate at the edge; authorize at every operation, against the owner of the resource; give each component the least privilege it needs; keep secrets out of code and images; decide tenant isolation up front, because it is very hard to add afterwards.

**Change**

- Put seams where change is evidenced - a second implementation exists or is scheduled - not where it is merely imaginable. An interface with one implementation "in case we switch databases" is pure cost.
- Migrate incrementally. Run old and new side by side, move traffic or data in steps, and keep every step deployable and reversible. Schema changes go expand, migrate, contract. Avoid the big-bang rewrite: it fails more often than it lands.

## Anti-patterns

| Pattern | Why it hurts |
|---|---|
| Microservices for a small team or an unproven product | The costs of a distributed system with none of the benefits |
| Services sharing a database | Coupled as tightly as one program, but harder to change |
| Layers that only pass calls through | Indirection with no decision in it |
| A generic framework built before the second use case | It abstracts the wrong thing, and everything bends around it |
| A cache to hide a slow query | Now two problems: the slow query, and invalidation |
| Async or events where a function call would do | Lost stack traces; ordering and delivery problems |
| A shared "common" module that everything imports | It becomes the coupling point of the whole system |
| Choosing technology because it is new or impressive | The team pays the learning and operating cost for good |
| Rewriting instead of migrating | A long freeze, lost edge-case behavior, late surprises |

## What to hand back

For an architecture question, give: the forces as you understand them, with assumptions marked; the recommendation; the alternatives and why not; the main risks and how the design handles them; what the walk-throughs showed; and the first incremental step. Add a small component and data-flow diagram (Mermaid or plain text) when there are more than three parts. Keep it as short as the decision allows.
