"""
PostToolUse hook (matches Write|Edit|Bash). After any tool call, checks whether
assets/<CV file>.pdf currently matches the hash recorded the last time it was
merged with publications.pdf. If it doesn't match (e.g. someone just dropped in
a fresh CV export, or edited/replaced the file), exits 2 so Claude sees the
reminder and can prompt the user to re-run the merge.
"""
import hashlib
import json
import os
import sys

REPO = os.environ.get("CLAUDE_PROJECT_DIR") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CV_PATH = os.path.join(REPO, "assets", "Kai Golan Hashiloni - CV.pdf")
STATE_PATH = os.path.join(REPO, ".claude", "hooks", ".cv_merge_state.json")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def main():
    if not os.path.exists(CV_PATH):
        return

    current_hash = sha256(CV_PATH)

    stored_hash = None
    if os.path.exists(STATE_PATH):
        try:
            with open(STATE_PATH) as f:
                stored_hash = json.load(f).get("merged_sha256")
        except (json.JSONDecodeError, OSError):
            stored_hash = None

    if current_hash != stored_hash:
        print(
            "The CV PDF (assets/Kai Golan Hashiloni - CV.pdf) does not match the last "
            "merged version — it looks like it was just replaced or edited outside the "
            "merge script, so it may no longer include the publications list as page 2. "
            "Ask the user whether to re-run `.claude/hooks/merge_cv_pubs.py` to fold "
            "assets/publications.pdf back in as page 2.",
            file=sys.stderr,
        )
        sys.exit(2)


if __name__ == "__main__":
    main()
