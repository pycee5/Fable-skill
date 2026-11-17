#!/usr/bin/env python3
"""Validate and package the skills in this repository.

    python3 scripts/skills.py validate            # check every skill under skills/
    python3 scripts/skills.py package [out-dir]   # write <name>.skill archives (default: dist/)

A .skill file is a zip of one skill folder and can be uploaded to a claude.ai
account. Standard library only.
"""
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"

ALLOWED_KEYS = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}
MAX_NAME = 64
MAX_DESCRIPTION = 1024
MAX_LINES = 500
# After a context compaction only the first 5,000 tokens of a loaded skill are
# re-attached, so a SKILL.md that fits survives whole.
MAX_TOKENS = 5000
SKIP_DIRS = {"__pycache__", "node_modules"}
SKIP_FILES = {".DS_Store"}


def estimate_tokens(text):
    """Rough estimate: about 3.3 characters a token for this kind of markdown.

    Calibrated against the on-invoke figures `claude plugin details` reports for
    these skills; the usual four-characters rule reads about 20% low here.
    """
    return len(text) * 10 // 33


def read_frontmatter(text):
    """Parse the simple `key: value` frontmatter these skills use.

    Returns (fields, problems). Deliberately stricter than YAML: every value must
    be a single-line plain scalar that any YAML parser reads the same way.
    """
    problems = []
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return {}, ["no YAML frontmatter block at the top of the file"]
    fields = {}
    for line in match.group(1).splitlines():
        if not line.strip():
            continue
        pair = re.match(r"^([A-Za-z][\w-]*):\s+(\S.*)$", line)
        if not pair:
            problems.append(f"frontmatter line is not a single-line 'key: value': {line[:60]!r}")
            continue
        key, value = pair.group(1), pair.group(2).strip()
        if value[0] in "[{&*!|>'\"%@`#" or ": " in value or " #" in value or value.endswith(":"):
            problems.append(f"'{key}' would be misread by YAML (leading special character, ': ' or ' #' inside the value)")
        fields[key] = value
    return fields, problems


def packaged_files(skill_dir):
    for path in sorted(skill_dir.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(skill_dir)
        if any(part in SKIP_DIRS for part in relative.parts) or relative.parts[0] == "evals":
            continue
        if path.name in SKIP_FILES or path.suffix == ".pyc":
            continue
        yield path


def check_skill(skill_dir, known_names):
    errors, warnings = [], []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return ["SKILL.md is missing"], warnings
    text = skill_md.read_text(encoding="utf-8")

    fields, problems = read_frontmatter(text)
    errors.extend(problems)
    unexpected = set(fields) - ALLOWED_KEYS
    if unexpected:
        errors.append(f"frontmatter keys not accepted on upload: {', '.join(sorted(unexpected))}")

    name = fields.get("name", "")
    if not name:
        errors.append("frontmatter has no name")
    else:
        if name != skill_dir.name:
            errors.append(f"name '{name}' does not match its folder '{skill_dir.name}'")
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
            errors.append(f"name '{name}' is not kebab-case")
        if len(name) > MAX_NAME:
            errors.append(f"name is {len(name)} characters; the limit is {MAX_NAME}")

    description = fields.get("description", "")
    if not description:
        errors.append("frontmatter has no description")
    else:
        if len(description) > MAX_DESCRIPTION:
            errors.append(f"description is {len(description)} characters; the limit is {MAX_DESCRIPTION}")
        if "<" in description or ">" in description:
            errors.append("description contains an angle bracket")

    extra_skill_files = [p for p in packaged_files(skill_dir) if p.name == "SKILL.md" and p != skill_md]
    if extra_skill_files:
        errors.append("more than one SKILL.md in the skill folder")

    lines = text.count("\n") + 1
    if lines > MAX_LINES:
        errors.append(f"SKILL.md is {lines} lines; keep it under {MAX_LINES} and move detail to references/")
    tokens = estimate_tokens(text)
    if tokens > MAX_TOKENS:
        warnings.append(f"SKILL.md is about {tokens} tokens; only the first {MAX_TOKENS} survive a compaction")

    for markdown in [p for p in packaged_files(skill_dir) if p.suffix == ".md"]:
        body = markdown.read_text(encoding="utf-8")
        where = markdown.relative_to(skill_dir)
        for reference in sorted(set(re.findall(r"\b(?:references|scripts|assets)/[\w./-]*\w", body))):
            if not (skill_dir / reference).exists():
                errors.append(f"{where} points to {reference}, which does not exist")
        for mention in sorted(set(re.findall(r"\bfable-[a-z]+(?:-[a-z]+)*\b", body))):
            if mention not in known_names:
                errors.append(f"{where} mentions {mention}, which is not a skill in this repository")

    return errors, warnings


def skill_dirs():
    return sorted(p for p in SKILLS.iterdir() if p.is_dir())


def validate():
    directories = skill_dirs()
    known_names = {p.name for p in directories}
    failed = False
    for skill_dir in directories:
        errors, warnings = check_skill(skill_dir, known_names)
        text = (skill_dir / "SKILL.md").read_text(encoding="utf-8") if (skill_dir / "SKILL.md").is_file() else ""
        status = "FAIL" if errors else "ok"
        print(f"{status:4}  {skill_dir.name:26} {text.count(chr(10)) + 1:4} lines  ~{estimate_tokens(text):5} tokens")
        for message in errors:
            print(f"      error: {message}")
        for message in warnings:
            print(f"      warning: {message}")
        failed = failed or bool(errors)
    print(f"\n{len(directories)} skills checked: {'errors found' if failed else 'all valid'}")
    return 1 if failed else 0


def package(out_dir):
    if validate() != 0:
        print("\nNot packaging: fix the errors above first.", file=sys.stderr)
        return 1
    out_dir.mkdir(parents=True, exist_ok=True)
    print()
    for skill_dir in skill_dirs():
        archive = out_dir / f"{skill_dir.name}.skill"
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as bundle:
            for path in packaged_files(skill_dir):
                bundle.write(path, path.relative_to(SKILLS))
        print(f"wrote {archive}")
    return 0


def main(argv):
    if len(argv) >= 2 and argv[1] == "validate" and len(argv) == 2:
        return validate()
    if len(argv) >= 2 and argv[1] == "package" and len(argv) <= 3:
        return package(Path(argv[2]) if len(argv) == 3 else ROOT / "dist")
    print(__doc__.strip(), file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
