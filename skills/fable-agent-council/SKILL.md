---
name: fable-agent-council
description: Convene a council of independent AI agents to deliberate on a hard decision - several subagents with deliberately different lenses answer separately, review each other's anonymized positions, and a chair synthesizes a decision with the dissent preserved. Use when a decision is expensive to reverse and has real tradeoffs (architecture, data model, public API, migration or security design), when you are stuck after two failed approaches and need new perspectives, before an irreversible action on a critical plan or diff, or whenever the user asks for a council, a second opinion, multiple perspectives, a debate, a red team or a devil's advocate. Includes a solo mode for when subagents are unavailable or not worth their cost. Not for questions a lookup or an experiment can settle.
---

# Agent Council

A council is a way to buy independence. One mind - yours - anchors on its first idea and then mostly finds support for it. Several agents that answer separately, from different angles, surface the considerations and failure modes a single pass misses.

A council improves judgment. It does not produce facts, and it is not cheap. Use it where those properties fit.

## When to convene, and when not

Convene when all three hold:

- **Stakes**: the decision is costly to reverse, or a wrong call wastes days.
- **A real tradeoff**: there are at least two defensible options and you can't confidently rank them.
- **Judgment, not fact**: reading the code or the docs, or running an experiment, won't settle it.

Also convene when the user asks for one, or when you are stuck: two approaches have failed and you suspect your own framing.

Don't convene for:

- anything a lookup or a quick experiment answers - evidence beats opinion, so go and get it;
- cheap, reversible choices - pick one and move;
- questions of the user's preferences or priorities - ask the user;
- putting off a decision you already have enough to make.

**Cost.** Every seat is a full agent run that starts from nothing. Three seats and one round is the default; five seats or a review round only when the stakes justify it. If the session's instructions restrict spawning subagents, or the user is watching cost, a council is not an exception: run the solo form below and mention that a full council is available.

## Protocol

### 1. Frame the question

You are the chair, and the council is only as good as its brief. Seats start with none of your context, so the brief has to stand alone:

- **The decision**, as one question with a concrete answer: "Should X do A or B, or something else?"
- **Context**: what the system is, what led here, the relevant paths and facts. Mark which facts you have verified.
- **Constraints and ranked criteria**: what any answer must satisfy, and what matters most.
- **Options known so far**, stated neutrally, with an explicit invitation to propose others.
- **Limits**: what is out of scope, and what seats may do - read files and run read-only commands; change nothing.

Keep your own leaning out of it. A brief that reveals the chair's preference gets the chair's preference back.

### 2. Seat the council

Choose three lenses that pull in different directions.

| Seat | Asks |
|---|---|
| Pragmatist | What is the simplest thing that works and fits what exists? What will the next maintainer thank us for? |
| Skeptic | How does each option fail? Which assumption is weakest? What is the worst realistic outcome? |
| User advocate | What does the person on the receiving end - end user, API caller, on-call engineer - actually experience? |
| Operator | What does it take to deploy, observe, roll back and pay for this? |
| Specialist | Security, performance, data integrity, accessibility - whichever the decision turns on |
| Outsider | Is this the right question? What would a from-scratch answer, or doing nothing, look like? |

A sound default is one who builds (Pragmatist), one who breaks (Skeptic) and one who lives with the result (User advocate or Operator). Always seat a Skeptic.

Different lenses matter far more than more seats: identical agents give correlated answers that only look like consensus. Mixing models, where several are available, adds independence. For judgment-heavy questions give seats the strongest model you can - weak seats produce confident noise.

### 3. Round one: independent positions

Send every seat the same brief plus its lens, all in a single message so that they run in parallel and none sees another's answer. Independence is the whole point: a seat that has read another's answer is no longer a separate opinion.

Ask each for the same structure:

1. Its recommendation, in one sentence.
2. The strongest reasons, each with its evidence (a file and line, a command's output, a named source), marked verified or assumed.
3. The best argument against its own recommendation.
4. What would change its mind.
5. Its confidence, and what that rests on.

### 4. Round two: anonymous cross-review

Run this when round one disagrees on something material. Give each seat the full set of positions labelled A, B, C with the authors removed, and ask for: the strongest objection to each; which factual claims are load-bearing but unverified; a ranking; and whether it now changes its own position, and why. Anonymity keeps the review about the arguments rather than the roles.

One review round only. Further rounds produce agreement through fatigue, not reasoning. Skip the round altogether when the seats agree and reached that agreement through different, evidenced reasons.

### 5. Check the checkable

Before deciding, list the factual claims the decision turns on and verify them yourself: open the file, run the measurement. Seats can be confidently wrong, and several agents repeating a claim doesn't make it truer. Disagreements about facts are settled by evidence, never by votes.

### 6. Synthesize

Weigh arguments; don't count votes. One well-evidenced objection outweighs three unsupported agreements. Be suspicious of quick unanimity - seats share training and blind spots, so agreement without independent evidence is weak.

Write the decision record:

- **Decision**, and the reasons that carried it.
- **Dissent**: the strongest opposing view, stated fairly, and why it wasn't followed. Preserve it; don't smooth it away.
- **Risks accepted**, and how each will be mitigated or watched.
- **What would reopen this**: the observation that would mean the decision was wrong.
- **Next step.**

You remain accountable. "The council decided" is not a reason; the reasons are the reason.

### 7. Hand it to the user

If the decision belongs to the user - direction, cost, anything irreversible - present the recommendation with the dissent and let them decide. Give them the record, not the transcripts.

## Solo council

When subagents are unavailable or not worth their cost, run the lenses yourself, in sequence:

1. Write the brief anyway. It forces the question into shape.
2. Write each seat's position in full, one at a time, staying inside that lens.
3. Take the Skeptic last, under a rule: it must find at least one real problem with the leading option. "No significant issues" is not an acceptable finding.
4. Verify the checkable claims, then synthesize as above.

This is weaker than a real council, because the seats aren't independent of one another; say so if you report it. It is still much better than a single pass.

## How councils go wrong

| Failure | Guard |
|---|---|
| Echo: seats too alike, or a leading brief | Distinct lenses, a neutral brief, a mandatory Skeptic |
| Starved seats: generic answers because context was missing | A self-contained brief with paths and verified facts |
| Vote counting | Weigh evidence; record the dissent |
| Laundering: a guess becomes "the council's finding" | Verify load-bearing facts yourself |
| Endless deliberation | One review round, then decide |
| Council as avoidance | If you can already decide, decide |
| Seats that edit, push or send messages | A read-only instruction in every brief |
| Runaway cost | Three seats and one round unless the stakes say otherwise |

Templates for the brief, the seat prompt, the review prompt and the decision record are in `references/templates.md`. For how to write briefs in general, see `fable-delegation`.
