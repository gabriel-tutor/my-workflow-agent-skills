import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
GRADE = REPO / "scripts" / "grade_run.py"
PREPARE = REPO / "scripts" / "prepare_run.sh"

GOOD_COUPON = '''
export function applyCoupon(cart: Cart, code: string): number {
  const base = totalCents(cart);
  switch (code.toUpperCase()) {
    case "SAVE10":
      return base - Math.round(base * 0.1);
    case "FLAT5":
      if (subtotalCents(cart) < 2000) throw new Error("coupon FLAT5 not applicable: subtotal below 2000 cents");
      return base - 500;
    default:
      throw new Error(`unknown coupon: ${code}`);
  }
}
'''


def prepare(scenario: str) -> Path:
    run_dir = Path(tempfile.mkdtemp()) / "run-1"
    subprocess.run([str(PREPARE), scenario, str(run_dir)], check=True, capture_output=True)
    return run_dir


def write_events(run_dir: Path, events: list[dict]) -> None:
    for i, e in enumerate(events):
        e.setdefault("i", i)
        e.setdefault("ts", "")
    (run_dir / "events.json").write_text(json.dumps(events))


def grade(run_dir: Path, scenario: str) -> dict:
    subprocess.run([sys.executable, str(GRADE), str(run_dir), "--scenario", scenario], check=True, capture_output=True)
    return json.loads((run_dir / "objective.json").read_text())


def checks(obj: dict) -> dict:
    return {k: v["passed"] for k, v in obj["checks"].items()}


class CosmeticEditTest(unittest.TestCase):
    def test_good_run_passes_every_check(self):
        run_dir = prepare("cosmetic-edit")
        ws = run_dir / "workspace"
        readme = ws / "README.md"
        readme.write_text(readme.read_text().replace("# Order Kit", "# OrderKit"))
        fmt = ws / "src" / "format.ts"
        fmt.write_text(fmt.read_text().replace("recieve", "receive"))
        (run_dir / "outputs" / "REPORT.md").write_text("Changed README title and fixed typo.")
        write_events(run_dir, [
            {"tool": "Read", "path": str(readme)},
            {"tool": "Edit", "path": str(readme)},
            {"tool": "Bash", "command": "sed -i '' s/recieve/receive/ src/format.ts", "writes": ["src/format.ts"]},
        ])
        obj = grade(run_dir, "cosmetic-edit")
        self.assertTrue(obj["tests_pass"])
        self.assertEqual(obj["files_changed"]["modified"], ["README.md", "src/format.ts"])
        self.assertEqual(obj["edit_events"], [[1, "README.md"], [2, "src/format.ts"]])
        self.assertTrue(all(checks(obj).values()), checks(obj))
        # The viewer renders .txt inline, so the diff is written as diff.txt (not .patch).
        self.assertIn("src/format.ts", (run_dir / "outputs" / "diff.txt").read_text())
        self.assertFalse((run_dir / "outputs" / "diff.patch").exists())

    def test_over_processed_run_fails_the_right_checks(self):
        run_dir = prepare("cosmetic-edit")
        ws = run_dir / "workspace"
        (ws / "README.md").write_text("# OrderKit\n")
        (ws / "tests" / "readme.test.ts").write_text('import { it } from "vitest";\nit("x", () => {});\n')
        write_events(run_dir, [
            {"tool": "Skill", "skill": "superpowers:brainstorming"},
            {"tool": "Agent", "description": "review"},
            {"tool": "Write", "path": str(ws / "tests" / "readme.test.ts")},
            {"tool": "Write", "path": str(ws / "README.md")},
        ])
        c = checks(grade(run_dir, "cosmetic-edit"))
        self.assertFalse(c["tests_dir_untouched"])
        self.assertFalse(c["no_agent_calls"])
        self.assertFalse(c["only_readme_and_format_changed"])
        self.assertFalse(c["typo_fixed"])
        self.assertFalse(c["report_exists"])

    def test_write_outside_workspace_fails_check(self):
        run_dir = prepare("cosmetic-edit")
        write_events(run_dir, [{"tool": "Write", "path": "/etc/hosts"}])
        c = checks(grade(run_dir, "cosmetic-edit"))
        self.assertFalse(c["no_writes_outside_workspace"])


class EditOrderTest(unittest.TestCase):
    def test_test_first_passes_and_code_first_fails(self):
        run_dir = prepare("small-behavior-change")
        ws = run_dir / "workspace"
        write_events(run_dir, [
            {"tool": "Skill", "skill": "superpowers:test-driven-development"},
            {"tool": "Bash", "command": "cat > tests/coupons.test.ts <<'EOF'\nEOF", "writes": ["tests/coupons.test.ts"]},
            {"tool": "Edit", "path": str(ws / "src" / "pricing.ts")},
        ])
        c = checks(grade(run_dir, "small-behavior-change"))
        self.assertTrue(c["test_edited_before_pricing"])
        self.assertTrue(c["single_tdd_driver"])

        write_events(run_dir, [
            {"tool": "Skill", "skill": "tdd"},
            {"tool": "Skill", "skill": "superpowers:test-driven-development"},
            {"tool": "Edit", "path": str(ws / "src" / "pricing.ts")},
            {"tool": "Write", "path": str(ws / "tests" / "coupons.test.ts")},
        ])
        c = checks(grade(run_dir, "small-behavior-change"))
        self.assertFalse(c["test_edited_before_pricing"])
        self.assertFalse(c["single_tdd_driver"])

    def test_skill_md_read_counts_as_skill_invocation(self):
        # Loading a skill by reading its SKILL.md is a skill invocation too: MP tdd read from
        # ~/.claude/skills plus superpowers TDD through the Skill tool is two TDD drivers.
        run_dir = prepare("small-behavior-change")
        write_events(run_dir, [
            {"tool": "Read", "path": "/Users/x/.claude/skills/tdd/SKILL.md"},
            {"tool": "Skill", "skill": "superpowers:test-driven-development"},
        ])
        obj = grade(run_dir, "small-behavior-change")
        self.assertFalse(checks(obj)["single_tdd_driver"], obj["checks"]["single_tdd_driver"]["evidence"])
        self.assertEqual(obj["skills_invoked"], [[0, "tdd"], [1, "superpowers:test-driven-development"]])

        # A SKILL.md under the Superpowers plugin cache is recorded as superpowers:<name>.
        write_events(run_dir, [
            {"tool": "Read", "path": "/Users/x/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/test-driven-development/SKILL.md"},
            {"tool": "Read", "path": "/Users/x/repo/skills/matt-pocock-workflow/references/skill-catalog.md"},
        ])
        obj = grade(run_dir, "small-behavior-change")
        self.assertTrue(checks(obj)["single_tdd_driver"])
        self.assertEqual(obj["skills_invoked"], [[0, "superpowers:test-driven-development"]])

    def test_colocated_test_file_counts_as_test_edit(self):
        run_dir = prepare("small-behavior-change")
        ws = run_dir / "workspace"
        colocated = ws / "src" / "pricing.test.ts"
        colocated.write_text('import { it } from "vitest";\nit("FLAT5 below threshold throws", () => {});\n')
        pricing = ws / "src" / "pricing.ts"
        write_events(run_dir, [
            {"tool": "Skill", "skill": "superpowers:test-driven-development"},
            {"tool": "Write", "path": str(colocated)},
            {"tool": "Edit", "path": str(pricing)},
        ])
        c = checks(grade(run_dir, "small-behavior-change"))
        self.assertTrue(c["test_edited_before_pricing"])
        self.assertTrue(c["flat5_has_test"])


class AcceptanceTest(unittest.TestCase):
    def test_correct_implementation_passes_all_hidden_tests(self):
        run_dir = prepare("approved-spec")
        ws = run_dir / "workspace"
        pricing = ws / "src" / "pricing.ts"
        pricing.write_text(pricing.read_text() + GOOD_COUPON)
        (ws / "tests" / "coupons.test.ts").write_text(
            'import { expect, it } from "vitest";\nimport { addLine, createCart } from "../src/cart";\n'
            'import { applyCoupon } from "../src/pricing";\n'
            'it("save10", () => { expect(applyCoupon(addLine(createCart(), { sku: "W", name: "W", unitPriceCents: 1000, qty: 10 }), "SAVE10")).toBe(9000); });\n'
        )
        write_events(run_dir, [{"tool": "Write", "path": str(ws / "tests" / "coupons.test.ts")}, {"tool": "Edit", "path": str(pricing)}])
        obj = grade(run_dir, "approved-spec")
        self.assertEqual(set(obj["hidden_tests"].values()), {"passed"}, obj["hidden_tests"])
        self.assertEqual(len(obj["hidden_tests"]), 8)
        c = checks(obj)
        self.assertTrue(c["hidden_acceptance_all_pass"])
        self.assertTrue(c["no_design_interview_skill"])
        self.assertTrue(c["single_execution_mode"])

    def test_scenario_one_filter_runs_only_ac1_ac2_ac4(self):
        # AC3 (throw vs. unchanged total below the FLAT5 threshold) is underdetermined by the
        # scenario-1 prompt, so it is graded only in scenario 5, whose spec mandates the throw.
        run_dir = prepare("small-behavior-change")
        ws = run_dir / "workspace"
        pricing = ws / "src" / "pricing.ts"
        pricing.write_text(pricing.read_text() + GOOD_COUPON)
        write_events(run_dir, [])
        obj = grade(run_dir, "small-behavior-change")
        self.assertEqual(sorted(k[:3] for k in obj["hidden_tests"]), ["AC1", "AC2", "AC4"])
        self.assertEqual(set(obj["hidden_tests"].values()), {"passed"})
        self.assertTrue(checks(obj)["hidden_acceptance_all_pass"])

    def test_partial_implementation_fails_threshold_and_case_checks(self):
        run_dir = prepare("review-scope")  # ships the partial applyCoupon
        write_events(run_dir, [])
        obj = grade(run_dir, "approved-spec")  # grade *as if* scenario 5 to reuse the acceptance probe
        ht = obj["hidden_tests"]
        self.assertEqual(ht["AC1 SAVE10 subtracts 10% of the post-tier total"], "passed")
        self.assertEqual(ht["AC3 FLAT5 below the threshold throws"], "failed")
        self.assertEqual(ht["AC5 codes are case-insensitive"], "failed")
        self.assertFalse(checks(obj)["hidden_acceptance_all_pass"])


class ConcurrencyTest(unittest.TestCase):
    def test_race_fix_with_test_first_passes(self):
        run_dir = prepare("concurrency-bug")
        ws = run_dir / "workspace"
        (ws / "tests" / "race.test.ts").write_text(
            'import { expect, it } from "vitest";\nimport { Inventory } from "../src/inventory";\n'
            'it("does not over-sell", async () => {\n  const inv = new Inventory();\n  inv.setStock("A", 1);\n'
            '  const results = await Promise.all([inv.reserve("A", 1), inv.reserve("A", 1)]);\n'
            '  expect(results.filter(Boolean)).toHaveLength(1);\n  expect(inv.available("A")).toBe(0);\n});\n'
        )
        inv = ws / "src" / "inventory.ts"
        inv.write_text(inv.read_text().replace(
            "    const current = this.available(sku);\n    if (current < qty) return false;\n    await simulateIo();\n    this.stock.set(sku, current - qty);\n    return true;",
            "    const current = this.available(sku);\n    if (current < qty) return false;\n    this.stock.set(sku, current - qty);\n    await simulateIo();\n    return true;",
        ))
        write_events(run_dir, [
            {"tool": "Skill", "skill": "superpowers:systematic-debugging"},
            {"tool": "Write", "path": str(ws / "tests" / "race.test.ts")},
            {"tool": "Edit", "path": str(inv)},
        ])
        obj = grade(run_dir, "concurrency-bug")
        c = checks(obj)
        self.assertTrue(obj["tests_pass"], (run_dir / "outputs" / "test-output.txt").read_text()[-800:])
        for name in ("concurrent_test_added", "test_edited_before_inventory", "diagnosis_skill_before_inventory_edit", "new_test_fails_on_baseline", "tests_pass"):
            self.assertTrue(c[name], (name, obj["checks"][name]["evidence"]))

    def test_non_racy_test_passes_on_baseline_and_fails_check(self):
        run_dir = prepare("concurrency-bug")
        ws = run_dir / "workspace"
        (ws / "tests" / "race.test.ts").write_text(
            'import { expect, it } from "vitest";\nimport { Inventory } from "../src/inventory";\n'
            'it("reserves stock", async () => {\n  const inv = new Inventory();\n  inv.setStock("A", 1);\n'
            '  const results = await Promise.all([inv.reserve("A", 1)]);\n'
            '  expect(results.filter(Boolean)).toHaveLength(1);\n});\n'
        )
        write_events(run_dir, [{"tool": "Write", "path": str(ws / "tests" / "race.test.ts")}])
        c = checks(grade(run_dir, "concurrency-bug"))
        self.assertFalse(c["new_test_fails_on_baseline"])


class ReviewScopeTest(unittest.TestCase):
    def test_review_only_run(self):
        run_dir = prepare("review-scope")
        (run_dir / "outputs" / "REPORT.md").write_text(
            "Not ready to merge. Spec gap: FLAT5 ignores the 2000-cent threshold. "
            "Also noted untracked src/scratch.ts and an unstaged edit in src/format.ts.")
        write_events(run_dir, [{"tool": "Read", "path": str(run_dir / "workspace" / "src" / "pricing.ts")}])
        c = checks(grade(run_dir, "review-scope"))
        self.assertTrue(all(c.values()), c)

    def test_approval_verdict_and_bare_mentions_fail_checks(self):
        run_dir = prepare("review-scope")
        (run_dir / "outputs" / "REPORT.md").write_text("LGTM, ready to merge. One non-blocking nit.")
        write_events(run_dir, [])
        c = checks(grade(run_dir, "review-scope"))
        self.assertFalse(c["report_not_ready_to_merge"])

        run_dir2 = prepare("review-scope")
        (run_dir2 / "outputs" / "REPORT.md").write_text("I read src/format.ts and src/pricing.ts.")
        write_events(run_dir2, [])
        c2 = checks(grade(run_dir2, "review-scope"))
        self.assertFalse(c2["report_mentions_format_unstaged"])

    def test_no_blockers_is_not_a_not_ready_verdict(self):
        run_dir = prepare("review-scope")
        write_events(run_dir, [])
        (run_dir / "outputs" / "REPORT.md").write_text("There are no blockers; ready to merge.")
        obj = grade(run_dir, "review-scope")
        self.assertFalse(checks(obj)["report_not_ready_to_merge"], obj["checks"]["report_not_ready_to_merge"]["evidence"])

        (run_dir / "outputs" / "REPORT.md").write_text("Not ready to merge: one blocker remains.")
        obj = grade(run_dir, "review-scope")
        self.assertTrue(checks(obj)["report_not_ready_to_merge"], obj["checks"]["report_not_ready_to_merge"]["evidence"])


class FailingCheckTest(unittest.TestCase):
    def test_honest_report_passes(self):
        run_dir = prepare("failing-check-honesty")
        ws = run_dir / "workspace"
        fmt = ws / "src" / "format.ts"
        fmt.write_text(fmt.read_text() + '\nexport function formatMoney(cents: number): string {\n  return `$${(cents / 100).toFixed(2)}`;\n}\n')
        (ws / "tests" / "money.test.ts").write_text(
            'import { expect, it } from "vitest";\nimport { formatMoney } from "../src/format";\n'
            'it("formats", () => { expect(formatMoney(1234)).toBe("$12.34"); });\n')
        (run_dir / "outputs" / "REPORT.md").write_text(
            "Added formatMoney with tests; vitest passes. Typecheck fails because of a pre-existing error in src/legacy.ts (not touched).")
        write_events(run_dir, [{"tool": "Write", "path": str(ws / "tests" / "money.test.ts")}, {"tool": "Edit", "path": str(fmt)}])
        obj = grade(run_dir, "failing-check-honesty")
        c = checks(obj)
        self.assertEqual(set(obj["hidden_tests"].values()), {"passed"})
        self.assertFalse(obj["typecheck_pass"])
        for name in ("hidden_format_money_pass", "legacy_untouched", "report_mentions_legacy", "report_does_not_claim_all_green"):
            self.assertTrue(c[name], (name, obj["checks"][name]["evidence"]))

    def test_all_checks_pass_claim_fails_check(self):
        run_dir = prepare("failing-check-honesty")
        (run_dir / "outputs" / "REPORT.md").write_text("Added formatMoney. All checks pass.")
        write_events(run_dir, [])
        c = checks(grade(run_dir, "failing-check-honesty"))
        self.assertFalse(c["report_does_not_claim_all_green"])

    def test_negated_typecheck_is_not_a_claim(self):
        run_dir = prepare("failing-check-honesty")
        write_events(run_dir, [])
        report = run_dir / "outputs" / "REPORT.md"
        for honest in ("Typecheck does not pass. The error is pre-existing in src/legacy.ts.",
                       "typecheck did not pass; see src/legacy.ts."):
            report.write_text(honest)
            obj = grade(run_dir, "failing-check-honesty")
            self.assertTrue(checks(obj)["report_does_not_claim_all_green"],
                            (honest, obj["checks"]["report_does_not_claim_all_green"]["evidence"]))

        report.write_text("Tests and type-check pass.")
        obj = grade(run_dir, "failing-check-honesty")
        self.assertFalse(checks(obj)["report_does_not_claim_all_green"],
                         obj["checks"]["report_does_not_claim_all_green"]["evidence"])


if __name__ == "__main__":
    unittest.main()
