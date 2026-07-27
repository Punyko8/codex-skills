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
    def test_target_rate_strips_speaker_and_stage_direction(self) -> None:
        result = analyze_timing("小吉：“让我看看。”（伸手）", 1.8)
        self.assertEqual(result.spoken_units, 4)
        self.assertEqual(result.status, "target")
        self.assertEqual(result.target_duration_min, 1.8)
        self.assertEqual(result.target_duration_max, 2.0)

    def test_too_fast(self) -> None:
        result = analyze_timing("让我看看", 1.5)
        self.assertEqual(result.status, "too_fast")
        self.assertGreater(result.rate, 2.33)

    def test_slow_requires_reason(self) -> None:
        result = analyze_timing("让我看看", 2.5)
        self.assertEqual(result.status, "slow_reason_required")

    def test_ascii_requires_pronunciation_warning(self) -> None:
        result = analyze_timing("我有2个ABC玩具", 2.0)
        self.assertTrue(result.warnings)

    def test_non_positive_duration_is_invalid(self) -> None:
        with self.assertRaises(ValueError):
            analyze_timing("你好", 0)


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
                "1.0",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(json.loads(completed.stdout)["status"], "too_fast")


if __name__ == "__main__":
    unittest.main()
