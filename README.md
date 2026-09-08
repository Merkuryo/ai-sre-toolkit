# AI SRE Toolkit

A small suite of Claude-powered command-line tools for common SRE/DevOps tasks: log triage, PR review, incident postmortems, and a reusable prompt library.

Each tool is a standalone script — use what you need, no framework lock-in.

## Tools

### `log_analyzer.py`
Feeds application logs to Claude and returns a plain-English summary, anomaly flags, and suggested next steps.

```bash
python log_analyzer.py --file app.log
```

### `pr_reviewer.py`
Posts an AI-generated review comment on a GitHub pull request, focused on bugs, security issues, and performance red flags. Designed to run as a GitHub Action step.

```bash
python pr_reviewer.py --repo owner/repo --pr 42
```

### `postmortem_generator.py`
Pulls timeline data from an incident (PagerDuty export, Datadog export, or a plain log/notes file) and drafts a structured postmortem — ready to edit and publish.

```bash
python postmortem_generator.py --source incident_notes.txt --output postmortem.md
```

### `prompts/`
A curated library of prompt templates for recurring SRE tasks: incident triage, Terraform plan review, Kubernetes manifest review, and security-focused code review. Each template documents the inputs it expects and the format of the output.

## Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your-key-here
```

## Why this exists

Most AI coding assistants are optimized for writing new code. These tools are optimized for the parts of the job that aren't writing code: reading logs at 3am, reviewing someone else's PR, and writing the postmortem nobody wants to write. They're deliberately small and readable — each one is a single file you can understand in five minutes and adapt to your own stack.

## License

MIT
