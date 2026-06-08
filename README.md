# content-engine

A Claude-powered prototype named Content Engine — the little engine that can make written content consistently good.

## Why it exists

When you're running a company with a lot of content, especially documentation, it's important for the voice to be consistent across all docs. This helps with exactly that, allowing you to ensure the reader has a great experience interacting with your product or service.

## How it works in a nutshell

This utilises a local MCP server and a Claude Skill to help your work become consistent with the existing written content from your knowledge base.

It features a miniature AI content pipeline which turns rough technical notes into publication-ready, machine-readable docs while using a Skill to ensure that the tone of voice, person, and tone fit a high quality bar.

## What's here

```
content-engine/
├── server.py                    # FastMCP server: corpus + lint_style + draft_doc
├── requirements.txt
├── SKILL.md                     # the skill: process, voice, structure, output
├── style-guide.md               # full house-style ruleset + self-check
└── corpus/                      # your .md files (CV, portfolio text, past docs)
```

## The two pieces, and how they relate

- **The Skill** encodes editorial judgment: it takes messy notes and produces a doc
  in a fixed house style (second person, reasoned instructions, machine-readable
  frontmatter). This is the "writer enables everyone to write well" half.
- **The MCP server** is the infrastructure: it exposes your professional corpus as
  resources, a deterministic `lint_style` tool that programmatically enforces the
  style rules (the automated quality gate), and a `draft_doc` prompt that invokes
  the Skill.

A connected client pulls corpus context → the Skill shapes the draft → `lint_style`
catches any drift. That loop is the whole pitch in miniature.

## How to run it

**1. Create and activate a virtual environment**

On Windows:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

On Mac/Linux:
```bash
python -m venv .venv && source .venv/bin/activate
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Add your corpus**

Create a `corpus/` folder and add `.md` files — your CV, portfolio text, past docs. These become queryable resources for any connected MCP client.

**4. Try it with the MCP Inspector (no Claude Desktop needed)**

> Note: don't run `python server.py` directly — it starts the server in stdio mode and hangs waiting for a client. Use the Inspector command below instead, which launches the server and gives you a browser UI to interact with it.

```bash
npx @modelcontextprotocol/inspector python server.py
```

Open the URL it prints. Click **Connect**, then explore the tools and prompts directly in the browser UI.

**5. Connect to Claude Desktop**

Register the server in Claude Desktop's MCP config (see the [current MCP docs](https://modelcontextprotocol.io/docs/tools/claude-desktop)) and restart the app. The `draft_doc` prompt and `lint_style` tool will then be available in your Claude conversations.

## Troubleshooting

**`python` not found** — try `python3` instead, or check your PATH includes your Python installation.

**`.venv\Scripts\Activate.ps1` is blocked by execution policy** — run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` in PowerShell, then try again.

**`npx` not found** — you need Node.js installed. Download it from [nodejs.org](https://nodejs.org).

**Inspector connects but shows no tools, or errors mention the wrong Python/directory** — the Inspector may be picking up a stale config from a previous project. Make sure your venv is active and you're in the right folder before running `npx`. To be explicit about which Python to use, pass the full path:

```powershell
npx @modelcontextprotocol/inspector C:\Users\grayw\dev\claude-skills\.venv\Scripts\python.exe server.py
```

Run this from `c:\Users\grayw\dev\claude-skills` so `server.py` resolves correctly.

**`corpus://` resources return "No document named..."** — check that your files are in the `corpus/` folder next to `server.py` and have a `.md` extension.

## A few things to know

This is a prototype: one transformation, three server capabilities. Scope was chosen on purpose — the goal is to demonstrate the MCP + Skills pattern clearly, not to build a production system.

That maps directly onto the role: Claude Skills, MCP integration, machine-readable docs, automated quality gate, enabling non-writers.
