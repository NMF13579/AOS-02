# Manual Workflow Demonstrator v0

```yaml
example_status: FICTIONAL_NON_AUTHORITATIVE_DEMONSTRATION
canonical_authority: NONE
grants_execution_authorization: false
grants_commit_authorization: false
grants_push_authorization: false
grants_merge_authorization: false
grants_release_authorization: false
```

This pack is a safe, fictional walkthrough of the current AOS-02 documentation/control workflow. It does **not** describe a real request, real person, real repository action, real approval, or real Evidence.

## Read the chain in this order

1. [Idea Record](idea-record.yaml) — an initial problem statement and its unknowns.
2. [Risk Profile](risk-profile.yaml) — an illustrative human-selected risk level.
3. [Scope & Change](scope-and-change.yaml) — the fictional allowed and forbidden paths.
4. [Draft Task Brief](task-brief.yaml) — a bounded proposal; it grants nothing.
5. [Human Result Decision example](human-result-decision.yaml) — a fictional acceptance of the example result, with no execution or Git grants.
6. [Evidence Report](evidence-report.yaml) — fictional observations that still require human review.

## What this demonstrates

- Each stage has a distinct role and binding.
- A Task Brief is not an execution grant.
- Evidence and technical checks are not approval.
- Human review remains explicit, even in a fully documented chain.
- Unknowns and non-grants remain visible instead of being silently treated as success.

## What this does not demonstrate

- Trusted human identity.
- A real executable task or real human decision.
- Runtime enforcement, file mutation, Git operations, push, merge, or release.
- A replacement for any accepted AOS-02 contract.

For the canonical workflow explanation, see the [Idea → Human Review v0 guide](../../workflows/idea-to-review-v0.md).