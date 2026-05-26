#!/usr/bin/env python3
"""Create a journal summary from local agent JSONL transcripts."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass, field
from datetime import date, datetime
import json
import os
from pathlib import Path
import re
import shlex
import sys
from typing import Any


@dataclass
class Item:
    source: str
    timestamp: str
    role: str
    excerpt: str = ""


@dataclass
class Digest:
    source_counts: Counter[str] = field(default_factory=Counter)
    role_counts: Counter[str] = field(default_factory=Counter)
    tools: Counter[str] = field(default_factory=Counter)
    paths: Counter[str] = field(default_factory=Counter)
    items: list[Item] = field(default_factory=list)
    include_excerpts: bool = False


def parse_date(value: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        raise SystemExit(f"Invalid date {value!r}; expected YYYY-MM-DD")


def date_from_timestamp(value: str) -> date | None:
    if not value:
        return None
    text = value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(text).date()
    except ValueError:
        match = re.match(r"(\d{4}-\d{2}-\d{2})", value)
        return parse_date(match.group(1)) if match else None


def date_range(start: date, end: date) -> list[date]:
    if start > end:
        raise SystemExit("--date-from must be before or equal to --date-to")
    days: list[date] = []
    current = start.toordinal()
    while current <= end.toordinal():
        days.append(date.fromordinal(current))
        current += 1
    return days


def compact_text(text: str, max_chars: int = 800) -> str:
    value = text
    value = re.sub(r"\s+", " ", value).strip()
    if len(value) > max_chars:
        value = value[: max_chars - 1].rstrip() + "..."
    return value


def text_from_value(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        parts: list[str] = []
        for item in value:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                text = item.get("text") or item.get("content") or item.get("input")
                if isinstance(text, str):
                    parts.append(text)
        return "\n".join(parts)
    if isinstance(value, dict):
        for key in ("text", "content", "message", "input"):
            if isinstance(value.get(key), str):
                return value[key]
        if isinstance(value.get("parts"), list):
            return text_from_value(value["parts"])
    return ""


def command_family(command: str) -> str:
    try:
        parts = shlex.split(command)
    except ValueError:
        parts = command.split()
    if not parts:
        return ""
    executable = parts[0]
    if "=" in executable and "/" not in executable:
        return "env"
    return Path(executable).name or "command"


def note_command(command: str, digest: Digest) -> None:
    family = command_family(command)
    if family:
        digest.tools[f"cmd:{family}"] += 1


def extract_paths(text: str, digest: Digest) -> None:
    for match in re.finditer(r"(?m)^\*\*\* (?:Add|Update|Delete) File: (.+)$", text):
        digest.paths[Path(match.group(1)).name or "[unnamed]"] += 1
    for match in re.finditer(r"(?m)^[MADRCU?]{1,2}\s+(.+)$", text):
        digest.paths[Path(match.group(1)).name or "[unnamed]"] += 1


def add_item(digest: Digest, source: str, timestamp: str, role: str, text: str) -> None:
    if not compact_text(text, max_chars=80):
        return
    digest.source_counts[source] += 1
    digest.role_counts[role] += 1
    extract_paths(text, digest)
    excerpt = compact_text(text) if digest.include_excerpts else ""
    digest.items.append(Item(source, timestamp, role, excerpt))


def discover_codex(root: Path, days: list[date]) -> list[Path]:
    files: list[Path] = []
    for day in days:
        folder = root / f"{day:%Y}" / f"{day:%m}" / f"{day:%d}"
        if folder.exists():
            files.extend(sorted(folder.glob("*.jsonl")))
    return files


def discover_claude(root: Path) -> list[Path]:
    return sorted(root.glob("*/*.jsonl")) if root.exists() else []


def discover_hermes(root: Path) -> list[tuple[Path, str]]:
    """Return (path, kind) pairs for Hermes sessions, deduped by session id.

    Full ``session_*.json`` records are preferred because they hold the
    complete message list. Standalone ``*.jsonl`` logs are included only when no
    full record exists for the same session id.
    """
    if not root.exists():
        return []
    found: dict[str, tuple[Path, str]] = {}
    for path in sorted(root.glob("session_*.json")):
        found[path.stem[len("session_") :]] = (path, "json")
    for path in sorted(root.glob("*.jsonl")):
        found.setdefault(path.stem, (path, "jsonl"))
    return [found[key] for key in sorted(found)]


def parse_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        for line in path.read_text(errors="replace").splitlines():
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    except OSError as exc:
        print(f"Warning: could not read {path}: {exc}", file=sys.stderr)
    return rows


def timestamp_for(row: dict[str, Any]) -> str:
    for key in ("timestamp", "created_at", "time"):
        if isinstance(row.get(key), str):
            return row[key]
    return ""


def in_range(row: dict[str, Any], start: date, end: date) -> bool:
    row_date = date_from_timestamp(timestamp_for(row))
    return bool(row_date and start <= row_date <= end)


def parse_codex_file(path: Path, start: date, end: date, digest: Digest) -> None:
    for row in parse_jsonl(path):
        if not in_range(row, start, end):
            continue
        timestamp = timestamp_for(row)
        row_type = str(row.get("type") or row.get("item_type") or "")
        role = str(row.get("role") or row.get("author") or "")

        payload = row.get("payload") if isinstance(row.get("payload"), dict) else row
        text = text_from_value(payload.get("text") or payload.get("content") or payload.get("message"))
        if text and role in {"user", "assistant"}:
            add_item(digest, "codex", timestamp, role, text)

        name = str(payload.get("name") or payload.get("tool_name") or payload.get("recipient") or "")
        args = payload.get("arguments") or payload.get("input") or {}
        if name:
            digest.tools[name] += 1
        if isinstance(args, dict):
            command = args.get("cmd") or args.get("command")
            if isinstance(command, str):
                note_command(command, digest)
            patch = args.get("patch") or args.get("input")
            if isinstance(patch, str):
                extract_paths(patch, digest)
        elif isinstance(args, str) and ("*** Begin Patch" in args or row_type == "tool_call"):
            extract_paths(args, digest)


def parse_claude_file(path: Path, start: date, end: date, digest: Digest, project_filter: str | None) -> None:
    if project_filter and project_filter.lower() not in str(path).lower():
        return
    for row in parse_jsonl(path):
        if not in_range(row, start, end):
            continue
        timestamp = timestamp_for(row)
        role = str(row.get("type") or row.get("role") or "")
        message = row.get("message") if isinstance(row.get("message"), dict) else row
        content = message.get("content") if isinstance(message, dict) else row.get("content")
        text = text_from_value(content)
        if text and role in {"user", "assistant"}:
            add_item(digest, "claude", timestamp, role, text)

        if isinstance(content, list):
            for block in content:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "tool_use":
                    name = str(block.get("name") or "tool")
                    digest.tools[name] += 1
                    tool_input = block.get("input")
                    if isinstance(tool_input, dict):
                        command = tool_input.get("command") or tool_input.get("cmd")
                        if isinstance(command, str):
                            note_command(command, digest)


def hermes_session_dates(obj: dict[str, Any] | None, path: Path) -> tuple[date | None, date | None]:
    if isinstance(obj, dict):
        start = date_from_timestamp(str(obj.get("session_start") or ""))
        end = date_from_timestamp(str(obj.get("last_updated") or "")) or start
        return start or end, end or start
    match = re.match(r"(\d{4})(\d{2})(\d{2})_", path.stem)
    if match:
        day = parse_date(f"{match.group(1)}-{match.group(2)}-{match.group(3)}")
        return day, day
    return None, None


def add_hermes_row(digest: Digest, row: dict[str, Any], timestamp: str) -> None:
    role = str(row.get("role") or "")
    text = text_from_value(row.get("content"))
    if text and role in {"user", "assistant"}:
        add_item(digest, "hermes", timestamp, role, text)

    for call in row.get("tool_calls") or []:
        if not isinstance(call, dict):
            continue
        function = call.get("function") if isinstance(call.get("function"), dict) else {}
        name = str(function.get("name") or call.get("name") or "tool")
        digest.tools[name] += 1
        raw_args = function.get("arguments")
        args: Any = {}
        if isinstance(raw_args, str):
            try:
                args = json.loads(raw_args)
            except json.JSONDecodeError:
                args = {}
        elif isinstance(raw_args, dict):
            args = raw_args
        if isinstance(args, dict):
            command = args.get("command") or args.get("cmd")
            if isinstance(command, str):
                note_command(command, digest)
            for key in ("path", "file_path"):
                value = args.get(key)
                if isinstance(value, str) and value:
                    digest.paths[Path(value).name or "[unnamed]"] += 1


def parse_hermes_file(path: Path, kind: str, start: date, end: date, digest: Digest) -> None:
    if kind == "json":
        try:
            obj = json.loads(path.read_text(errors="replace"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"Warning: could not read {path}: {exc}", file=sys.stderr)
            return
        if not isinstance(obj, dict):
            return
        messages = obj.get("messages")
        if not isinstance(messages, list):
            return
        # Full records carry no per-message timestamps, so include the whole
        # session when its [start, last_updated] window overlaps the range.
        s_start, s_end = hermes_session_dates(obj, path)
        if not (s_start and s_end and s_start <= end and s_end >= start):
            return
        default_ts = str(obj.get("last_updated") or obj.get("session_start") or "")
        for row in messages:
            if isinstance(row, dict):
                add_hermes_row(digest, row, timestamp_for(row) or default_ts)
        return

    session_date, _ = hermes_session_dates(None, path)
    for row in parse_jsonl(path):
        row_date = date_from_timestamp(timestamp_for(row)) or session_date
        if not (row_date and start <= row_date <= end):
            continue
        add_hermes_row(digest, row, timestamp_for(row) or (str(session_date) if session_date else ""))


def build_digest(args: argparse.Namespace) -> Digest:
    today = date.today()
    if args.date:
        start = end = parse_date(args.date)
    else:
        start = parse_date(args.date_from) if args.date_from else today
        end = parse_date(args.date_to) if args.date_to else today

    days = date_range(start, end)
    digest = Digest()
    digest.include_excerpts = args.include_excerpts

    if args.source in {"all", "codex"}:
        codex_root = Path(args.codex_root).expanduser()
        for path in discover_codex(codex_root, days):
            parse_codex_file(path, start, end, digest)

    if args.source in {"all", "claude"}:
        claude_root = Path(args.claude_root).expanduser()
        for path in discover_claude(claude_root):
            parse_claude_file(path, start, end, digest, args.project_filter)

    if args.source in {"all", "hermes"}:
        hermes_root = Path(args.hermes_root).expanduser()
        for path, kind in discover_hermes(hermes_root):
            parse_hermes_file(path, kind, start, end, digest)

    digest.items.sort(key=lambda item: item.timestamp)
    if args.max_items and len(digest.items) > args.max_items:
        digest.items = digest.items[-args.max_items :]
    digest.range = (start, end)  # type: ignore[attr-defined]
    return digest


def render_markdown(digest: Digest) -> str:
    start, end = digest.range  # type: ignore[attr-defined]
    label = f"{start:%Y-%m-%d}" if start == end else f"{start:%Y-%m-%d} to {end:%Y-%m-%d}"
    lines = [
        "# Journal Session History",
        "",
        f"Date: {label}",
        f"Items: {len(digest.items)}",
        "",
        "## Snapshot",
        "",
        f"- Sources: {dict((k, v) for k, v in digest.source_counts.items() if not k.startswith('date_'))}",
        f"- Roles: {dict(digest.role_counts)}",
        f"- Top tools: {dict(digest.tools.most_common(10))}",
        "",
    ]

    if digest.paths:
        lines.extend(["## Changed Or Referenced File Names", ""])
        for path, count in digest.paths.most_common(20):
            lines.append(f"- `{path}` ({count})")
        lines.append("")

    lines.extend(["## Timeline", ""])
    for item in digest.items:
        timestamp = item.timestamp or "unknown time"
        lines.append(f"### {timestamp} - {item.source} - {item.role}")
        if item.excerpt:
            lines.append("")
            lines.append(item.excerpt)
        lines.append("")

    if not digest.include_excerpts:
        lines.extend(
            [
                "> Raw transcript excerpts are omitted by default. Rerun with `--include-excerpts` for local-only review.",
                "",
            ]
        )

    lines.extend(
        [
            "## Journal Starters",
            "",
            "- Pull out concrete tasks, decisions, blockers, and verification steps.",
            "- Turn repeated work patterns into lessons or follow-up topics.",
        ]
    )
    return "\n".join(lines)


def render_json(digest: Digest) -> str:
    start, end = digest.range  # type: ignore[attr-defined]
    payload = {
        "date_from": f"{start:%Y-%m-%d}",
        "date_to": f"{end:%Y-%m-%d}",
        "source_counts": dict(digest.source_counts),
        "role_counts": dict(digest.role_counts),
        "tools": dict(digest.tools.most_common()),
        "paths": dict(digest.paths.most_common()),
        "items": [item.__dict__ for item in digest.items],
    }
    return json.dumps(payload, indent=2)


def build_parser() -> argparse.ArgumentParser:
    default_codex = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "sessions"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", help="Single date as YYYY-MM-DD.")
    parser.add_argument("--date-from", help="Inclusive start date as YYYY-MM-DD.")
    parser.add_argument("--date-to", help="Inclusive end date as YYYY-MM-DD.")
    parser.add_argument("--source", choices=["all", "codex", "claude", "hermes"], default="all")
    parser.add_argument("--codex-root", default=str(default_codex))
    parser.add_argument("--claude-root", default=str(Path.home() / ".claude" / "projects"))
    parser.add_argument("--hermes-root", default=str(Path.home() / ".hermes" / "sessions"))
    parser.add_argument("--project-filter", help="Substring filter for Claude project paths.")
    parser.add_argument("--max-items", type=int, default=80)
    parser.add_argument(
        "--include-excerpts",
        action="store_true",
        help="Include compact transcript excerpts in output. Default omits raw transcript text.",
    )
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.date and (args.date_from or args.date_to):
        raise SystemExit("--date cannot be combined with --date-from or --date-to")
    digest = build_digest(args)
    print(render_json(digest) if args.format == "json" else render_markdown(digest))


if __name__ == "__main__":
    main()
