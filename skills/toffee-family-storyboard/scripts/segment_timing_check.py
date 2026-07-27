#!/usr/bin/env python3
"""校验一次视频生成任务对应的生产段编号、类型、镜数和总时长。"""

from __future__ import annotations

import argparse
import json
import math
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

SEGMENT_RE = re.compile(r"^段(\d{3})$")
SHOT_RE = re.compile(r"^(?:镜)?(\d+)$")
SCENE_RE = re.compile(r"^S(\d+)$")
ALLOWED_TYPES = {
    "单镜连续",
    "多镜叙事",
    "快速切镜",
    "纯转场",
    "时间蒙太奇",
}
MIN_DURATION = 4.0
MAX_DURATION = 15.0


@dataclass(frozen=True)
class SegmentResult:
    segment: str
    segment_type: str
    shots: list[str]
    duration_seconds: float
    errors: list[str]
    warnings: list[str]


@dataclass(frozen=True)
class ValidationReport:
    status: str
    segment_count: int
    shot_count: int
    errors: list[str]
    warnings: list[str]
    segments: list[SegmentResult]


def parse_positive_number(value: Any, field: str) -> float:
    """解析正数并拒绝布尔值、NaN 与无穷值。"""

    if isinstance(value, bool):
        raise ValueError(f"{field} 必须为正数")
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} 必须为正数") from exc
    if not math.isfinite(number) or number <= 0:
        raise ValueError(f"{field} 必须为正数")
    return number


def parse_shot_number(value: Any) -> int:
    """接受整数、数字字符串或“镜001”格式。"""

    if isinstance(value, bool):
        raise ValueError("镜号必须为正整数")
    match = SHOT_RE.fullmatch(str(value))
    if not match or int(match.group(1)) <= 0:
        raise ValueError("镜号必须为正整数或“镜001”格式")
    return int(match.group(1))


def load_rows(path: Path) -> list[dict[str, Any]]:
    """读取 JSON 数组，或读取含 shots 数组的对象。"""

    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = payload.get("shots") if isinstance(payload, dict) else payload
    if not isinstance(rows, list) or not rows:
        raise ValueError("输入必须是非空 JSON 数组，或含非空 shots 数组的对象")
    if not all(isinstance(row, dict) for row in rows):
        raise ValueError("每个镜头必须是 JSON 对象")
    return rows


def validate_rows(rows: list[dict[str, Any]]) -> ValidationReport:
    """按表格顺序校验生产段与镜号，不另建段级总表。"""

    global_errors: list[str] = []
    global_warnings: list[str] = []
    normalized: list[dict[str, Any]] = []

    for index, row in enumerate(rows, start=1):
        prefix = f"第 {index} 行"
        segment = row.get("segment")
        match = SEGMENT_RE.fullmatch(str(segment))
        if not match:
            global_errors.append(f"{prefix}：段号必须使用“段001”三位格式")
            segment_number = -1
        else:
            segment_number = int(match.group(1))

        segment_type = row.get("segment_type")
        if segment_type not in ALLOWED_TYPES:
            global_errors.append(f"{prefix}：未知段类型“{segment_type}”")

        try:
            shot_number = parse_shot_number(row.get("shot"))
        except ValueError as exc:
            global_errors.append(f"{prefix}：{exc}")
            shot_number = -1

        try:
            duration = parse_positive_number(row.get("duration"), "镜头时长")
        except ValueError as exc:
            global_errors.append(f"{prefix}：{exc}")
            duration = 0.0

        normalized.append(
            {
                **row,
                "segment": str(segment),
                "segment_number": segment_number,
                "segment_type": str(segment_type),
                "shot_number": shot_number,
                "duration": duration,
            }
        )

    valid_shots = [row["shot_number"] for row in normalized if row["shot_number"] > 0]
    if valid_shots:
        expected = list(range(1, len(valid_shots) + 1))
        if valid_shots != expected:
            global_errors.append(
                f"镜号必须从 1 开始按整集连续排列；当前为 {valid_shots}"
            )

    segment_order: list[str] = []
    grouped: dict[str, list[dict[str, Any]]] = {}
    closed_segments: set[str] = set()
    previous_segment: str | None = None
    for row in normalized:
        segment = row["segment"]
        if segment != previous_segment:
            if segment in closed_segments:
                global_errors.append(f"{segment} 在表中重复出现为非连续区块")
            if previous_segment is not None:
                closed_segments.add(previous_segment)
            previous_segment = segment
        if segment not in grouped:
            segment_order.append(segment)
            grouped[segment] = []
        grouped[segment].append(row)

    valid_segment_numbers = [
        grouped[segment][0]["segment_number"]
        for segment in segment_order
        if grouped[segment][0]["segment_number"] > 0
    ]
    if valid_segment_numbers:
        expected = list(range(1, len(valid_segment_numbers) + 1))
        if valid_segment_numbers != expected:
            global_errors.append(
                "段号必须从段001开始按整集连续排列；" f"当前为 {valid_segment_numbers}"
            )

    segment_results: list[SegmentResult] = []
    for segment in segment_order:
        segment_rows = grouped[segment]
        errors: list[str] = []
        warnings: list[str] = []
        types = {row["segment_type"] for row in segment_rows}
        segment_type = segment_rows[0]["segment_type"]
        if len(types) != 1:
            errors.append("同一段的每个镜头必须重复填写相同段类型")

        duration = round(sum(row["duration"] for row in segment_rows), 3)
        if duration < MIN_DURATION - 1e-9 or duration > MAX_DURATION + 1e-9:
            errors.append(f"段总时长 {duration:g}s 不在 4–15s 硬范围内")

        shot_count = len(segment_rows)
        special_montage = any(bool(row.get("special_montage")) for row in segment_rows)
        if segment_type == "单镜连续" and shot_count != 1:
            errors.append("单镜连续必须恰好包含 1 个镜头")
        elif segment_type == "多镜叙事" and not 2 <= shot_count <= 3:
            warnings.append("多镜叙事通常包含 2–3 个镜头，请复核是否应拆段或改类型")
        elif segment_type == "快速切镜" and not 4 <= shot_count <= 6:
            if not (shot_count > 6 and special_montage):
                warnings.append("快速切镜通常包含 4–6 个镜头")
        elif segment_type == "时间蒙太奇":
            if not 3 <= shot_count <= 6 and not (shot_count > 6 and special_montage):
                warnings.append("时间蒙太奇通常包含 3–6 个镜头")
            evidence: set[str] = set()
            for row in segment_rows:
                row_evidence = row.get("time_evidence", [])
                if not isinstance(row_evidence, list):
                    errors.append("time_evidence 必须是时间证据类型数组")
                    continue
                evidence.update(
                    str(item).strip() for item in row_evidence if str(item).strip()
                )
            if len(evidence) < 2:
                errors.append("时间蒙太奇必须至少提供两类 time_evidence 时间证据")
            if any(row.get("dialogue_continues_across_jump") for row in segment_rows):
                errors.append("连续对白不得跨越时间蒙太奇中的时间跳跃")
        elif segment_type == "纯转场":
            if shot_count > 6:
                warnings.append("纯转场超过 6 镜，通常应拆段")
            forbidden = {
                "has_new_dialogue": "新对白",
                "has_educational_point": "教育点",
                "has_new_conflict": "新冲突",
            }
            present = [
                label
                for key, label in forbidden.items()
                if any(bool(row.get(key)) for row in segment_rows)
            ]
            if present:
                errors.append(f"纯转场不得承担{'、'.join(present)}")

        scenes = [
            str(row["scene"])
            for row in segment_rows
            if row.get("scene") is not None and str(row["scene"]).strip()
        ]
        unique_scenes = list(dict.fromkeys(scenes))
        if segment_type != "纯转场" and len(unique_scenes) > 1:
            errors.append("普通段不得跨场景")
        elif segment_type == "纯转场" and len(unique_scenes) > 2:
            errors.append("纯转场只能跨相邻的两个场景")
        elif segment_type == "纯转场" and len(unique_scenes) == 2:
            scene_matches = [SCENE_RE.fullmatch(scene) for scene in unique_scenes]
            if all(scene_matches):
                scene_numbers = [
                    int(match.group(1)) for match in scene_matches if match
                ]
                if abs(scene_numbers[0] - scene_numbers[1]) != 1:
                    errors.append("纯转场只能跨编号相邻的两个场景")

        if any(bool(row.get("sound_crosses_segment")) for row in segment_rows):
            errors.append("对白、旁白、画外音、环境声和音效均不得跨段")

        trim_rows = [row for row in segment_rows if row.get("trim_to") is not None]
        if trim_rows:
            if shot_count != 1 or abs(duration - 4.0) > 1e-9:
                errors.append("后期裁短只适用于生成时长写 4s 的单镜独立段")
            for row in trim_rows:
                try:
                    trim_to = parse_positive_number(row["trim_to"], "建议裁后时长")
                except ValueError as exc:
                    errors.append(str(exc))
                    continue
                if trim_to >= 4:
                    errors.append("建议裁后时长必须小于 4s")
                if not str(row.get("edit_note", "")).strip():
                    errors.append("后期裁短必须在 edit_note 中写明保留动作范围")

        segment_result = SegmentResult(
            segment=segment,
            segment_type=segment_type,
            shots=[str(row.get("shot")) for row in segment_rows],
            duration_seconds=duration,
            errors=errors,
            warnings=warnings,
        )
        segment_results.append(segment_result)
        global_errors.extend(f"{segment}：{message}" for message in errors)
        global_warnings.extend(f"{segment}：{message}" for message in warnings)

    return ValidationReport(
        status="fail" if global_errors else "pass",
        segment_count=len(segment_results),
        shot_count=len(rows),
        errors=global_errors,
        warnings=global_warnings,
        segments=segment_results,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="校验 Toffee Family 生产段")
    parser.add_argument("--input", required=True, type=Path, help="镜头行 JSON 文件")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        report = validate_rows(load_rows(args.input))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps(asdict(report), ensure_ascii=False, sort_keys=True))
    return 1 if report.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
