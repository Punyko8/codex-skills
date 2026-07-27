"""生产段校验器的单元测试与命令行集成测试。"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "segment_timing_check.py"
sys.path.insert(0, str(SCRIPT.parent))

from segment_timing_check import validate_rows  # noqa: E402


def shot(
    segment: str,
    segment_type: str,
    number: int,
    duration: float,
    **extra: object,
) -> dict[str, object]:
    return {
        "segment": segment,
        "segment_type": segment_type,
        "shot": number,
        "duration": duration,
        "scene": "S01",
        **extra,
    }


class ValidateRowsTest(unittest.TestCase):
    def test_valid_multi_shot_segments(self) -> None:
        rows = [
            shot("段001", "多镜叙事", 1, 2),
            shot("段001", "多镜叙事", 2, 3),
            shot("段002", "快速切镜", 3, 1),
            shot("段002", "快速切镜", 4, 1),
            shot("段002", "快速切镜", 5, 1),
            shot("段002", "快速切镜", 6, 1),
        ]
        report = validate_rows(rows)
        self.assertEqual(report.status, "pass")
        self.assertFalse(report.errors)

    def test_internal_shot_may_be_under_four_but_segment_may_not(self) -> None:
        valid = validate_rows(
            [
                shot("段001", "多镜叙事", 1, 1.5),
                shot("段001", "多镜叙事", 2, 2.5),
            ]
        )
        invalid = validate_rows([shot("段001", "单镜连续", 1, 3.9)])
        self.assertEqual(valid.status, "pass")
        self.assertIn("不在 4–15s", invalid.errors[0])

    def test_segment_over_fifteen_fails(self) -> None:
        report = validate_rows([shot("段001", "单镜连续", 1, 15.1)])
        self.assertEqual(report.status, "fail")

    def test_global_segment_and_shot_numbering_must_be_continuous(self) -> None:
        report = validate_rows(
            [
                shot("段001", "单镜连续", 1, 4),
                shot("段003", "单镜连续", 3, 4),
            ]
        )
        self.assertTrue(any("镜号必须" in message for message in report.errors))
        self.assertTrue(any("段号必须" in message for message in report.errors))

    def test_repeated_segment_type_must_match(self) -> None:
        report = validate_rows(
            [
                shot("段001", "多镜叙事", 1, 2),
                shot("段001", "快速切镜", 2, 2),
            ]
        )
        self.assertTrue(any("相同段类型" in message for message in report.errors))

    def test_all_sounds_must_end_inside_segment(self) -> None:
        report = validate_rows(
            [
                shot(
                    "段001",
                    "单镜连续",
                    1,
                    4,
                    sound_crosses_segment=True,
                )
            ]
        )
        self.assertTrue(any("不得跨段" in message for message in report.errors))

    def test_pure_transition_cannot_add_story_content(self) -> None:
        report = validate_rows(
            [
                shot(
                    "段001",
                    "纯转场",
                    1,
                    4,
                    has_new_dialogue=True,
                )
            ]
        )
        self.assertTrue(any("新对白" in message for message in report.errors))

    def test_single_shot_four_second_generation_can_trim(self) -> None:
        report = validate_rows(
            [
                shot(
                    "段001",
                    "单镜连续",
                    1,
                    4,
                    trim_to=2.5,
                    edit_note="后期建议保留 2.5s，保留抬头到眨眼完成",
                )
            ]
        )
        self.assertEqual(report.status, "pass")

    def test_time_montage_requires_two_evidence_types(self) -> None:
        report = validate_rows(
            [
                shot(
                    "段001",
                    "时间蒙太奇",
                    1,
                    1.5,
                    time_evidence=["光线"],
                ),
                shot("段001", "时间蒙太奇", 2, 1.5),
                shot("段001", "时间蒙太奇", 3, 1.5),
            ]
        )
        self.assertTrue(any("两类" in message for message in report.errors))

    def test_time_evidence_must_be_an_array(self) -> None:
        report = validate_rows(
            [
                shot(
                    "段001",
                    "时间蒙太奇",
                    1,
                    1.5,
                    time_evidence="光线变化",
                ),
                shot("段001", "时间蒙太奇", 2, 1.5),
                shot("段001", "时间蒙太奇", 3, 1.5),
            ]
        )
        self.assertTrue(
            any("必须是时间证据类型数组" in message for message in report.errors)
        )

    def test_over_six_rapid_cuts_warn_unless_special(self) -> None:
        rows = [shot("段001", "快速切镜", number, 1) for number in range(1, 8)]
        regular = validate_rows(rows)
        special = validate_rows([{**row, "special_montage": True} for row in rows])
        self.assertTrue(regular.warnings)
        self.assertFalse(special.warnings)


class CommandLineTest(unittest.TestCase):
    def test_cli_outputs_json_and_returns_zero(self) -> None:
        rows = [shot("段001", "单镜连续", 1, 4)]
        with tempfile.TemporaryDirectory() as directory:
            input_path = Path(directory) / "segments.json"
            input_path.write_text(
                json.dumps(rows, ensure_ascii=False),
                encoding="utf-8",
            )
            completed = subprocess.run(
                [sys.executable, str(SCRIPT), "--input", str(input_path)],
                check=False,
                capture_output=True,
                text=True,
            )
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(json.loads(completed.stdout)["status"], "pass")


if __name__ == "__main__":
    unittest.main()
