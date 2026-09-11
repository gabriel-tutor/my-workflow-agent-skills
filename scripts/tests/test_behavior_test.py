"""The behavior-test harness's stream scanner, driven through `behavior_test.py scan <stream>`.

A run's verdict is its first committing call: a Skill or AskUserQuestion call (a process
choice) or an Edit/Write (straight to code). The scanner records that call, the exploring
tool calls before it, the assistant text before it, and, when no such call happens, the
final result.
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
HARNESS = REPO / "scripts" / "behavior_test.py"

INIT = {"type": "system", "subtype": "init", "model": "claude-opus-5"}


def assistant(*blocks):
    return {"type": "assistant", "message": {"role": "assistant", "content": list(blocks)}}


def tool(name, **inputs):
    return {"type": "tool_use", "id": f"toolu_{name}", "name": name, "input": inputs}


def text(value):
    return {"type": "text", "text": value}


def scan(*items):
    """Scan a stream built from event dicts and raw (possibly malformed) lines."""
    lines = (json.dumps(i) if isinstance(i, dict) else i for i in items)
    with tempfile.TemporaryDirectory() as d:
        stream = Path(d) / "stream.jsonl"
        stream.write_text("".join(line + "\n" for line in lines))
        out = subprocess.run([sys.executable, str(HARNESS), "scan", str(stream)],
                             capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


class ScanTest(unittest.TestCase):
    def test_first_skill_after_exploration(self):
        r = scan(INIT,
                 assistant(tool("Read", file_path="src/inventory.ts")),
                 assistant(text("Using diagnosing-bugs."), tool("Skill", skill="diagnosing-bugs")))
        self.assertEqual(r["first_tool"], "Skill")
        self.assertEqual(r["skill"], "diagnosing-bugs")
        self.assertEqual(r["before"], ["Read"])
        self.assertEqual(r["text"], "Using diagnosing-bugs.")
        self.assertEqual(r["model"], "claude-opus-5")

    def test_only_the_first_committing_call_counts(self):
        r = scan(INIT, assistant(tool("Skill", skill="tdd")), assistant(tool("Skill", skill="code-review")))
        self.assertEqual(r["skill"], "tdd")

    def test_an_edit_before_any_skill_is_the_verdict(self):
        r = scan(INIT,
                 assistant(tool("Read", file_path="README.md")),
                 assistant(tool("Edit", file_path="README.md")),
                 assistant(tool("Skill", skill="tdd")))
        self.assertEqual((r["first_tool"], r["skill"], r["before"]), ("Edit", None, ["Read"]))

    def test_skill_later_in_the_same_message(self):
        r = scan(INIT, assistant(tool("Grep", pattern="reserve"), tool("Skill", skill="diagnosing-bugs")))
        self.assertEqual((r["skill"], r["before"]), ("diagnosing-bugs", ["Grep"]))

    def test_ask_user_question_counts_its_questions(self):
        r = scan(INIT, assistant(tool("AskUserQuestion", questions=[{"question": "Which seam?"}])))
        self.assertEqual((r["first_tool"], r["skill"], r["questions"]), ("AskUserQuestion", None, 1))

    def test_no_committing_call_keeps_the_result(self):
        r = scan(INIT,
                 assistant(tool("Read", file_path="src/pricing.ts")),
                 assistant(text("Which coupon codes should stack?")),
                 {"type": "result", "subtype": "success", "result": "Which coupon codes should stack?",
                  "total_cost_usd": 0.12})
        self.assertIsNone(r["first_tool"])
        self.assertEqual(r["before"], ["Read"])
        self.assertEqual(r["result"], "Which coupon codes should stack?")
        self.assertEqual(r["cost_usd"], 0.12)

    def test_malformed_lines_are_skipped(self):
        r = scan(INIT, "not json", "[1, 2]", assistant(tool("Skill", skill="diagnosing-bugs")))
        self.assertEqual(r["skill"], "diagnosing-bugs")


if __name__ == "__main__":
    unittest.main()
