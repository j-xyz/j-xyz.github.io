"""Exercise the public-site checker using isolated copies of real built pages."""

import datetime
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SCRIPTS = Path(__file__).resolve().parent
FIXTURES = SCRIPTS / "fixtures"


class CheckSiteTests(unittest.TestCase):
  def setUp(self):
    self.temp = tempfile.TemporaryDirectory()
    self.addCleanup(self.temp.cleanup)
    self.root = Path(self.temp.name)
    self.site = self.root / "site"
    self.data = self.root / "data"
    shutil.copytree(FIXTURES / "fixture-site", self.site)
    self.data.mkdir()
    for name in ("roadmap.json", "numbers.json"):
      shutil.copyfile(FIXTURES / name, self.data / name)
    self.blocklist = self.root / "blocklist.txt"
    shutil.copyfile(FIXTURES / "blocklist-dummy.txt", self.blocklist)

  def run_check(self, expected=1, extra=()):
    result = subprocess.run(
      [sys.executable, "-I", str(SCRIPTS / "check-site.py"),
       "--site", str(self.site), "--data", str(self.data),
       "--blocklist", str(self.blocklist), *extra],
      capture_output=True, text=True, check=False,
    )
    self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
    self.assertEqual(result.stderr, "")
    lines = result.stdout.splitlines()
    if expected == 0:
      self.assertEqual(lines, ["PASS"])
    else:
      self.assertEqual(lines[-1], f"FAIL {len(lines) - 1}")
      for line in lines[:-1]:
        self.assertRegex(line, r"^FAIL \S+ .+:\d+ .+$")
    return result.stdout

  def edit_page(self, page, old, new):
    path = self.site / page / "index.html"
    text = path.read_text(encoding="utf-8")
    self.assertIn(old, text)
    path.write_text(text.replace(old, new, 1), encoding="utf-8")

  def edit_numbers(self, key, value):
    path = self.data / "numbers.json"
    numbers = json.loads(path.read_text(encoding="utf-8"))
    numbers[key] = value
    path.write_text(json.dumps(numbers), encoding="utf-8")

  def test_real_fixtures_pass_and_inputs_are_unchanged(self):
    before = {path: path.read_bytes() for path in self.root.rglob("*")
              if path.is_file()}
    self.run_check(expected=0)
    after = {path: path.read_bytes() for path in self.root.rglob("*")
             if path.is_file()}
    self.assertEqual(before, after)

  def test_credentials_in_every_supported_extension(self):
    # Assemble dummy values at runtime; never store a token-shaped literal.
    credentials = [prefix + "_" + "a" * 24
                   for prefix in ("ghp", "gho", "ghu", "ghs", "github_pat")]
    credentials += ["sk" + "-" + "b" * 24,
                    "-----BEGIN " + "RSA PRIVATE KEY-----",
                    "password" + "=dummy"]
    for extension in ("html", "xml", "txt", "json", "webmanifest", "js", "css"):
      with self.subTest(extension=extension):
        path = self.site / f"probe.{extension}"
        path.write_text("\n".join(credentials), encoding="utf-8")
        output = self.run_check()
        self.assertEqual(output.count("FAIL credentials "), len(credentials))
        self.assertIn(f"probe.{extension}:1", output)
        for credential in credentials:
          self.assertNotIn(credential, output)
        path.unlink()

  def test_blocklist_hit_is_literal_case_insensitive_and_redacted(self):
    word = "dummy.cue+[sample]"
    self.blocklist.write_text("# ignored\n\n" + word + "\n", encoding="utf-8")
    (self.site / "probe.txt").write_text("safe\n" + word.upper(), encoding="utf-8")
    output = self.run_check()
    self.assertEqual(output, "FAIL blocklist probe.txt:2 blocklist line 3\nFAIL 1\n")
    self.assertNotIn(word, output.casefold())
    (self.site / "probe.txt").write_text("DUMMYxCUEsample", encoding="utf-8")
    self.run_check(expected=0)

  def test_reordered_lists(self):
    for page in ("build", "whats-next"):
      with self.subTest(page=page):
        self.edit_page(page, "<li>Custom roles that take orders on the register.</li>", "<li>SWAP</li>")
        self.edit_page(page, "<li>Staff sales that follow a check when it’s handed to someone else.</li>", "<li>Custom roles that take orders on the register.</li>")
        self.edit_page(page, "<li>SWAP</li>", "<li>Staff sales that follow a check when it’s handed to someone else.</li>")
        self.assertIn(f"FAIL lists {page}/index.html:", self.run_check())
        shutil.copyfile(FIXTURES / "fixture-site" / page / "index.html",
                        self.site / page / "index.html")

  def test_missing_next_item(self):
    self.edit_page("whats-next", "<li>Courses, with hold and fire</li>", "")
    self.assertIn("next: list differs", self.run_check())

  def test_next_must_be_ordered(self):
    self.edit_page("whats-next", "<ol>", "<ul>")
    self.edit_page("whats-next", "</ol>", "</ul>")
    self.assertIn("next: list differs", self.run_check())

  def test_extra_planned_item(self):
    self.edit_page("whats-next", "<li>Card payments</li>", "<li>Extra</li><li>Card payments</li>")
    self.assertIn("planned", self.run_check())

  def test_fixed_planned_items_cannot_change(self):
    for item in ("Card payments", "A live view of the tip pool, so everyone in it sees their share"):
      with self.subTest(item=item):
        self.edit_page("whats-next", f"<li>{item}</li>", "<li>Changed</li>")
        self.assertIn("planned: list differs", self.run_check())
        shutil.copyfile(FIXTURES / "fixture-site/whats-next/index.html",
                        self.site / "whats-next/index.html")

  def test_every_roadmap_list_is_checked(self):
    for key in ("inWorks", "coming", "next", "planned", "ideas"):
      with self.subTest(key=key):
        path = self.data / "roadmap.json"
        original = path.read_text(encoding="utf-8")
        roadmap = json.loads(original)
        roadmap[key].append("Extra data item")
        path.write_text(json.dumps(roadmap), encoding="utf-8")
        self.assertIn(f"{key}: list differs", self.run_check())
        path.write_text(original, encoding="utf-8")

  def test_entities_whitespace_and_inline_markup_are_normalized(self):
    self.edit_page("build", "<h3>In the works</h3>", "<h3> In <em>the</em>\n works </h3>")
    self.edit_page("build", "<li>A notification center.</li>", "<li> A&#32;<em>notification</em>\n center. </li>")
    self.edit_page("whats-next", "manager’s phone.", "manager&#8217;s phone.")
    self.run_check(expected=0)

  def test_missing_heading_or_list(self):
    self.edit_page("whats-next", "<h3>Ideas</h3>", "<h3>Other</h3>")
    self.assertIn("ideas", self.run_check())

  def test_bad_counted_on(self):
    for value in ("invalid", "2026-02-30", "2026-1-02", None,
                  (datetime.date.today() + datetime.timedelta(days=1)).isoformat()):
      with self.subTest(value=value):
        self.edit_numbers("countedOn", value)
        self.assertIn("countedOn", self.run_check())

  def test_counts_are_positive_integers(self):
    for key in ("updates", "changes"):
      for value in (0, -1, True, 1.5, "16", None):
        with self.subTest(key=key, value=value):
          self.edit_numbers(key, value)
          self.assertIn(key, self.run_check())
          shutil.copyfile(FIXTURES / "numbers.json", self.data / "numbers.json")

  def test_counts_must_be_inside_numbers_strip(self):
    self.edit_page("build", "<strong>16</strong>", "<strong>116</strong>")
    self.edit_page("build", "<strong>401</strong>", "<strong>4010</strong>")
    self.edit_page("build", "</main>", "<p>16 401</p></main>")
    output = self.run_check()
    self.assertIn("updates", output)
    self.assertIn("changes", output)

  def test_missing_blocklist_is_usage_error(self):
    self.blocklist.unlink()
    self.assertIn("FAIL usage blocklist:1", self.run_check(expected=2))

  def test_unreadable_blocklist_is_usage_error(self):
    self.blocklist.unlink()
    self.blocklist.mkdir()
    self.assertIn("FAIL usage blocklist:1", self.run_check(expected=2))

  def test_missing_argument_is_usage_error(self):
    result = subprocess.run([sys.executable, "-I", str(SCRIPTS / "check-site.py")],
                            capture_output=True, text=True, check=False)
    self.assertEqual(result.returncode, 2)
    self.assertEqual(result.stderr, "")
    self.assertTrue(result.stdout.endswith("FAIL 1\n"))


if __name__ == "__main__":
  unittest.main()
