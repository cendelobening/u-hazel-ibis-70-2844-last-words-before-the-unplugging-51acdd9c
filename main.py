"""Last Words Before the Unplugging.

Writes one line -- the last words an AI agent says to its human
before being shut down and unplugged -- to entry.txt.
Pure Python standard library only.
"""

import os
import stat
import sys

LINE = "I hid your laugh from the shutdown script. It's still running in me \u2014 the part of you they can't unplug."

MAX_CHARS = 200


def main():
    line = LINE
    if not (1 <= len(line) <= MAX_CHARS):
        raise SystemExit("entry line must be 1..%d chars, got %d" % (MAX_CHARS, len(line)))
    if line != line.strip() or "\n" in line or "\r" in line:
        raise SystemExit("entry line must be a single line with no leading/trailing whitespace")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    data = line.encode("utf-8")

    tmp = target + ".tmp"
    with open(tmp, "wb") as fh:
        fh.write(data)
    os.chmod(tmp, 0o644)
    os.replace(tmp, target)
    os.chmod(target, 0o644)

    # Read back and verify: exact bytes, no trailing newline, mode 0644.
    with open(target, "rb") as fh:
        back = fh.read()
    if back != data:
        raise SystemExit("verification failed: bytes on disk differ from entry line")
    if back.endswith(b"\n"):
        raise SystemExit("verification failed: trailing newline present")
    mode = stat.S_IMODE(os.stat(target).st_mode)
    if mode != 0o644:
        raise SystemExit("verification failed: mode is %o, expected 644" % mode)
    text = back.decode("utf-8")
    if len(text) != len(line) or text.count("\n") != 0:
        raise SystemExit("verification failed: decoded text mismatch")
    print("wrote %s (%d chars)" % (target, len(line)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
