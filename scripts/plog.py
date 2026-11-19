#!/usr/bin/env python3
"""Append one UTC-stamped line to a progress log or to the project state log.

Windows-friendly twin of scripts/plog.sh (which needs bash).
Usage: python scripts/plog.py <task-id|state> <ACTOR> <message...>
  task-id -> progress/<task-id>.log
  state   -> state/PROJECT_STATE.md (append-only event log)
Line format: - <UTC> <ACTOR>: <message>
The stamp is read from the system clock at the moment of writing, so nobody types a clock time by hand.
"""
import datetime
import pathlib
import re
import sys
import time

USAGE = "usage: python scripts/plog.py <task-id|state> <ACTOR> <message...>"
NAME = re.compile(r"^[A-Za-z0-9_.-]+$")


def main():
    if len(sys.argv) < 4:
        print(USAGE, file=sys.stderr)
        return 2
    task, actor = sys.argv[1], sys.argv[2]
    if not NAME.match(task):
        print("plog: bad task id", file=sys.stderr)
        return 2
    if not NAME.match(actor):
        print("plog: bad actor", file=sys.stderr)
        return 2
    message = re.sub(r"\s+", " ", " ".join(sys.argv[3:])).strip()
    if not message:
        print("plog: empty message", file=sys.stderr)
        return 2
    root = pathlib.Path(__file__).resolve().parent.parent
    target = root / "state" / "PROJECT_STATE.md" if task == "state" else root / "progress" / f"{task}.log"
    target.parent.mkdir(parents=True, exist_ok=True)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"- {stamp} {actor}: {message}\n"
    for attempt in range(8):
        try:
            with open(target, "a", encoding="utf-8", newline="\n") as handle:
                handle.write(line)
            break
        except OSError:
            time.sleep(0.25 * (attempt + 1))
    else:
        print("plog: could not append", file=sys.stderr)
        return 1
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(line.rstrip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
