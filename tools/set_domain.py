"""
Switch the site's placeholder domain to the production domain.

Replaces every absolute URL built on the placeholder in the HTML pages,
sitemap.xml, and robots.txt, and removes the "replace the domain" TODO notes.

Usage:
    python tools/set_domain.py https://www.patientaid.com
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLACEHOLDER = "https://patientaid.example.com"
TODO_COMMENT = re.compile(
    r"^\s*<!-- TODO: replace patientaid\.example\.com with the production domain before launch\. -->\n",
    re.M,
)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python tools/set_domain.py https://www.example.com")
        return 2

    domain = sys.argv[1].strip().rstrip("/")
    if not re.fullmatch(r"https?://[A-Za-z0-9.-]+(:\d+)?", domain):
        print(f"Not a valid origin: {domain!r}")
        return 2

    targets = sorted(ROOT.glob("*.html")) + [ROOT / "sitemap.xml", ROOT / "robots.txt"]
    total = 0

    for path in targets:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if PLACEHOLDER not in text:
            continue
        count = text.count(PLACEHOLDER)
        text = text.replace(PLACEHOLDER, domain)
        text = TODO_COMMENT.sub("", text)
        path.write_text(text, encoding="utf-8")
        total += count
        print(f"{path.name}: {count} URL(s) updated")

    print(f"\nDone. {total} URL(s) now use {domain}.")
    print("Next: upload the folder, then submit sitemap.xml in Google Search Console.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
