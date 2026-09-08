# Terraform Plan Review

**Use case:** Before applying a `terraform plan`, get a second opinion on blast radius and risk.

**Inputs:** Paste the full `terraform plan` output.

**Prompt:**
```
Review this Terraform plan output. Flag:
- Any resource being destroyed and recreated (not just updated in place)
- Any change affecting production data stores, networking, or IAM
- Anything that looks like a mistake (e.g. unexpected resource count changes)

Plan output: {plan}
```

**Output format:** Bulleted list of flags, ranked by risk. If nothing risky, say so.
