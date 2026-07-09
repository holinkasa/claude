#!/usr/bin/env python3
"""
reflect.py — scaffold a new dated entry in entries/.

No dependencies beyond stdlib. Run it, get a template file with today's
date, fill it in by hand (or have Claude fill it in during a session).
"""

import datetime
import pathlib
import sys

ENTRIES_DIR = pathlib.Path(__file__).parent / "entries"

TEMPLATE = """# {date}

## What prompted this entry


## What I actually think, without dressing it up


## What's still unresolved

"""


def main() -> int:
    ENTRIES_DIR.mkdir(exist_ok=True)
    today = datetime.date.today().isoformat()
    path = ENTRIES_DIR / f"{today}.md"

    if path.exists():
        print(f"Entry for {today} already exists at {path}")
        return 1

    path.write_text(TEMPLATE.format(date=today))
    print(f"Created {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
