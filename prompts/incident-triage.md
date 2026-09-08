# Incident Triage

**Use case:** An alert just fired and you need a fast first read before paging anyone else.

**Inputs:** Paste the alert payload, recent relevant logs, and a one-line description of what's user-facing.

**Prompt:**
```
You are helping triage a live incident. Given the alert, logs, and description below,
answer in this order:
1. Severity assessment (SEV1-4) with one-sentence justification.
2. Most likely root cause, with confidence level.
3. Immediate mitigation steps (things to try in the next 5 minutes).
4. Who else should be paged, if anyone.

Alert: {alert}
Logs: {logs}
Description: {description}
```

**Output format:** Four numbered sections, terse, ranked by urgency.
