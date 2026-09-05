# Independent reviews

This directory retains independent review records that are required by an engineering-gate
criterion. It is not a project-state system: gate status remains canonical in
[`project/status.yaml`](../status.yaml), and each review is linked from the relevant gate.

Keep a review concise, date it, identify the reviewer and scope, distinguish findings from
changes made, and state what remains for human acceptance. Do not copy project status here.

| Review | Reviewer | Gate | Result |
|---|---|---|---|
| [G0-codex-review-2026-09-05.md](G0-codex-review-2026-09-05.md) | Codex — Lead Tester / Reviewer | G0 | Suitable with minor changes; corrections applied before acceptance |
| [G0-chatgpt-review-2026-09-05.md](G0-chatgpt-review-2026-09-05.md) | ChatGPT — Solution Architect | G0 | Ready to pass; no finding required a change before G0 |

A review record is filed verbatim as the reviewer wrote it. Where a review's findings need
action, that action is recorded in the artifact that owns it — not left in the review.
