#!/usr/bin/env python3
"""Render a WeChat-ready article HTML from structured input."""

import argparse
import sys
from pathlib import Path


TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
</head>
<body>

<h1>{title}</h1>

<section>
  <p>{digest}</p>
</section>

{body}

</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(
        description="Render a WeChat-editor-ready article HTML"
    )
    parser.add_argument("--title", required=True, help="Article title")
    parser.add_argument("--digest", default="", help="Article digest/summary (80-120 chars)")
    parser.add_argument("--body", type=Path, help="Article body HTML file (containing p/h2/blockquote/strong tags only)")
    parser.add_argument("--out", type=Path, required=True, help="Output HTML file path")
    args = parser.parse_args()

    body_html = ""
    if args.body:
        if not args.body.exists():
            print(f"Error: body file not found: {args.body}", file=sys.stderr)
            sys.exit(1)
        body_html = args.body.read_text().strip()

    html = TEMPLATE.format(
        title=args.title,
        digest=args.digest,
        body=body_html,
    )

    args.out.write_text(html)
    print(f"Article written: {args.out}")
    print("Open in browser, select all, copy, paste into WeChat editor.")


if __name__ == "__main__":
    main()
