import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / "jsonl_to_transcript.py"
FIXTURE = HERE / "fixtures" / "sample-subagent.jsonl"


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


if __name__ == "__main__":
    unittest.main()
