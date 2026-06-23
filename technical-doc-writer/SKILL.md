---
name: technical-doc-writer
description: Turn rough technical notes or changelogs into publication-ready docs in a fixed house style: second person, reasoned steps, machine-readable frontmatter. Use when writing technical docs.
---

# Technical Doc Writer

This skill turns rough input into a finished technical document that obeys a strict house style. The goal is a doc a developer trusts and enjoys: reader-centric, every instruction justified, and structured so both humans and AI agents can parse it.

## Process

Follow these steps in order. Do not skip the self-check — it is the quality gate.

1. **Intake.** Read the raw input. Identify the reader (who is this for?), the task (what will they accomplish?), and any code, commands, or config that must appear and must be correct.
2. **Structure.** Lay the doc on a narrative spine — the reader's journey from start state to goal — not a flat feature list. Break it into problem-framed sections (see Structure below).
3. **Draft.** Write each section in the house voice. Put real, correct code in fenced blocks. Never invent an API, flag, or command; if the input is ambiguous, mark it `<!-- TODO: confirm -->` rather than guessing.
4. **Add metadata.** Emit YAML frontmatter so the doc is machine-readable and agent-consumable (see Output below).
5. **Self-check.** Run every rule in `references/style-guide.md` against the draft. If the `lint_style` MCP tool is available, run it and fix every flag before returning.

## House voice (summary — full rules in references/style-guide.md)

- **Second person, reader as subject.** "Here you will learn…", "Next you need to…". The reader is the subject of the sentence, never the author.
- **No first-person plural as narrator.** No "we", "our", "us", "let's". This is absolute.
- **The product can act.** Naming the product as the actor is fine: "Upsun provisions the environment in seconds." The ban is on the *authorial* voice only.
- **Every instruction carries its reasoning.** Never a bare command. The pattern is: what to do → why it matters → what's at risk if skipped → therefore how to prioritise it. Example: "Set the region before you deploy. This pins your data to the right jurisdiction; skip it and you risk a compliance violation that is painful to unwind, so treat it as a first step, not a detail."
- **Active, friendly, direct.**
- **End with an onward pointer.** Close sections or the doc with a deliberate next step: "Want to learn more? See [related doc]." Treat this as navigation, not a sign-off.

## Structure

Shape the doc as a journey, using this repeatable pattern:

- **Opening:** Tell the reader what they will learn and why it matters to them. One short paragraph.
- **Body sections:** One section per problem or milestone. Where useful, frame the section header in the reader's own voice ("You need to store more than engineering values"). Within each: state the situation, give the steps with reasoning, show correct code, state the outcome.
- **Close:** Confirm what the reader can now do, then the onward pointer.

## Output

Return a single Markdown file with this frontmatter, then the body:

```yaml
---
title: <clear, reader-facing title>
audience: <who this is for>
summary: <one sentence; used by search and AI agents>
prerequisites: [<list>]
related: [<paths or titles of onward docs>]
last_reviewed: <YYYY-MM-DD>
---
```

The `summary`, `audience`, and `related` fields are what make the doc agent-consumable: an AI agent can route, link, and surface the doc from these without parsing the prose.

## Guidelines

- Prefer fewer, correct code blocks over many illustrative-but-vague ones.
- If a step has no real reason, it is probably not a real step — cut it.
- Keep the reader moving forward; every paragraph should advance the task.
