"""对白语速校验器的单元测试与命令行集成测试。"""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "dialogue_timing_check.py"
sys.path.insert(0, str(SCRIPT.parent))

from dialogue_timing_check import analyze_timing  # noqa: E402


class AnalyzeTimingTest(unittest.TestCase):
    def test_slow_tier_strips_speaker_and_stage_direction(self) -> None:
        result = analyze_timing("小吉：“让我看看。”（伸手）", 1.8, "慢")
        self.assertEqual(result.spoken_units, 4)
        self.assertEqual(result.status, "target")
        self.assertEqual(result.target_duration_min, 1.8)
        self.assertEqual(result.target_duration_max, 2.0)

    def test_medium_tier(self) -> None:
        result = analyze_timing("皮皮站起来很生气地向爸爸大声投诉", 6.0, "中")
        self.assertEqual(result.spoken_units, 16)
        self.assertEqual(result.rate, 2.667)
        self.assertEqual(result.actual_tier, "中")
        self.assertEqual(result.status, "target")

    def test_fast_tier_upper_boundary(self) -> None:
        result = analyze_timing("一" * 33, 10.0, "快")
        self.assertEqual(result.rate, 3.3)
        self.assertEqual(result.status, "target")

    def test_too_fast(self) -> None:
        result = analyze_timing("让我看看", 1.0, "快")
        self.assertEqual(result.status, "too_fast")
        self.assertGreater(result.rate, 3.3)

    def test_slow_requires_reason(self) -> None:
        result = analyze_timing("让我看看", 2.5, "慢")
        self.assertEqual(result.status, "slow_reason_required")

    def test_slow_with_reason_is_allowed(self) -> None:
        result = analyze_timing("让我看看", 2.5, "慢", "皮皮哽咽后留出理解停顿")
        self.assertEqual(result.status, "slow_with_reason")

    def test_tier_mismatch(self) -> None:
        result = analyze_timing("让我看看", 1.5, "慢")
        self.assertEqual(result.actual_tier, "中")
        self.assertEqual(result.status, "tier_mismatch")

    def test_ascii_requires_pronunciation_warning(self) -> None:
        result = analyze_timing("我有2个ABC玩具", 2.0, "慢")
        self.assertTrue(result.warnings)

    def test_non_positive_duration_is_invalid(self) -> None:
        with self.assertRaises(ValueError):
            analyze_timing("你好", 0, "慢")


class CommandLineTest(unittest.TestCase):
    def test_cli_target_returns_zero_and_json(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--text",
                "皮皮：你好呀",
                "--duration",
                "1.5",
                "--tier",
                "慢",
                "--json",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["spoken_units"], 3)
        self.assertEqual(payload["status"], "target")

    def test_cli_too_fast_returns_one(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--text",
                "皮皮：你好呀",
                "--duration",
                "0.8",
                "--tier",
                "快",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(json.loads(completed.stdout)["status"], "too_fast")

    def test_cli_tier_mismatch_returns_one(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--text",
                "皮皮：你好呀",
                "--duration",
                "1.0",
                "--tier",
                "慢",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(json.loads(completed.stdout)["status"], "tier_mismatch")


if __name__ == "__main__":
    unittest.main()
