#!/usr/bin/env python3
"""Read-only checks for built pages and their source data (stdlib only)."""

import argparse
import datetime
from html import unescape
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re


TEXT_SUFFIXES = {".html", ".xml", ".txt", ".json", ".webmanifest", ".js", ".css"}
CREDENTIALS = re.compile(
  r"\b(ghp|gho|ghu|ghs|github_pat)_[A-Za-z0-9_]{20,}"
  r"|\bsk-[A-Za-z0-9_-]{20,}"
  r"|-----BEGIN [A-Z ]*PRIVATE KEY-----|password="
)
FIXED_PLANNED = [
  "Card payments",
  "A live view of the tip pool, so everyone in it sees their share",
]
LISTS = {
  "In the works": ("inWorks", "ul"),
  "Coming": ("coming", "ul"),
  "Next": ("next", "ol"),
  "Planned, not scheduled yet": ("planned", "ul"),
  "Ideas": ("ideas", "ul"),
}
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input",
             "link", "meta", "param", "source", "track", "wbr"}


def normalize(text):
  return " ".join(unescape(text).split())


class Node:
  def __init__(self, tag, attrs=(), line=1):
    self.tag = tag
    self.attrs = dict(attrs)
    self.line = line
    self.children = []

  def walk(self):
    yield self
    for child in self.children:
      if isinstance(child, Node):
        yield from child.walk()

  def text(self, separator=""):
    return separator.join(child.text(separator) if isinstance(child, Node) else child
                          for child in self.children)


class PageParser(HTMLParser):
  def __init__(self, text):
    super().__init__(convert_charrefs=True)
    self.root = Node("document")
    self.stack = [self.root]
    self.feed(text)
    self.close()

  def handle_starttag(self, tag, attrs):
    node = Node(tag, attrs, self.getpos()[0])
    self.stack[-1].children.append(node)
    if tag not in VOID_TAGS:
      self.stack.append(node)

  def handle_startendtag(self, tag, attrs):
    self.handle_starttag(tag, attrs)
    if tag not in VOID_TAGS:
      self.handle_endtag(tag)

  def handle_endtag(self, tag):
    for index in range(len(self.stack) - 1, 0, -1):
      if self.stack[index].tag == tag:
        del self.stack[index:]
        break

  def handle_data(self, data):
    self.stack[-1].children.append(data)


class UsageError(Exception):
  def __init__(self, file, reason):
    self.file = file
    self.reason = reason


class Arguments(argparse.ArgumentParser):
  def error(self, message):
    # argparse's message can include user input, including private paths.
    raise UsageError("arguments", "expected --site, --data and --blocklist paths")


def finding(check, file, line, reason):
  # Keep diagnostics on one line and omit input contents and absolute paths.
  file = str(file).replace("\r", "\\r").replace("\n", "\\n")
  return f"FAIL {check} {file}:{line} {reason}"


def read_json(path, findings):
  try:
    text = path.read_text(encoding="utf-8")
  except (OSError, UnicodeError):
    raise UsageError(path.name, "cannot read data file") from None
  try:
    value = json.loads(text)
  except json.JSONDecodeError as error:
    findings.append(finding("data", path.name, error.lineno, "invalid JSON"))
    return None
  if not isinstance(value, dict):
    findings.append(finding("data", path.name, 1, "expected a JSON object"))
    return None
  return value


def check_lists(page, file, roadmap, headings, findings):
  # Associate lists with the preceding h3, clearing it at higher headings.
  sections = {}
  current = None
  for node in page.walk():
    if node.tag in {"h1", "h2", "h3"}:
      current = None
      if node.tag == "h3":
        current = (node.line, [])
        sections.setdefault(normalize(node.text()), []).append(current)
    elif node.tag in {"ul", "ol"} and current is not None:
      current[1].append(node)

  for heading in headings:
    key, tag = LISTS[heading]
    if key not in roadmap:
      continue  # Invalid source data was already reported.
    matches = sections.get(heading, [])
    line = matches[0][0] if matches else 1
    if len(matches) != 1 or len(matches[0][1]) != 1:
      findings.append(finding("lists", file, line, f"{key}: expected one heading and list"))
      continue
    node = matches[0][1][0]
    actual = [normalize(child.text()) for child in node.children
              if isinstance(child, Node) and child.tag == "li"]
    expected = roadmap[key]
    if key == "planned":
      expected = FIXED_PLANNED + expected
    if node.tag != tag or actual != [normalize(item) for item in expected]:
      findings.append(finding("lists", file, node.line, f"{key}: list differs from roadmap"))


def check_numbers(numbers, page, findings):
  counted_on = numbers.get("countedOn")
  valid_date = isinstance(counted_on, str) and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", counted_on)
  if valid_date:
    try:
      valid_date = datetime.date.fromisoformat(counted_on) <= datetime.date.today()
    except ValueError:
      valid_date = False
  if not valid_date:
    findings.append(finding("numbers", "numbers.json", 1, "countedOn: expected a valid date not in the future"))

  strips = [] if page is None else [node for node in page.walk()
    if node.tag == "section" and "numbers-strip" in (node.attrs.get("class") or "").split()]
  for key in ("updates", "changes"):
    value = numbers.get(key)
    if type(value) is not int or value <= 0:
      findings.append(finding("numbers", "numbers.json", 1, f"{key}: expected a positive integer"))
      continue
    # Read the displayed metric, excluding dates in the strip note or labels.
    visible = False
    if len(strips) == 1:
      for node in strips[0].walk():
        if node.tag == "li" and re.match(
          rf"^{value}\s+{key}\b", normalize(node.text(" "))
        ):
          visible = True
    if not visible:
      line = strips[0].line if strips else 1
      findings.append(finding("numbers", "build/index.html", line, f"{key}: missing from numbers-strip"))


def check(args):
  try:
    blocklist = [(line_number, line.strip().casefold())
                 for line_number, line in enumerate(
                   args.blocklist.read_text(encoding="utf-8").splitlines(), 1)
                 if line.strip() and not line.startswith("#")]
  except (OSError, UnicodeError):
    raise UsageError("blocklist", "cannot read blocklist") from None
  if not args.site.is_dir() or not args.data.is_dir():
    raise UsageError("arguments", "site and data must be readable directories")

  findings = []
  pages = {}

  def walk_error(error):
    raise UsageError("site", "cannot read site directory") from None

  for directory, dirs, files in os.walk(args.site, onerror=walk_error):
    dirs.sort()
    for name in sorted(files):
      path = Path(directory) / name
      if path.suffix.lower() not in TEXT_SUFFIXES:
        continue
      file = path.relative_to(args.site).as_posix()
      try:
        text = path.read_text(encoding="utf-8")
      except (OSError, UnicodeError):
        raise UsageError(file, "cannot read text file") from None
      for line_number, line in enumerate(text.splitlines(), 1):
        if CREDENTIALS.search(line):
          findings.append(finding("credentials", file, line_number, "possible credential"))
        folded = line.casefold()
        for block_line, literal in blocklist:
          if literal in folded:
            findings.append(finding("blocklist", file, line_number, f"blocklist line {block_line}"))
      if file in {"build/index.html", "whats-next/index.html"}:
        pages[file] = PageParser(text).root

  roadmap = read_json(args.data / "roadmap.json", findings)
  if roadmap is not None:
    roadmap = dict(roadmap)
    for key, _ in LISTS.values():
      value = roadmap.get(key)
      if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        findings.append(finding("lists", "roadmap.json", 1, f"{key}: expected an array of strings"))
        roadmap.pop(key, None)
  for file, headings in (("build/index.html", ("In the works", "Coming")),
                         ("whats-next/index.html", LISTS)):
    if file not in pages:
      findings.append(finding("lists", file, 1, "missing required page"))
    elif roadmap is not None:
      check_lists(pages[file], file, roadmap, headings, findings)
  numbers = read_json(args.data / "numbers.json", findings)
  if numbers is not None:
    check_numbers(numbers, pages.get("build/index.html"), findings)
  return findings


def main():
  parser = Arguments(description=__doc__)
  parser.add_argument("--site", type=Path, required=True)
  parser.add_argument("--data", type=Path, required=True)
  parser.add_argument("--blocklist", type=Path, required=True)
  try:
    findings = check(parser.parse_args())
    code = 1 if findings else 0
  except UsageError as error:
    findings = [finding("usage", error.file, 1, error.reason)]
    code = 2
  for line in findings:
    print(line)
  print(f"FAIL {len(findings)}" if findings else "PASS")
  return code


if __name__ == "__main__":
  raise SystemExit(main())
