#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


ORIGINAL = Path("/Users/yoda/.claude/plugins/cache/claude-plugins-official/skill-creator/unknown/skills/skill-creator/eval-viewer/generate_review.py")


def main() -> None:
    source = ORIGINAL.read_text(encoding="utf-8")
    if "from __future__ import annotations" not in source.splitlines()[:5]:
        lines = source.splitlines()
        if lines and lines[0].startswith("#!"):
            lines.insert(1, "from __future__ import annotations")
        else:
            lines.insert(0, "from __future__ import annotations")
        source = "\n".join(lines)

    globals_dict = {
        "__name__": "__main__",
        "__file__": str(ORIGINAL),
    }
    exec(compile(source, str(ORIGINAL), "exec"), globals_dict)


if __name__ == "__main__":
    main()
