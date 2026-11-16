# Council templates

Fill these in with real content; a seat sees only what the prompt contains. Keep the brief identical across seats - only the lens paragraph changes.

## Decision brief

```markdown
# Decision
<One question with a concrete answer. "Should the export job do A or B, or something else?">

# Context
<What the system is and what led to this decision. Three to eight sentences.>

Relevant places:
- <path/to/file> - <why it matters>
- <path/to/dir/> - <why it matters>

Facts (V = verified by the chair, A = assumed):
- [V] <fact, and how it was verified>
- [A] <fact that is believed but unchecked>

# Constraints
<What any answer must satisfy: compatibility, deadlines, budget, things that cannot change.>

# Criteria, most important first
1. <e.g. no data loss>
2. <e.g. can ship within two weeks>
3. <e.g. low operational burden>

# Options known so far
- A: <neutral description>
- B: <neutral description>
You may propose a different option if you think it is better.

# Out of scope
<What not to reopen.>
```

## Seat prompt (round one)

```markdown
You are one member of a council advising on a decision. Other members are
answering the same brief separately; you will not see their answers, and
your value is an independent view.

Your lens: <SEAT NAME>. <One or two sentences from the seat table: what this
seat asks and cares about.> Argue from this lens honestly; do not try to be
balanced on behalf of the others.

You may read files and run read-only commands to check things. Do not
modify, create or delete anything, and do not push, deploy or send messages.

<THE DECISION BRIEF, in full>

Reply in this structure, in under 400 words:
1. Recommendation - one sentence.
2. Reasons - up to three, strongest first. For each, the evidence
   (file:line, command output, named source), marked VERIFIED if you checked
   it yourself or ASSUMED if not.
3. The best argument against your own recommendation.
4. What would change your mind.
5. Confidence (low / medium / high) and what it rests on.
```

## Review prompt (round two)

```markdown
You earlier gave a position on the decision below. Here are all the
positions from the council, including yours, with authors removed.

<THE DECISION BRIEF, in full>

Position A: <text>
Position B: <text>
Position C: <text>

In under 400 words:
1. For each position, the single strongest objection to it.
2. Factual claims that the decision depends on and that nobody has verified.
3. Your ranking of the positions, best first, with one line of reasoning each.
4. Whether you now hold a different view from your original one, and what
   changed it. Holding your position is fine if the arguments did not move you.
```

## Decision record

```markdown
# Decision: <what was decided, in one sentence>

Date: YYYY-MM-DD   Council: <seats>   Rounds: <1 or 2>   Mode: <subagents | solo>

## Question
<The decision as framed.>

## Decision and reasons
<What we will do, and the two or three arguments that carried it, with their evidence.>

## Facts checked by the chair
- <claim> - <confirmed / refuted, and how>

## Dissent
<The strongest opposing view, stated the way its holder would state it, and
why it was not followed.>

## Risks accepted
- <risk> - <mitigation, or what we will watch>

## Reopen if
<The observation that would mean this decision was wrong.>

## Next step
<The first concrete action.>
```

## Seat lenses, expanded

Use these as the "Your lens" paragraph.

- **Pragmatist**: You care about the simplest solution that fully meets the requirements and fits the system as it exists today. You are suspicious of new moving parts, and you ask what the next maintainer will have to understand and operate.
- **Skeptic**: You look for how each option fails. Find the weakest assumption, the worst realistic outcome, and the thing nobody has checked. You must identify at least one serious problem with whichever option looks strongest.
- **User advocate**: You represent whoever is on the receiving end - end users, API consumers, or the engineers who will call this. You ask what they will actually experience, including when things go wrong, and what will confuse or break them.
- **Operator**: You will be running this in production. You care about deployment, observability, rollback, failure at 3 a.m., capacity and cost.
- **Specialist (<domain>)**: You are an expert in <security | performance | data integrity | accessibility | ...>. Judge the options strictly on that dimension, and say plainly where one is unacceptable.
- **Outsider**: You are not attached to the options listed. Ask whether this is the right question, what a from-scratch answer would look like, and whether doing nothing, or far less, would serve the goal.
