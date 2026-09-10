import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / "jsonl_to_transcript.py"
FIXTURE = HERE / "fixtures" / "sample-subagent.jsonl"

sys.path.insert(0, str(SCRIPT.parent))
from jsonl_to_transcript import bash_writes


class JsonlToTranscriptTest(unittest.TestCase):
    def setUp(self):
        self.run_dir = Path(tempfile.mkdtemp())
        subprocess.run([sys.executable, str(SCRIPT), str(FIXTURE), str(self.run_dir)], check=True)

    def test_events_are_ordered_and_typed(self):
        events = json.loads((self.run_dir / "events.json").read_text())
        self.assertEqual([e["tool"] for e in events], ["Skill", "Bash", "Edit", "Agent"])
        self.assertEqual([e["i"] for e in events], [0, 1, 2, 3])
        self.assertEqual(events[0]["skill"], "superpowers:test-driven-development")
        self.assertEqual(events[2]["path"], "/ws/src/pricing.ts")
        self.assertEqual(events[3]["description"], "Review the diff")

    def test_bash_writes_are_extracted(self):
        events = json.loads((self.run_dir / "events.json").read_text())
        self.assertEqual(events[1]["writes"], ["tests/coupons.test.ts", "/tmp/out.txt"])
        self.assertTrue(events[1]["command"].startswith("cd /ws && cat >"))

    def test_metrics(self):
        m = json.loads((self.run_dir / "metrics.json").read_text())
        self.assertEqual(m["tool_calls"], {"Skill": 1, "Bash": 1, "Edit": 1, "Agent": 1})
        self.assertEqual(m["total_tool_calls"], 4)
        self.assertEqual(m["total_steps"], 3)
        self.assertEqual(m["errors_encountered"], 1)
        self.assertEqual(m["usage"]["output_tokens"], 21)
        self.assertEqual(m["usage"]["cache_read_input_tokens"], 300)
        self.assertGreater(m["transcript_chars"], 100)

    def test_transcript_has_prompt_calls_and_results_but_no_thinking(self):
        t = (self.run_dir / "transcript.md").read_text()
        self.assertIn("Execute this task: add applyCoupon.", t)
        self.assertIn("**Skill** superpowers:test-driven-development", t)
        self.assertIn("**Edit** /ws/src/pricing.ts", t)
        self.assertIn("FAIL tests/coupons.test.ts", t)
        self.assertIn("(error)", t)
        self.assertNotIn("secret", t)

    def test_sed_target_captured_in_compound_command(self):
        self.assertEqual(
            bash_writes("sed -i '' 's/recieve/receive/' src/format.ts && npm test"),
            ["src/format.ts"],
        )
        self.assertEqual(
            bash_writes("cd /ws && sed -i '' 's/a/b/' src/x.ts; npx vitest run"),
            ["src/x.ts"],
        )

    def test_malformed_line_is_skipped_not_fatal(self):
        run_dir = Path(tempfile.mkdtemp())
        lines = FIXTURE.read_text().splitlines()
        lines.append('{"type": "assistant", "message": ')
        bad_jsonl = run_dir / "input.jsonl"
        bad_jsonl.write_text("\n".join(lines) + "\n")

        result = subprocess.run([sys.executable, str(SCRIPT), str(bad_jsonl), str(run_dir)])

        self.assertEqual(result.returncode, 0)
        events = json.loads((run_dir / "events.json").read_text())
        self.assertEqual(len(events), 4)
        metrics = json.loads((run_dir / "metrics.json").read_text())
        self.assertEqual(metrics["malformed_lines"], 1)


if __name__ == "__main__":
    unittest.main()
