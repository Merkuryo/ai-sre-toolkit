# Security-Focused Code Review

**Use case:** A focused security pass on a diff, separate from a general code review.

**Inputs:** Paste the diff.

**Prompt:**
```
Review this diff for security issues only: injection risks, auth/authz bugs,
secrets in code, unsafe deserialization, missing input validation, and
dependency risks. Ignore style and non-security bugs.

Diff: {diff}
```

**Output format:** Bulleted list, each item tagged with severity (High/Medium/Low).
