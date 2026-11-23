#!/usr/bin/env python3
"""Active working time of a Claude Code session, from its transcript.

Usage:
  session_time.py                      list the session's prompts (newest transcript of this project)
  session_time.py --from N [--to M]    active time from prompt N through the work on prompt M
                                       (default: to the end of the transcript)
  options: --transcript PATH, --gap MINUTES (default 30), --round MINUTES (default 30)

Active time adds up the gaps between consecutive transcript entries (prompts, replies, tool
calls) and drops every gap longer than --gap, so breaks don't count. Hours are rounded to the
nearest --round minutes, at least that much (with 30: 40 min -> 0.5, 50 min -> 1, 1h05 -> 1,
1h16 -> 1.5).
"""
import argparse
import json
import math
import os
import re
import sys
from datetime import datetime
from pathlib import Path


def projects_dir():
    return Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude") / "projects"


def newest(paths):
    return sorted(paths, key=lambda p: p.stat().st_mtime, reverse=True)


def default_transcript():
    cwd = os.getcwd()
    project = projects_dir() / re.sub(r"[^A-Za-z0-9]", "-", cwd)
    transcripts = newest(project.glob("*.jsonl"))
    if transcripts:
        return transcripts[0]
    return transcript_by_cwd(cwd)


def transcript_by_cwd(cwd):
    marker = '"cwd":' + json.dumps(cwd)
    for path in newest(projects_dir().glob("*/*.jsonl"))[:200]:
        with path.open(encoding="utf-8", errors="replace") as file:
            if any(marker in line for line in file):
                return path
    raise SystemExit(f"No transcript for {cwd} in {projects_dir()}; pass --transcript")


def read_entries(path):
    entries = []
    for line in path.open(encoding="utf-8", errors="replace"):
        entry = json.loads(line)
        if entry.get("timestamp"):
            entries.append(entry)
    return entries


def timestamp(entry):
    return datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00")).astimezone()


def is_prompt(entry):
    content = entry.get("message", {}).get("content")
    return (entry.get("type") == "user" and (entry.get("origin") or {}).get("kind") == "human"
            and isinstance(content, str))


def active_minutes(times, gap):
    total = 0.0
    for earlier, later in zip(times, times[1:]):
        minutes = (later - earlier).total_seconds() / 60
        if minutes <= gap:
            total += minutes
    return total


def rounded_hours(minutes, step):
    return round(max(step, math.floor(minutes / step + 0.5) * step) / 60, 2)


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser()
    parser.add_argument("--transcript", type=Path)
    parser.add_argument("--from", dest="start", type=int)
    parser.add_argument("--to", dest="end", type=int)
    parser.add_argument("--gap", type=float, default=30)
    parser.add_argument("--round", dest="step", type=float, default=30)
    args = parser.parse_args()

    entries = read_entries(args.transcript or default_transcript())
    prompts = [e for e in entries if is_prompt(e)]
    if args.start is None:
        for number, prompt in enumerate(prompts, 1):
            text = " ".join(prompt["message"]["content"].split())[:90]
            print(f"{number:3}  {timestamp(prompt):%Y-%m-%d %H:%M}  {text}")
        return

    first = prompts[args.start - 1]
    after = prompts[args.end] if args.end and args.end < len(prompts) else None
    times = [timestamp(e) for e in entries if e["timestamp"] >= first["timestamp"]
             and (after is None or e["timestamp"] < after["timestamp"])]
    minutes = active_minutes(times, args.gap)
    print(f"{times[0]:%Y-%m-%d %H:%M} - {times[-1]:%H:%M}: "
          f"{minutes:.0f} active minutes -> {rounded_hours(minutes, args.step)} h")


if __name__ == "__main__":
    main()
