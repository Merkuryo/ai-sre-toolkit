#!/usr/bin/env python3
"""
pr_reviewer.py — Posts an AI-generated review comment on a GitHub pull request,
focused on bugs, security issues, and performance red flags.

Designed to run as a step in a GitHub Actions workflow, but works standalone
with a GitHub personal access token.

Usage:
    python pr_reviewer.py --repo owner/repo --pr 42
"""
import argparse
import os
import sys

import anthropic
import requests

SYSTEM_PROMPT = """You are a senior engineer reviewing a pull request diff.
Focus only on: correctness bugs, security issues, and performance problems.
Do not comment on style or naming unless it causes a real bug.
Format your response as a short list of findings. If you find nothing
significant, say so in one sentence — do not invent issues to fill space."""

GITHUB_API = "https://api.github.com"


def fetch_diff(repo: str, pr: int, token: str) -> str:
    url = f"{GITHUB_API}/repos/{repo}/pulls/{pr}"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3.diff"}
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.text


def review_diff(diff_text: str, model: str = "claude-sonnet-4-6") -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    response = client.messages.create(
        model=model,
        max_tokens=1500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": diff_text[:50_000]}],
    )
    return "".join(block.text for block in response.content if block.type == "text")


def post_comment(repo: str, pr: int, body: str, token: str) -> None:
    url = f"{GITHUB_API}/repos/{repo}/issues/{pr}/comments"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    resp = requests.post(url, headers=headers, json={"body": body}, timeout=30)
    resp.raise_for_status()


def main() -> int:
    parser = argparse.ArgumentParser(description="AI code review for a GitHub PR.")
    parser.add_argument("--repo", required=True, help="owner/repo")
    parser.add_argument("--pr", required=True, type=int, help="Pull request number")
    parser.add_argument("--model", default="claude-sonnet-4-6")
    parser.add_argument("--dry-run", action="store_true", help="Print review instead of posting.")
    args = parser.parse_args()

    for var in ("ANTHROPIC_API_KEY", "GITHUB_TOKEN"):
        if var not in os.environ:
            print(f"Error: set {var}", file=sys.stderr)
            return 1

    token = os.environ["GITHUB_TOKEN"]
    diff = fetch_diff(args.repo, args.pr, token)
    review = review_diff(diff, args.model)

    header = "### 🤖 AI Review\n\n"
    body = header + review

    if args.dry_run:
        print(body)
    else:
        post_comment(args.repo, args.pr, body, token)
        print(f"Posted review comment on {args.repo}#{args.pr}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
