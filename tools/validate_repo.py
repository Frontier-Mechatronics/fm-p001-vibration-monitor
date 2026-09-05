#!/usr/bin/env python3
"""Structural self-consistency check for the FM-P001 repository harness.

Checks that the harness artifacts are internally consistent: identifiers are
well-formed and unique, requirements are traced, ADRs have their required
sections, project status points at real files, every directory has a documented
purpose, and relative links resolve.

What it deliberately does NOT check: whether any of the content is *true*. It
cannot tell an honest measurement from a fabricated one, or a sound requirement
from a bad one. That is a human and reviewer responsibility (AGENTS.md §9).

Usage:
    python3 tools/validate_repo.py [--repo <path>]

Exit status: 0 if no errors, 1 otherwise. Warnings do not fail the run.
Requires PyYAML.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date, datetime
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - environment issue, not a repo defect
    sys.exit("PyYAML is required: pip install pyyaml")

REQ_ID = re.compile(r"^SV-(SYS|ACQ|DSP|STO|COM|GW|CLD|HW|OPS)-\d{3}$")
GATE_ID = re.compile(r"^G\d{1,2}$")
EXP_DIR = re.compile(r"^EXP-(\d{4})-[a-z0-9][a-z0-9-]*$")
EXP_ID = re.compile(r"^EXP-\d{4}$")
ADR_FILE = re.compile(r"^ADR-(\d{4})-[a-z0-9][a-z0-9-]*\.md$")
EVIDENCE_ID = re.compile(r"^(CAP|DATA|IMG|MEAS|LOG)-\d{4}$")
MSG_FILE = re.compile(
    r"^(\d{8}T\d{6}Z)(?:-([0-9a-f]{4}))?-([a-z]+)-to-([a-z]+)\.md$")
MSG_ID = re.compile(r"^MSG-\d{8}T\d{6}Z(?:-[0-9a-f]{4})?-[a-z]+$")

# ChatGPT has no direct writer in this workflow, so it can never be a sender: a
# message carrying ChatGPT's words is authored by whoever transcribed it and
# declares `Relayed from`. Add chatgpt here only if it gains repository access.
SENDERS = {"claude", "codex", "human"}
PARTIES = SENDERS | {"chatgpt"}
RECIPIENTS = PARTIES | {"all"}

# Filenames gained a random nonce at this instant (MSG-20260905T014514Z-7cb4-claude).
# Messages written before it predate the rule and are retained unaltered.
NONCE_REQUIRED_FROM = "20260905T014500Z"

# A relayed message must carry an attribution trail, not just a heading.
RELAY_FIELDS = ("Supplied by", "Supplied at", "Fidelity", "Source")
FIDELITY = {"verbatim", "summarised"}
ISO_UTC = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
PLACEHOLDER = re.compile(r"^(?:<.*>|\.\.\.|…|tbd|n/?a|none|)$", re.IGNORECASE)
MD_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")

REQ_STATUS = {"draft", "accepted", "superseded", "rejected"}
VERIFICATION = {"unit", "integration", "hil", "bench", "fault", "analysis", "inspection"}
GATE_STATUS = {"not_started", "in_progress", "ready_for_review", "passed", "superseded"}
EXP_STATUS = {"draft", "ready", "running", "analysed", "accepted", "rejected", "abandoned"}
EVIDENCE_STATUS = {"recorded", "accepted", "rejected"}
EVIDENCE_KIND = {
    "CAP": "capture", "DATA": "dataset", "IMG": "image",
    "MEAS": "measurement", "LOG": "log",
}

REQUIRED_REQ_FIELDS = ("id", "title", "statement", "status", "rationale",
                       "verification", "gate", "evidence")
REQUIRED_STATUS_KEYS = ("schema_version", "harness_version", "updated", "product",
                        "phase", "gate", "objective", "experiment",
                        "active_requirements", "blockers", "decisions_required",
                        "human_actions_required", "latest_accepted_evidence",
                        "next_proposed_actions")
ADR_SECTIONS = ("context", "decision", "alternatives", "rationale", "consequences",
                "evidence", "revisit triggers")

SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", "node_modules"}


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.checks = 0

    def check(self, ok: bool, message: str, warn: bool = False) -> bool:
        self.checks += 1
        if not ok:
            (self.warnings if warn else self.errors).append(message)
        return ok

    def error(self, message: str) -> None:
        self.checks += 1
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.checks += 1
        self.warnings.append(message)


def load_yaml(path: Path, rep: Report, name: str | None = None):
    label = name or str(path)
    if not path.exists():
        rep.error(f"{label}: missing")
        return None
    try:
        return yaml.safe_load(path.read_text())
    except yaml.YAMLError as exc:
        rep.error(f"{label}: YAML parse error: {exc}")
        return None
    except ValueError as exc:
        # PyYAML resolves timestamp-shaped scalars itself and raises a bare
        # ValueError on an impossible one (2026-99-99T25:61:61Z). Without this the
        # validator would crash instead of reporting the defect.
        rep.error(f"{label}: invalid timestamp value: {exc}")
        return None


def check_status(repo: Path, rep: Report) -> dict:
    path = repo / "project/status.yaml"
    data = load_yaml(path, rep, "project/status.yaml")
    if not isinstance(data, dict):
        return {}
    for key in REQUIRED_STATUS_KEYS:
        rep.check(key in data, f"project/status.yaml: missing key '{key}'")

    gate = data.get("gate") or {}
    current = gate.get("current")
    rep.check(bool(current) and GATE_ID.match(str(current)),
              f"project/status.yaml: gate.current '{current}' is not a valid gate id")
    rep.check(gate.get("status") in GATE_STATUS,
              f"project/status.yaml: gate.status '{gate.get('status')}' not in {sorted(GATE_STATUS)}")
    gate_file = gate.get("file")
    if gate_file:
        rep.check((repo / gate_file).exists(),
                  f"project/status.yaml: gate.file '{gate_file}' does not exist")

    exp = (data.get("experiment") or {}).get("active")
    if exp is not None:
        rep.check(bool(EXP_ID.match(str(exp))),
                  f"project/status.yaml: experiment.active '{exp}' is not a valid experiment id")
    return data


def check_requirements(repo: Path, rep: Report) -> dict:
    path = repo / "requirements/product.yaml"
    data = load_yaml(path, rep, "requirements/product.yaml")
    reqs: dict[str, dict] = {}
    if not isinstance(data, dict):
        return reqs
    items = data.get("requirements") or []
    rep.check(bool(items), "requirements/product.yaml: no requirements defined")
    for item in items:
        rid = item.get("id", "<missing id>")
        if not REQ_ID.match(str(rid)):
            rep.error(f"requirements: '{rid}' does not match SV-<AREA>-nnn")
            continue
        if rid in reqs:
            rep.error(f"requirements: duplicate id {rid}")
            continue
        reqs[rid] = item
        for field in REQUIRED_REQ_FIELDS:
            rep.check(field in item, f"{rid}: missing field '{field}'")
        rep.check(item.get("status") in REQ_STATUS,
                  f"{rid}: status '{item.get('status')}' not in {sorted(REQ_STATUS)}")
        rep.check(bool(GATE_ID.match(str(item.get("gate")))),
                  f"{rid}: gate '{item.get('gate')}' is not a valid gate id")
        for method in item.get("verification") or []:
            rep.check(method in VERIFICATION,
                      f"{rid}: verification method '{method}' not in {sorted(VERIFICATION)}")
        for ev in item.get("evidence") or []:
            rep.check(bool(EVIDENCE_ID.match(str(ev))),
                      f"{rid}: evidence '{ev}' is not a valid evidence id")
    return reqs


def check_traceability(repo: Path, reqs: dict, rep: Report) -> None:
    path = repo / "requirements/traceability.md"
    if not rep.check(path.exists(), "requirements/traceability.md: missing"):
        return
    text = path.read_text()
    for rid in reqs:
        count = len(re.findall(rf"\|\s*{re.escape(rid)}\s*\|", text))
        if count == 0:
            rep.error(f"traceability: {rid} has no row in traceability.md")
        elif count > 1:
            rep.error(f"traceability: {rid} appears in {count} rows; expected exactly one")
    for rid in sorted(set(re.findall(r"SV-[A-Z]{2,3}-\d{3}", text))):
        rep.check(rid in reqs,
                  f"traceability: {rid} is referenced but not defined in product.yaml")


def check_gates(repo: Path, status: dict, rep: Report) -> None:
    gates_dir = repo / "project/gates"
    if not rep.check(gates_dir.is_dir(), "project/gates: missing"):
        return
    files = sorted(p.name for p in gates_dir.glob("G*.md"))
    rep.check(bool(files), "project/gates: no gate files found")
    current = (status.get("gate") or {}).get("current")
    if current:
        rep.check(any(f.startswith(f"{current}-") for f in files),
                  f"project/gates: no file for current gate {current}")
    for name in files:
        gid = name.split("-", 1)[0]
        rep.check(bool(GATE_ID.match(gid)),
                  f"project/gates/{name}: filename does not start with a valid gate id")


def check_adrs(repo: Path, rep: Report) -> None:
    adr_dir = repo / "docs/decisions"
    if not rep.check(adr_dir.is_dir(), "docs/decisions: missing"):
        return
    register = (adr_dir / "README.md").read_text() if (adr_dir / "README.md").exists() else ""
    seen: dict[str, str] = {}
    files = [p for p in sorted(adr_dir.glob("ADR-*.md"))]
    rep.check(bool(files), "docs/decisions: no ADRs found")
    for path in files:
        match = ADR_FILE.match(path.name)
        if not match:
            rep.error(f"docs/decisions/{path.name}: filename does not match ADR-nnnn-<slug>.md")
            continue
        num = match.group(1)
        if num in seen:
            rep.error(f"docs/decisions: duplicate ADR number {num} "
                      f"({seen[num]} and {path.name})")
            continue
        seen[num] = path.name
        text = path.read_text()
        lowered = text.lower()
        for section in ADR_SECTIONS:
            rep.check(f"\n## {section}" in lowered,
                      f"docs/decisions/{path.name}: missing required section '{section}'")
        rep.check(bool(re.search(r"\|\s*Status\s*\|\s*\S", text)),
                  f"docs/decisions/{path.name}: no Status row in the header table")
        rep.check(path.name in register,
                  f"docs/decisions/README.md: register does not list {path.name}")
    rep.check(bool((adr_dir / "adr-template.md").exists()),
              "docs/decisions/adr-template.md: missing")


def check_experiments(repo: Path, rep: Report) -> dict[str, str]:
    exp_root = repo / "experiments"
    evidence_status: dict[str, str] = {}
    if not rep.check(exp_root.is_dir(), "experiments: missing"):
        return {}
    for required in ("README.md", "evidence.md",
                     "templates/experiment-template.md",
                     "templates/evidence-manifest.yaml"):
        rep.check((exp_root / required).exists(), f"experiments/{required}: missing")

    seen_nums: dict[str, str] = {}
    for path in sorted(p for p in exp_root.iterdir() if p.is_dir()):
        if path.name == "templates":
            continue
        match = EXP_DIR.match(path.name)
        if not match:
            rep.error(f"experiments/{path.name}: directory does not match EXP-nnnn-<slug>")
            continue
        num = match.group(1)
        if num in seen_nums:
            rep.error(f"experiments: duplicate experiment number {num} "
                      f"({seen_nums[num]} and {path.name})")
            continue
        seen_nums[num] = path.name
        record = path / f"EXP-{num}.md"
        rep.check(record.exists(), f"experiments/{path.name}: missing record EXP-{num}.md")
        if record.exists():
            text = record.read_text()
            found = re.search(r"\|\s*Status\s*\|\s*([a-z_]+)", text)
            if found:
                rep.check(found.group(1) in EXP_STATUS,
                          f"{record.relative_to(repo)}: status '{found.group(1)}' "
                          f"not in {sorted(EXP_STATUS)}")
            else:
                rep.warn(f"{record.relative_to(repo)}: no Status row found")
        manifest = path / "evidence" / "manifest.yaml"
        if (path / "evidence").is_dir():
            if not rep.check(manifest.exists(),
                             f"experiments/{path.name}/evidence: missing manifest.yaml"):
                continue
            data = load_yaml(manifest, rep, str(manifest.relative_to(repo))) or {}
            listed = set()
            for item in data.get("items") or []:
                eid = str(item.get("id"))
                if not EVIDENCE_ID.match(eid):
                    rep.error(f"{manifest.relative_to(repo)}: '{eid}' is not a valid evidence id")
                    continue
                if eid in evidence_status:
                    rep.error(f"evidence: duplicate id {eid} "
                              f"(already declared in another experiment and {path.name})")
                    continue
                status = item.get("status")
                evidence_status[eid] = str(status)
                rep.check(item.get("status") in EVIDENCE_STATUS,
                          f"{manifest.relative_to(repo)}: {eid} status "
                          f"'{item.get('status')}' not in {sorted(EVIDENCE_STATUS)}")
                fname = item.get("file")
                if fname:
                    listed.add(fname)
                    rep.check((path / "evidence" / fname).exists(),
                              f"{manifest.relative_to(repo)}: {eid} references missing file '{fname}'")
                    rep.check(fname.startswith(f"{eid}_EXP-{num}_"),
                              f"{manifest.relative_to(repo)}: {eid} file '{fname}' "
                              "does not follow <EVIDENCE-ID>_<EXP-ID>_<description> naming")
                prefix = eid.split("-", 1)[0]
                problem = _recorded_at_problem(item.get("recorded_at"))
                rep.check(problem is None,
                          f"{manifest.relative_to(repo)}: {eid} recorded_at {problem}")
                rep.check(item.get("kind") == EVIDENCE_KIND.get(prefix),
                          f"{manifest.relative_to(repo)}: {eid} kind '{item.get('kind')}' "
                          f"does not match its {prefix} prefix")
            rep.check(data.get("experiment") == f"EXP-{num}",
                      f"{manifest.relative_to(repo)}: experiment must be EXP-{num}")
            for f in (path / "evidence").iterdir():
                if f.name != "manifest.yaml" and f.name not in listed:
                    rep.error(f"experiments/{path.name}/evidence/{f.name}: "
                              "file has no manifest entry (an unmanifested file is not evidence)")
    return evidence_status


def check_evidence_references(status: dict, reqs: dict,
                              evidence_status: dict[str, str], rep: Report) -> None:
    for rid, requirement in reqs.items():
        for eid in requirement.get("evidence") or []:
            rep.check(str(eid) in evidence_status,
                      f"{rid}: evidence '{eid}' has no manifest entry in any experiment")
            rep.check(evidence_status.get(str(eid)) == "accepted",
                      f"{rid}: evidence '{eid}' is not accepted")
    for eid in status.get("latest_accepted_evidence") or []:
        rep.check(str(eid) in evidence_status,
                  f"project/status.yaml: latest_accepted_evidence '{eid}' "
                  "has no manifest entry in any experiment")
        rep.check(evidence_status.get(str(eid)) == "accepted",
                  f"project/status.yaml: latest_accepted_evidence '{eid}' is not accepted")


def _sender_of(message_id: str) -> str:
    """Sender encoded in a message ID (MSG-<timestamp>-<sender>)."""
    return message_id.rsplit("-", 1)[-1]


def _recorded_at_problem(value: object) -> str | None:
    """Why an evidence `recorded_at` is unacceptable, or None if it is fine.

    Convention (ruled by Codex, MSG-20260905T015729Z-98ba-codex): either the literal
    `unknown`, or a calendar-valid ISO-8601/RFC-3339 timestamp carrying an explicit
    UTC offset. `Z` is accepted; a local offset is retained, never normalised.

    PyYAML resolves an unquoted timestamp to a datetime before this sees it, so both
    a datetime and a string have to be handled. datetime is checked before date
    because datetime is a subclass of date.
    """
    if value is None:
        return "is missing"
    if isinstance(value, str):
        text = value.strip()
        if text == "unknown":
            return None
        try:
            parsed = datetime.fromisoformat(text)
        except ValueError:
            return (f"'{value}' is neither the literal `unknown` nor a valid "
                    "ISO-8601/RFC-3339 timestamp")
    elif isinstance(value, datetime):
        parsed = value
    elif isinstance(value, date):
        return f"'{value}' is a date with no time of day or UTC offset"
    else:
        return f"has unexpected type {type(value).__name__}"
    if parsed.tzinfo is None:
        return (f"'{value}' has no explicit UTC offset "
                "(append Z for UTC, or a local offset such as +10:00)")
    return None


def _utc_or_none(value: str, fmt: str) -> datetime | None:
    r"""Parse a UTC timestamp, rejecting impossible calendar dates and times.

    A shape regex is not enough: `\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z` accepts
    2026-99-99T25:61:61Z. strptime rejects month/day overflow, hour 24, and seconds
    60-61 (it does not permit leap seconds), which is what makes this semantic.
    """
    try:
        return datetime.strptime(value, fmt)
    except ValueError:
        return None


def _section(text: str, heading: str) -> str | None:
    """Body of one '## <heading>' section, up to the next heading or end of file."""
    found = re.search(rf"^##\s+{re.escape(heading)}\s*$(.*?)(?=^##\s|\Z)",
                      text, re.MULTILINE | re.DOTALL)
    return found.group(1) if found else None


def _msg_field(text: str, field: str) -> str | None:
    found = re.search(rf"^\|\s*{re.escape(field)}\s*\|\s*(.+?)\s*\|\s*$",
                      text, re.MULTILINE)
    return found.group(1).strip() if found else None


def check_coordination(repo: Path, rep: Report) -> list[str]:
    """Validate the coordination ledger and report open threads.

    The ledger is append-only with no index, so the only thing that can rot is a
    header disagreeing with its filename -- which would make the ledger unsortable
    and its IDs unresolvable. That is what is checked here.
    """
    root = repo / "project/coordination"
    if not root.is_dir():
        return []
    rep.check((root / "README.md").exists(), "project/coordination/README.md: missing")

    seen: dict[str, str] = {}
    replies: list[tuple[str, str, str]] = []
    needs_response: dict[str, str] = {}
    reply_senders: list[tuple[str, str]] = []

    # rglob so archiving by year later does not hide messages
    for path in sorted(root.rglob("*.md")):
        if path.name == "README.md":
            continue
        rel = path.relative_to(repo)
        match = MSG_FILE.match(path.name)
        if not match:
            rep.error(f"{rel}: filename does not match "
                      "YYYYMMDDThhmmssZ-<nonce>-<sender>-to-<recipient>.md "
                      "(nonce is exactly 4 lowercase hex characters)")
            continue
        stamp, nonce, sender, recipient = match.groups()
        if _utc_or_none(stamp, "%Y%m%dT%H%M%SZ") is None:
            rep.error(f"{rel}: filename timestamp '{stamp}' is not a real UTC instant")
            continue
        rep.check(sender in SENDERS,
                  f"{rel}: '{sender}' is not a valid sender {sorted(SENDERS)} -- a party "
                  "with no direct writer must be relayed, not impersonated")
        rep.check(recipient in RECIPIENTS, f"{rel}: unknown recipient '{recipient}'")
        if stamp >= NONCE_REQUIRED_FROM:
            rep.check(bool(nonce),
                      f"{rel}: filename needs a 4-hex-character nonce "
                      "(<timestamp>-<nonce>-<sender>-to-<recipient>.md)")

        text = path.read_text()
        mid = _msg_field(text, "ID")
        expected_id = f"MSG-{stamp}-{nonce}-{sender}" if nonce else f"MSG-{stamp}-{sender}"
        if not mid or not MSG_ID.match(mid):
            rep.error(f"{rel}: missing or malformed ID field")
            continue
        rep.check(mid == expected_id,
                  f"{rel}: ID '{mid}' disagrees with filename (expected '{expected_id}')")
        if mid in seen:
            rep.error(f"coordination: duplicate message ID {mid} "
                      f"({seen[mid]} and {rel})")
            continue
        seen[mid] = str(rel)

        frm = (_msg_field(text, "From") or "").lower()
        to = (_msg_field(text, "To") or "").lower()
        rep.check(frm == sender, f"{rel}: From '{frm}' disagrees with filename '{sender}'")
        rep.check(to == recipient,
                  f"{rel}: To '{to}' disagrees with filename '{recipient}'")

        created = _msg_field(text, "Created") or ""
        expected_created = (f"{stamp[0:4]}-{stamp[4:6]}-{stamp[6:8]}T"
                            f"{stamp[9:11]}:{stamp[11:13]}:{stamp[13:15]}Z")
        rep.check(created == expected_created,
                  f"{rel}: Created '{created}' disagrees with filename "
                  f"(expected '{expected_created}')")

        gate = _msg_field(text, "Gate") or ""
        rep.check(gate == "none" or bool(GATE_ID.match(gate)),
                  f"{rel}: Gate '{gate}' is not a valid gate id or 'none'")

        requires = (_msg_field(text, "Requires response") or "").lower()
        rep.check(requires in {"yes", "no"},
                  f"{rel}: Requires response '{requires}' must be yes or no")
        # A broadcast asking several parties for input would be closed by whichever
        # replied first, so broadcasts are notification-only.
        if recipient == "all":
            rep.check(requires == "no",
                      f"{rel}: a 'To: All' broadcast must be notification-only "
                      "(Requires response: no); send separate messages when independent "
                      "replies are needed")

        relayed = (_msg_field(text, "Relayed from") or "none").lower()
        if relayed != "none":
            rep.check(relayed in PARTIES,
                      f"{rel}: Relayed from '{relayed}' is not a known party")
            rep.check(relayed != sender,
                      f"{rel}: Relayed from '{relayed}' cannot be the message's own author")
            body = _section(text, "Relay provenance")
            if body is None:
                rep.error(f"{rel}: a relayed message needs a 'Relay provenance' section")
            else:
                # The heading alone is not attribution -- check the fields it promises.
                for field in RELAY_FIELDS:
                    value = (_msg_field(body, field) or "").strip()
                    if PLACEHOLDER.match(value):
                        rep.error(f"{rel}: relay provenance '{field}' is missing, empty "
                                  "or an unfilled placeholder")
                        continue
                    if field == "Fidelity":
                        rep.check(value.lower() in FIDELITY,
                                  f"{rel}: relay provenance Fidelity '{value}' must be "
                                  f"one of {sorted(FIDELITY)}")
                    elif field == "Supplied at":
                        if not ISO_UTC.match(value):
                            rep.error(f"{rel}: relay provenance 'Supplied at' '{value}' "
                                      "must be ISO-8601 UTC (YYYY-MM-DDTHH:MM:SSZ)")
                        elif _utc_or_none(value, "%Y-%m-%dT%H:%M:%SZ") is None:
                            rep.error(f"{rel}: relay provenance 'Supplied at' '{value}' "
                                      "is correctly shaped but is not a real date and "
                                      "time")

        for section in ("## message", "## requested action",
                        "## canonical artifacts affected"):
            rep.check(section in text.lower(),
                      f"{rel}: missing section '{section[3:]}'")

        reply_to = _msg_field(text, "In reply to") or ""
        if requires == "yes":
            needs_response[mid] = str(rel)
        if reply_to and reply_to.lower() != "none":
            replies.append((mid, str(rel), reply_to))
            # A sender following up on their own message does not answer it -- the
            # request is still outstanding with the recipient. Only a different party
            # closes a thread.
            reply_senders.append((reply_to, sender))

    for _mid, rel, reply_to in replies:
        rep.check(reply_to in seen,
                  f"{rel}: 'In reply to' references unknown message {reply_to}")

    answered = {target for target, by in reply_senders
                if by != _sender_of(target)}
    still_open = {k: v for k, v in needs_response.items() if k not in answered}
    if still_open:
        print("Open coordination threads (awaiting a response):")
        for mid, rel in sorted(still_open.items()):
            print(f"  {mid}  {rel}")
        print()
    return list(seen)


def check_directory_purpose(repo: Path, rep: Report) -> None:
    """Every directory must be documented: its own README, or named in its parent's."""
    for path in sorted(repo.rglob("*")):
        if not path.is_dir():
            continue
        rel = path.relative_to(repo)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        # Experiment directories document themselves through their record and
        # manifest; they do not carry a README.
        if any(EXP_DIR.match(part) for part in rel.parts):
            continue
        if (path / "README.md").exists():
            continue
        parent_readme = path.parent / "README.md"
        if parent_readme.exists() and path.name in parent_readme.read_text():
            continue
        rep.error(f"{rel}/: no README.md and not described in {path.parent.name or '.'}/README.md")


def check_links(repo: Path, rep: Report) -> None:
    for path in sorted(repo.rglob("*.md")):
        rel = path.relative_to(repo)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        for target in MD_LINK.findall(path.read_text()):
            target = target.split()[0].strip()
            if target.startswith(("http://", "https://", "mailto:", "#")) or not target:
                continue
            resolved = (path.parent / target.split("#", 1)[0]).resolve()
            rep.check(resolved.exists(), f"{rel}: broken link -> {target}")


def check_no_placeholder_ids(repo: Path, rep: Report) -> None:
    """Templates use nnnn placeholders; real records must not."""
    records = list(repo.glob("experiments/EXP-*/EXP-*.md")) + \
        [p for p in repo.glob("docs/decisions/ADR-*.md")]
    for path in sorted(records):
        rel = path.relative_to(repo)
        if re.search(r"\b(EXP|ADR|CAP|DATA|IMG|MEAS|LOG)-nnnn\b", path.read_text()):
            rep.warn(f"{rel}: contains an unfilled 'nnnn' identifier placeholder")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=Path(__file__).resolve().parent.parent,
                        type=Path, help="repository root (default: parent of tools/)")
    args = parser.parse_args()
    repo = args.repo.resolve()

    rep = Report()
    for required in ("README.md", "AGENTS.md", "project/status.yaml",
                     "requirements/product.yaml", "requirements/traceability.md",
                     "tests/README.md"):
        rep.check((repo / required).exists(), f"{required}: missing")

    status = check_status(repo, rep)
    reqs = check_requirements(repo, rep)
    check_traceability(repo, reqs, rep)
    check_gates(repo, status, rep)
    check_adrs(repo, rep)
    evidence_status = check_experiments(repo, rep)
    check_evidence_references(status, reqs, evidence_status, rep)
    messages = check_coordination(repo, rep)
    check_directory_purpose(repo, rep)
    check_links(repo, rep)
    check_no_placeholder_ids(repo, rep)

    for message in rep.warnings:
        print(f"WARN  {message}")
    for message in rep.errors:
        print(f"ERROR {message}")

    print(f"\n{rep.checks} checks, {len(rep.errors)} errors, {len(rep.warnings)} warnings")
    print(f"requirements: {len(reqs)}  evidence items: {len(evidence_status)}  "
          f"coordination messages: {len(messages)}")
    if rep.errors:
        print("FAIL")
        return 1
    print("OK — structure is self-consistent. This says nothing about whether the "
          "content is correct (AGENTS.md §9).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
