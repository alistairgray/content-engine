# House Style Guide

This is the full ruleset for the `technical-doc-writer` skill. The SKILL.md carries the summary; this file carries the detail and the worked examples. Apply every rule, then run the self-check at the end.

## 1. Person and subject

The reader is the subject of the sentence.

- Yes: "Here you will configure the build pipeline."
- Yes: "Next you need to set the region, and this is why it matters."
- No: "In this section we configure the build pipeline."
- No: "Let's set the region."

## 2. Banned: first-person plural (authorial)

Never use, as the narrator: `we`, `we're`, `we've`, `we'd`, `we'll`, `our`, `ours`, `us`, `let's`, `lets`.

This is the single most common drift. Drafts obey it in paragraph one and break it by paragraph three. Check the whole document, not just the opening.

## 3. The product/company may act

The ban is on the *authorial* voice, not on naming the actor performing a step. The product, the platform, or a named tool can be the subject of an action.

- Yes: "Upsun provisions the environment in seconds."
- Yes: "The pipeline scrapes the page and flags the change."
- No: "We provision the environment for you." (authorial "we")

## 4. Every instruction carries its reasoning

No bare imperatives. Each instruction follows the shape:

> what to do → why it matters → what's at risk if skipped → how to prioritise it

Worked example:

> **Bare (rejected):** "Set the region before deploying."
>
> **Reasoned (accepted):** "Set the region before you deploy. This pins your data to the correct jurisdiction; skip it and you risk a compliance violation that is slow and costly to unwind, so make it one of the first things you do."

Reasoning markers that signal a rule is satisfied: *because, this enables, this means, so that, otherwise, if you don't, the risk is, which lets you*. A sentence opening with an imperative verb and containing none of these is probably a bare command — add the why.

## 5. Tone

Active, friendly, direct. Short sentences over long ones. Address the reader as a capable peer, not a novice to be managed.

## 6. Onward pointer

Close sections and the document with a deliberate next step. This is a navigation feature: it keeps the reader moving and it gives AI agents an explicit link graph to follow.

- "Want to learn more? See [Configuring environments]."
- "Ready for the next step? Head to [Deploying your first app]."

## Self-check (run before returning)

- [ ] No authorial `we / our / us / let's` anywhere in the document.
- [ ] Every instruction has a reason and, where relevant, a stated risk.
- [ ] The reader is the subject of the sentence throughout.
- [ ] Code blocks contain real, correct syntax — no invented APIs or flags.
- [ ] Frontmatter is present and complete (title, audience, summary, related).
- [ ] The document ends with an onward pointer.
