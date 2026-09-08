#!/usr/bin/env python3
"""
postmortem_generator.py — Drafts a structured incident postmortem from raw
timeline notes (PagerDuty export, Datadog export, or plain text notes).

Usage:
    python postmortem_generator.py --source incident_notes.txt --output postmortem.md
"""
import argparse
import os
import sys

import anthropic

SYSTEM_PROMPT = """You are an SRE writing a blameless incident postmortem.
Given raw incident notes/timeline data, produce a Markdown document with these sections:

# Incident Postmortem: <short title>

## Summary
2-3 sentences: what broke, user impact, duration.

## Timeline
Bulleted, chronological, with timestamps where available.

## Root Cause
What actually caused the incident, at a technical level.

## Impact
Who/what was affected and for how long.

## What Went Well
## What Went Wrong
## Action Items
Table with columns: Action | Owner (leave blank if unknown) | Priority

Keep it blameless — describe systems and processes, not individuals' mistakes.
If information is missing, write "TBD" rather than inventing details."""


def load_source(path: str) -> str:
    with open(path, "r", errors="replace") as f:
        return f.read()


def generate(source_text: str, model: str = "claude-sonnet-4-6") -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    response = client.messages.create(
        model=model,
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": source_text}],
    )
    return "".join(block.text for block in response.content if block.type == "text")


def main() -> int:
    parser = argparse.ArgumentParser(description="Draft an incident postmortem with Claude.")
    parser.add_argument("--source", required=True, help="Path to raw incident notes/timeline.")
    parser.add_argument("--output", default="postmortem.md", help="Output Markdown file.")
    parser.add_argument("--model", default="claude-sonnet-4-6")
    args = parser.parse_args()

    if "ANTHROPIC_API_KEY" not in os.environ:
        print("Error: set ANTHROPIC_API_KEY", file=sys.stderr)
        return 1

    source_text = load_source(args.source)
    draft = generate(source_text, args.model)

    with open(args.output, "w") as f:
        f.write(draft)
    print(f"Draft written to {args.output} — review before sharing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
