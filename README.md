# Fable-skill

A working method for Claude, written down as skills.

`fable-playbook` is the core: how to understand a request, plan it, break it into verifiable steps, check the result before calling it done, and report it honestly - with a table of the mistakes to watch for and how to notice each one. It is meant to be followed on every task and scales its own process to the size of the task. Nine specialist skills go deeper where the work calls for it.

## The skills

| Skill | Use it for |
|---|---|
| [`fable-playbook`](skills/fable-playbook/SKILL.md) | Every task. Size, understand, ground, plan, execute, verify, report. Routes to the others. |
| [`fable-code-design`](skills/fable-code-design/SKILL.md) | Writing or changing code: interfaces, types, naming, error handling, changing existing code safely. |
| [`fable-code-architecture`](skills/fable-code-architecture/SKILL.md) | System structure: boundaries, data model, contracts, technology choices, migrations, ADRs. |
| [`fable-ui-design`](skills/fable-ui-design/SKILL.md) | Anything a person looks at: hierarchy, layout, type, color, states, accessibility, verifying by rendering. |
| [`fable-agent-council`](skills/fable-agent-council/SKILL.md) | Hard, costly-to-reverse decisions: independent agents with different lenses, anonymous cross-review, a chair's synthesis. |
| [`fable-token-efficiency`](skills/fable-token-efficiency/SKILL.md) | Doing the same work for fewer tokens, and the false economies to avoid. |
| [`fable-debugging`](skills/fable-debugging/SKILL.md) | Finding the real cause of a bug: reproduce, hypothesize, experiment, fix the cause, prove it. |
| [`fable-verification`](skills/fable-verification/SKILL.md) | Proving work is correct: evidence by task type, tests that can fail, self-review, what to do when you can't run it. |
| [`fable-delegation`](skills/fable-delegation/SKILL.md) | Handing work to subagents: when to, how to brief, running in parallel, verifying what returns. |
| [`fable-communication`](skills/fable-communication/SKILL.md) | Reports, questions, commit messages, PR descriptions and docs that a busy reader can act on. |

`fable-ui-design` bundles two helper scripts and a starter stylesheet:

```bash
python3 skills/fable-ui-design/scripts/contrast.py "#6b7280" "#ffffff"       # WCAG contrast ratio
node skills/fable-ui-design/scripts/screenshot.cjs page.html ./shots         # phone/tablet/desktop x light/dark
```

The screenshot script needs [Playwright](https://playwright.dev) to be installed; it also reports horizontal overflow, naming the element that causes it, and console errors.

## Install

Pick the route that matches where you run Claude.

### 1. On your claude.ai account (Claude Code on the web, Cowork, chat)

Cloud sessions don't read plugins installed on your own machine or enabled in a repository's settings; they load what is saved on your claude.ai account. So add this repository there, once:

1. Open **Customize > Plugins** in claude.ai or the desktop app.
2. Choose **Add > Add marketplace** and enter `pycee5/Fable-skill`. If the repository is private, connect GitHub and give the Claude GitHub App access to it when the dialog asks.
3. Add the **Fable Playbook** plugin from the list.

The plugin then arrives in every Claude Code session as a synced plugin, with its skills named `fable:fable-playbook`, `fable:fable-debugging` and so on. Claude Code and Cowork also load its `SessionStart` hook, which tells each session that the playbook is the working method for every task; chat loads the skills and ignores the hook.

To add the skills one at a time instead, build the archives and add each to your account under **Customize > Skills**:

```bash
python3 scripts/skills.py package      # writes dist/<name>.skill, one per skill
```

### 2. As a Claude Code plugin on one machine (terminal, desktop app, IDE)

```text
/plugin marketplace add pycee5/Fable-skill
/plugin install fable@fable-skills
```

To install from a branch, add `#<branch>` to the repository: `/plugin marketplace add pycee5/Fable-skill#my-branch`.

This gives the same skills and the same `SessionStart` hook, on that machine only.

### 3. As plain skill folders

```bash
./install.sh                              # into ~/.claude/skills, for all your projects
./install.sh --project path/to/repo       # into that repo's .claude/skills, for everyone who uses it
./install.sh --always-on                  # also add the always-on instruction to CLAUDE.md
```

Copying the skills into a repository (`--project`) also works for cloud sessions on that repository, because the skills travel with the checkout.

## Making the playbook apply to every task

A skill is loaded when its description matches the work, and `fable-playbook`'s description asks for it at the start of any task. To make that a standing instruction instead of a judgment call:

- **Plugin** (routes 1 and 2): already done by the bundled `SessionStart` hook ([`hooks/`](hooks/)).
- **Skill folders** (route 3): run `./install.sh --always-on`, which appends the lines below to `CLAUDE.md`.
- **Individual account skills**: add the lines below to the `CLAUDE.md` of each repository you work in.

```markdown
## Working method

Follow the `fable-playbook` skill on every task. Load it at the start of each new task, before reading files or running commands, unless it is already in context. It scales its process to the size of the task and points to the specialist `fable-*` skills.
```

## Maintaining the skills

```bash
python3 scripts/skills.py validate     # frontmatter, size limits, links between files and between skills
claude plugin validate .               # plugin and marketplace manifests
```

Conventions the validator enforces, and the reasons for them:

- Frontmatter is `name` and `description` only, each on one line, with a description of at most 1,024 characters and no angle brackets. That is what a claude.ai skill upload accepts.
- Each `SKILL.md` stays under 500 lines and about 5,000 tokens. After a context compaction only the first 5,000 tokens of a loaded skill are re-attached, so a skill that fits survives whole. Longer material goes in `references/` and is read on demand.
- Every `references/`, `scripts/` or `assets/` path mentioned in a skill exists, and every `fable-*` name mentioned is a real skill.

Write for a capable reader: say why as well as what, prefer principles and tells to rigid rules, and keep each skill to what its reader needs when the description triggers.

`.claude-plugin/plugin.json` deliberately sets no `version`: setting one pins installed copies of the plugin to that version until it is changed.

## Layout

```text
.claude-plugin/     plugin.json and marketplace.json
hooks/              SessionStart hook that makes the playbook always-on for plugin installs
skills/<name>/      SKILL.md, plus references/, scripts/ and assets/ where a skill needs them
scripts/skills.py   validate and package
install.sh          copy the skills into ~/.claude/skills or a repository
```
