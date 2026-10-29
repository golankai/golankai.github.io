"""
Merges assets/publications.pdf onto the end of assets/<CV file>.pdf as page 2+,
and records the resulting file's hash so check_cv_merge.py knows it's up to date.

Usage: python merge_cv_pubs.py [source_cv.pdf]

Pass the single-page CV exported from the source when it changed; without an argument the
CV already in assets/ is used (re-running then would append the publications a second time).
"""
import hashlib
import json
import os
import sys
from pypdf import PdfReader, PdfWriter

REPO = os.environ.get("CLAUDE_PROJECT_DIR") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CV_PATH = os.path.join(REPO, "assets", "Kai Golan Hashiloni - CV.pdf")
PUBS_PATH = os.path.join(REPO, "assets", "publications.pdf")
STATE_PATH = os.path.join(REPO, ".claude", "hooks", ".cv_merge_state.json")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def main():
    source = sys.argv[1] if len(sys.argv) > 1 else CV_PATH
    writer = PdfWriter()
    for page in PdfReader(source).pages:
        writer.add_page(page)
    for page in PdfReader(PUBS_PATH).pages:
        writer.add_page(page)
    writer.add_metadata({
        "/Title": "Kai Golan Hashiloni - CV",
        "/Author": "Kai Golan Hashiloni",
    })
    with open(CV_PATH, "wb") as f:
        writer.write(f)

    with open(STATE_PATH, "w") as f:
        json.dump({"merged_sha256": sha256(CV_PATH)}, f)

    print(f"Merged. {CV_PATH} now has {len(PdfReader(CV_PATH).pages)} pages.")


if __name__ == "__main__":
    main()
