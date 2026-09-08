#!/usr/bin/env python3
"""
log_analyzer.py — Feed application logs to Claude and get back a plain-English
summary, anomaly flags, and suggested next steps.

Usage:
    python log_analyzer.py --file app.log
    python log_analyzer.py --file app.log --tail 500
"""
import argparse
import os
import sys

import anthropic

SYSTEM_PROMPT = """You are an SRE assistant reviewing raw application logs.
Given a log excerpt, respond with:
1. A one-paragraph plain-English summary of what happened.
2. A bulleted list of anomalies or errors worth investigating, ranked by severity.
3. Concrete next steps an on-call engineer should take.
Be concise. If the logs look healthy, say so plainly instead of inventing issues."""


def load_log(path: str, tail: int | None) -> str:
    with open(path, "r", errors="replace") as f:
        lines = f.readlines()
    if tail:
        lines = lines[-tail:]
    return "".join(lines)


def analyze(log_text: str, model: str = "claude-sonnet-4-6") -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    response = client.messages.create(
        model=model,
        max_tokens=1500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": log_text}],
    )
    return "".join(block.text for block in response.content if block.type == "text")


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze application logs with Claude.")
    parser.add_argument("--file", required=True, help="Path to the log file.")
    parser.add_argument("--tail", type=int, default=1000, help="Only analyze the last N lines.")
    parser.add_argument("--model", default="claude-sonnet-4-6", help="Model to use.")
    args = parser.parse_args()

    if "ANTHROPIC_API_KEY" not in os.environ:
        print("Error: set ANTHROPIC_API_KEY", file=sys.stderr)
        return 1

    log_text = load_log(args.file, args.tail)
    if not log_text.strip():
        print("Log file is empty.", file=sys.stderr)
        return 1

    print(analyze(log_text, args.model))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
