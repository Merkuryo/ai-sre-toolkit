# Kubernetes Manifest Review

**Use case:** Reviewing a Deployment/StatefulSet manifest before it ships.

**Inputs:** Paste the YAML manifest.

**Prompt:**
```
Review this Kubernetes manifest for common production issues:
- Missing resource requests/limits
- Missing liveness/readiness probes
- Containers running as root / missing securityContext
- Missing PodDisruptionBudget for a workload that needs one
- Hardcoded secrets or config that should be externalized

Manifest: {manifest}
```

**Output format:** Bulleted list of issues found, each with the fix.
