"""
content-engine MCP server
==========================

A miniature "AI content infrastructure" exposed over the Model Context Protocol.
Any MCP client (Claude Desktop, etc.) can connect and:

  - read your professional corpus as resources (corpus://...)
  - lint a draft against the house style  (tool: lint_style)   <-- real, deterministic
  - get a drafting prompt that invokes the technical-doc-writer skill (prompt: draft_doc)

Built on the official MCP Python SDK (`mcp`, which bundles FastMCP).
Run locally:   python server.py     (stdio transport, for Claude Desktop)

NOTE: MCP moves fast. Before a technical interview, re-check the current SDK
docs (https://github.com/modelcontextprotocol/python-sdk) so every detail is current.
"""

from pathlib import Path
import re

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("content-engine")

# --- Corpus -----------------------------------------------------------------
# Point this at a folder of your own material (CV, portfolio text, past docs).
# Exposing your own corpus is the memorable move: an agent can query and publish
# from your professional knowledge base — your "machine-parseable content" thesis,
# made literal.
CORPUS_DIR = Path(__file__).parent / "corpus"


@mcp.resource("corpus://{name}")
def get_corpus_doc(name: str) -> str:
    """Return one document from the corpus by filename (without extension)."""
    path = CORPUS_DIR / f"{name}.md"
    if not path.exists():
        return f"No corpus document named '{name}'. Add {path.name} to the corpus folder."
    return path.read_text(encoding="utf-8")


@mcp.tool()
def list_corpus() -> list[str]:
    """List the documents available in the corpus."""
    if not CORPUS_DIR.exists():
        return []
    return sorted(p.stem for p in CORPUS_DIR.glob("*.md"))


# --- Style linter (the showcase) --------------------------------------------
# Deterministic enforcement of the house style. This is the "automated guardrail"
# / "final quality gate" from the JD, in real code. Extend the heuristics over time;
# being honest that the imperative check is a heuristic is a strength, not a weakness.

BANNED_AUTHORIAL = re.compile(
    r"\b(we|we're|we've|we'd|we'll|our|ours|us|let's|lets)\b",
    re.IGNORECASE,
)

IMPERATIVE_OPENERS = re.compile(
    r"^(set|run|install|configure|create|add|deploy|click|open|select|enable|use|make|go|head|check)\b",
    re.IGNORECASE,
)

REASONING_MARKERS = re.compile(
    r"\b(because|this enables|this means|so that|so you|otherwise|if you don't|"
    r"the risk|which lets|to avoid|to ensure|this is why|enables you)\b",
    re.IGNORECASE,
)

ONWARD_MARKERS = re.compile(
    r"(want to learn more|ready for|next step|see \[|head to \[|read more)",
    re.IGNORECASE,
)


def _sentences(text: str) -> list[str]:
    # Naive splitter; good enough for linting prose. Real version could use a parser.
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


@mcp.tool()
def lint_style(draft: str) -> dict:
    """
    Check a draft against the house style and return structured findings.

    Returns a dict with a pass/fail flag and a list of issues, each with a
    rule id, the offending text, and a suggestion. Fix every issue before publishing.
    """
    issues: list[dict] = []

    # Rule 2: no authorial first-person plural
    for m in BANNED_AUTHORIAL.finditer(draft):
        issues.append({
            "rule": "no-authorial-plural",
            "match": m.group(0),
            "position": m.start(),
            "suggestion": "Rewrite in second person with the reader as subject, "
                          "or name the product as the actor.",
        })

    # Rule 4: imperatives must carry reasoning (heuristic)
    sentences = _sentences(draft)
    for i, sentence in enumerate(sentences):
        if IMPERATIVE_OPENERS.match(sentence):
            window = sentence + " " + (sentences[i + 1] if i + 1 < len(sentences) else "")
            if not REASONING_MARKERS.search(window):
                issues.append({
                    "rule": "imperative-needs-reason",
                    "match": sentence,
                    "position": None,
                    "suggestion": "Add why this step matters and what's at risk if skipped "
                                  "(heuristic flag — confirm manually).",
                })

    # Rule 6: document should end with an onward pointer
    tail = draft[-400:]
    if not ONWARD_MARKERS.search(tail):
        issues.append({
            "rule": "missing-onward-pointer",
            "match": None,
            "position": None,
            "suggestion": "Close with a deliberate next step, e.g. 'Want to learn more? See [...]'.",
        })

    return {
        "passed": len(issues) == 0,
        "issue_count": len(issues),
        "issues": issues,
    }


# --- Drafting prompt --------------------------------------------------------
# A prompt that hands the raw notes to the connected model with instructions to
# apply the technical-doc-writer skill. The Skill does the editorial work; this
# wires it into the MCP client.

@mcp.prompt()
def draft_doc(raw_notes: str) -> str:
    """Generate a prompt that turns raw notes into a house-style technical doc."""
    return (
        "Use the technical-doc-writer skill to turn the notes below into a "
        "publication-ready technical document. Obey the house style exactly: "
        "second person, no authorial we/our/let's, every instruction carries its "
        "reasoning, machine-readable frontmatter, and an onward pointer at the end. "
        "After drafting, run lint_style and fix every flag.\n\n"
        f"RAW NOTES:\n{raw_notes}"
    )


if __name__ == "__main__":
    mcp.run()  # stdio transport by default — what Claude Desktop expects
