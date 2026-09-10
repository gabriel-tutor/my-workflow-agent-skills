import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent


class InitIterationTest(unittest.TestCase):
    def test_single_run_layout_and_prompt(self):
        it = Path(tempfile.mkdtemp()) / "iteration-x"
        subprocess.run([sys.executable, str(REPO / "scripts" / "init_iteration.py"), str(it),
                        "--only", "2", "--configs", "new_skill,without_skill"], check=True, capture_output=True)
        runs = json.loads((it / "runs.json").read_text())
        self.assertEqual([r["config"] for r in runs], ["new_skill", "without_skill"])
        meta = json.loads((it / "eval-2-cosmetic-edit" / "eval_metadata.json").read_text())
        self.assertEqual(meta["eval_id"], 2)
        self.assertEqual(meta["eval_name"], "cosmetic-edit")
        self.assertIn("recieve", meta["prompt"])
        self.assertGreaterEqual(len(meta["assertions"]), 5)
        combo = runs[0]
        self.assertEqual(combo["agent_name"], "e2-combo")
        self.assertTrue(combo["skill_path"].endswith("skills/matt-pocock-superpowers-workflow/SKILL.md"))
        self.assertTrue((Path(combo["workspace"]) / "src" / "format.ts").exists())
        self.assertIn(combo["workspace"], combo["prompt_for_agent"])
        self.assertIn(combo["skill_path"], combo["prompt_for_agent"])
        self.assertIn("outputs/REPORT.md", combo["prompt_for_agent"])
        none = runs[1]
        self.assertIsNone(none["skill_path"])
        self.assertEqual(none["agent_name"], "e2-none")
        self.assertIn("work as you normally would", none["prompt_for_agent"])
        self.assertNotIn("SKILL.md", none["prompt_for_agent"])


class MergeGradingTest(unittest.TestCase):
    def test_normalises_grading_files(self):
        it = Path(tempfile.mkdtemp())
        run = it / "eval-9-x" / "new_skill" / "run-1"
        (run / "outputs").mkdir(parents=True)
        (run / "outputs" / "REPORT.md").write_text("hello world")
        (run / "metrics.json").write_text(json.dumps({"tool_calls": {"Bash": 3}, "total_tool_calls": 3, "total_steps": 2, "errors_encountered": 1, "transcript_chars": 500}))
        (run / "grading.json").write_text(json.dumps({
            "expectations": [{"text": "a", "passed": True, "evidence": "x"}, {"text": "b", "passed": False, "evidence": "y"}],
            "summary": {"passed": 9, "failed": 9, "total": 9, "pass_rate": 9.0},
            "timing": {"total_duration_seconds": 1.0},
        }))
        subprocess.run([sys.executable, str(REPO / "scripts" / "merge_grading.py"), str(it)], check=True, capture_output=True)
        g = json.loads((run / "grading.json").read_text())
        self.assertNotIn("timing", g)
        self.assertEqual(g["summary"], {"passed": 1, "failed": 1, "total": 2, "pass_rate": 0.5})
        self.assertEqual(g["execution_metrics"]["total_tool_calls"], 3)
        self.assertEqual(g["execution_metrics"]["errors_encountered"], 1)
        self.assertEqual(g["execution_metrics"]["output_chars"], 11)


if __name__ == "__main__":
    unittest.main()
