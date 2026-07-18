# AOS-02 v0 Safety Correction — Human Review Checklist

**Candidate under review:** `c3db9d5848a65bf5cef3768bd1441b17244af552`

**Tree under review:** `a80a6ad3329f812441fb3a9ddb9b731a3464c101`

## Review checks

- [ ] Candidate commit and tree match the Evidence package.
- [ ] Runtime mapping v2 is accepted as an implementation mapping, not as a replacement for canonical contracts.
- [ ] Local YAML is treated as structurally evaluable but `UNTRUSTED` for human authority.
- [ ] Execution API and CLI are non-mutating and return exit `4` only for structurally valid but unavailable execution authority.
- [ ] Malformed, schema-invalid, semantic-invalid, and ordinary blocked inputs return exit `3`.
- [ ] V2 schemas are closed-world and v1 inputs are not implicitly upgraded.
- [ ] Parser limits and portability rules are acceptable for the current non-mutating profile.
- [ ] Recorded limitations are accurate and not minimized.

## Required decision

Choose exactly one:

```text
ACCEPT_NON_MUTATING_CONTROL_CORE_V0_WITH_RECORDED_LIMITATIONS
NEEDS_CHANGES_TO_NON_MUTATING_CONTROL_CORE_V0
REJECT_NON_MUTATING_CONTROL_CORE_V0
```

Acceptance does **not** authorize a trusted executor, filesystem mutation, Git write actions, push, merge, release, UI, or external integrations.
