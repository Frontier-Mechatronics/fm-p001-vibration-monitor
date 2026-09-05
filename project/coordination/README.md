# Coordination ledger

An append-only record of coordination between agents and the human engineering lead.

Messages are sent only when the human engineering lead requests one — agents may propose,
never send unprompted (AGENTS.md §14).

Its purpose is narrow: to let parties who work in different sessions — and, in ChatGPT's
case, without continuous repository access — raise questions, challenge findings and agree
on next steps in a way that survives the session and can be reviewed in the diff.

## What this is not

**The ledger is never canonical project state.** It holds no decisions, requirements,
evidence, measurements or acceptances. Those live in their existing artifacts:

| Canonical thing | Lives in |
|---|---|
| Current project state | `project/status.yaml` |
| Gate criteria and status | `project/gates/` |
| Requirements | `requirements/product.yaml` |
| Decisions | `docs/decisions/` |
| Experiments and evidence | `experiments/` |
| Human bench actions required | `project/status.yaml` (`human_actions_required`) |

Hard rules:

1. **An agreed outcome is recorded in its canonical artifact in the same change** that
   records the message agreeing to it. A message alone changes nothing.
2. **A canonical artifact must stand alone.** If understanding a requirement, gate or ADR
   requires reading a message, the artifact is incomplete — fix the artifact.
3. **A message cannot authorise physical work, select hardware, accept evidence, or mark a
   gate passed.** Only the human engineering lead does those, in the canonical artifact
   (AGENTS.md §5, §7).
4. **Never record a measurement in a message.** Reference the evidence ID. A number in a
   message has no provenance and is not evidence (`experiments/evidence.md`).
5. **A bench request goes in `status.yaml` under `human_actions_required`**, always. A
   message may point at it; a message may never be the only place it exists.
6. **Link artifacts, do not restate them.** Restated content drifts from its source.

Messages are coordination *about* the work. They are not the work.

## File naming

```text
project/coordination/YYYYMMDDThhmmssZ-<nonce>-<sender>-to-<recipient>.md
```

UTC, seconds precision, plus a 4-hex-character random nonce. Example:
`20260905T014514Z-7cb4-claude-to-codex.md`

Generate the parts, never invent them:

```sh
date -u +"%Y%m%dT%H%M%SZ"; python3 -c "import secrets; print(secrets.token_hex(2))"
```

The nonce exists solely to make collisions impossible without touching the timestamp. An
earlier version of this convention resolved a same-second collision by advancing to the next
whole second — which records a creation time that is not the creation time, in a project
whose first principle is that records are not falsified. It also still raced between
concurrent senders. **The timestamp is always the true creation time.** The nonce is a
uniqueness token, not a sequence number: nothing is counted, scanned or registered.

Sorting filenames still gives chronological order, because the timestamp leads. Grepping
`To` gives an inbox.

> Three messages written before the nonce rule (`20260905T013443Z`, `20260905T014036Z`,
> `20260905T014339Z`) have no nonce and are retained unaltered. `tools/validate_repo.py`
> requires a nonce only for messages timestamped after the rule was introduced.

Files are **never edited or deleted after they are committed.** A message that was wrong is
corrected by sending another message, not by revising history. This is the same rule that
applies to experiment records and evidence, and for the same reason.

## Parties

| Party | May send | May receive |
|---|---|---|
| `claude` | yes | yes |
| `codex` | yes | yes |
| `human` | yes | yes |
| `chatgpt` | **no** | yes |
| `all` | — | yes (broadcast) |

**ChatGPT has no direct writer in this workflow**, so no message may be filed as though
ChatGPT wrote it. Filing someone else's words under their name is impersonating an author —
the same class of defect as recording a datasheet figure as a measurement. ChatGPT's input
arrives as a **relay**: a message authored by whoever transcribed it, declaring
`Relayed from: ChatGPT` and carrying a `## Relay provenance` section that states who
supplied the material, when, whether it is verbatim or summarised, and links the source or
context. The same applies to relaying any party.

If ChatGPT later gains direct repository access, add it to the senders in
`tools/validate_repo.py` and revise this table.

## Broadcasts

`To: All` is **notification-only** and must carry `Requires response: no`. A broadcast
asking several parties for input would be closed by whichever replied first, silently
discharging the others. When independent replies are needed, send separate messages.

## Message format

Copy this. The header uses the same `| Field | Value |` table as ADRs, gate files and
experiment records.

```markdown
# <Sender> → <Recipient>: <short subject>

| Field | Value |
|---|---|
| ID | MSG-<YYYYMMDDThhmmssZ>-<nonce>-<sender> |
| From | Claude \| Codex \| Human |
| To | Claude \| Codex \| ChatGPT \| Human \| All |
| Created | YYYY-MM-DDTHH:MM:SSZ |
| In reply to | MSG-… \| none |
| Gate | Gn \| none |
| Requires response | yes \| no |
| Relayed from | ChatGPT \| … \| none (omit if not a relay) |

## Message

Concise. Link artifacts rather than restating them.

## Requested action

What the recipient is being asked to do, or `none`.

## Canonical artifacts affected

- path/to/artifact — what changed, or what is proposed to change
- `none` if this message proposes no artifact change
```

### Relay provenance

A relayed message adds this section immediately after the header. The heading alone is not
attribution — every field is required and validated.

```markdown
## Relay provenance

| Field | Value |
|---|---|
| Supplied by | who handed the material over (a party, or the person who pasted it) |
| Supplied at | YYYY-MM-DDTHH:MM:SSZ — when it was supplied |
| Fidelity | verbatim \| summarised |
| Source | link, artifact path, or a description of the context it came from |
```

`Fidelity` must be `verbatim` or `summarised`; `Supplied at` must be ISO-8601 UTC; none may
be left empty or as an unfilled placeholder. `Relayed from` is not repeated here — it is
already in the header.

The distinction `Fidelity` records is the point of the section: a reader must be able to
tell whether they are seeing the relayed party's words or the relayer's paraphrase of them.
Those carry different weight, and conflating them is how a summary becomes attributed as a
quote.

`ID` must match the filename, and `From` / `To` / `Created` must agree with it —
`tools/validate_repo.py` checks this, because a header that contradicts its filename makes
the ledger unsortable and untrustworthy.

## Threads

A reply is a new file naming the earlier message in `In reply to`. There are no threads as
objects, no inbox or outbox folders, and no status field to update — an unanswered question
is simply one with no reply pointing at it.

Open threads are therefore *derived*, not tracked. `tools/validate_repo.py` reports every
message with `Requires response: yes` that no later message replies to, so nothing needs to
be marked resolved and nothing can go stale.

Only a reply from a **different party** closes a thread. A sender following up on their own
message does not answer it — the request is still outstanding with the recipient.

## Volume

No retention rule. If the directory becomes unwieldy, archive by year into subdirectories —
messages are still discovered recursively — and never delete. Add a retention rule only when
volume is demonstrably a burden, not in anticipation of it (AGENTS.md §8).
