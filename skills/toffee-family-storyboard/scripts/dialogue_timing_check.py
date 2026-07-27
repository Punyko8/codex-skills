#!/usr/bin/env python3
"""校验儿童剧普通中文对白的慢、中、快三档实际发声速度。"""

from __future__ import annotations

import argparse
import json
import math
import re
from dataclasses import asdict, dataclass

TIER_BOUNDS = {
    "慢": (2.0, 2.33),
    "中": (2.33, 2.8),
    "快": (2.8, 3.3),
}
TIER_ALIASES = {
    "slow": "慢",
    "medium": "中",
    "fast": "快",
    **{tier: tier for tier in TIER_BOUNDS},
}
MIN_RATE = 2.0
MAX_RATE = 3.3
CHINESE_RE = re.compile(r"[\u3400-\u4DBF\u4E00-\u9FFF]")
ASCII_RE = re.compile(r"[A-Za-z0-9]")
SPEAKER_RE = re.compile(r"^[^：:\n]{1,20}[：:]\s*")
BRACKET_RE = re.compile(r"（[^）]*）|\([^)]*\)|【[^】]*】|\[[^\]]*\]")


@dataclass(frozen=True)
class TimingResult:
    text: str
    spoken_text: str
    spoken_units: int
    duration_seconds: float
    rate: float
    selected_tier: str
    actual_tier: str | None
    target_duration_min: float
    target_duration_max: float
    status: str
    reason: str | None
    warnings: list[str]


def ceil_tenth(value: float) -> float:
    """向上取到 0.1 秒，避免舍入后突破最快语速。"""

    return math.ceil((value - 1e-12) * 10) / 10


def floor_tenth(value: float) -> float:
    """向下取到 0.1 秒，确保开放下界不会因舍入落入前一档。"""

    return math.floor((value - 1e-12) * 10) / 10


def normalize_spoken_text(text: str) -> str:
    """移除说话者标签和默认不发声的括号舞台说明。"""

    without_speaker = SPEAKER_RE.sub("", text.strip(), count=1)
    return BRACKET_RE.sub("", without_speaker)


def normalize_tier(tier: str) -> str:
    """把中英文档位名称统一为中文。"""

    try:
        return TIER_ALIASES[tier.lower() if tier.isascii() else tier]
    except KeyError as exc:
        raise ValueError("语速档位必须为慢、中、快或 slow、medium、fast") from exc


def classify_rate(rate: float) -> str | None:
    """按无重叠边界返回实际档位；区间外返回 None。"""

    if MIN_RATE - 1e-9 <= rate <= TIER_BOUNDS["慢"][1] + 1e-9:
        return "慢"
    if TIER_BOUNDS["中"][0] + 1e-9 < rate <= TIER_BOUNDS["中"][1] + 1e-9:
        return "中"
    if TIER_BOUNDS["快"][0] + 1e-9 < rate <= MAX_RATE + 1e-9:
        return "快"
    return None


def target_duration_range(units: int, tier: str) -> tuple[float, float]:
    """返回选定档位可安全填写的一位小数时长范围。"""

    minimum_rate, maximum_rate = TIER_BOUNDS[tier]
    minimum_duration = ceil_tenth(units / maximum_rate)
    if tier == "慢":
        maximum_duration = ceil_tenth(units / minimum_rate)
    else:
        maximum_duration = floor_tenth(units / minimum_rate)
    return minimum_duration, maximum_duration


def analyze_timing(
    text: str,
    duration: float,
    tier: str,
    reason: str | None = None,
) -> TimingResult:
    """返回对白语速、选定档位、目标时长区间和处理状态。"""

    if duration <= 0:
        raise ValueError("对白实际发声时长必须大于 0")
    selected_tier = normalize_tier(tier)

    spoken_text = normalize_spoken_text(text)
    units = len(CHINESE_RE.findall(spoken_text))
    if units == 0:
        raise ValueError("没有检测到可发音中文汉字")

    warnings: list[str] = []
    if ASCII_RE.search(spoken_text):
        warnings.append("检测到数字或拉丁字母；请先展开为实际中文读音")

    rate = units / duration
    actual_tier = classify_rate(rate)
    normalized_reason = reason.strip() if reason and reason.strip() else None
    if rate > MAX_RATE + 1e-9:
        status = "too_fast"
    elif rate < MIN_RATE - 1e-9:
        status = "slow_with_reason" if normalized_reason else "slow_reason_required"
    elif actual_tier != selected_tier:
        status = "tier_mismatch"
    else:
        status = "target"

    target_min, target_max = target_duration_range(units, selected_tier)
    return TimingResult(
        text=text,
        spoken_text=spoken_text,
        spoken_units=units,
        duration_seconds=round(duration, 3),
        rate=round(rate, 3),
        selected_tier=selected_tier,
        actual_tier=actual_tier,
        target_duration_min=target_min,
        target_duration_max=target_max,
        status=status,
        reason=normalized_reason,
        warnings=warnings,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="按慢、中、快三档校验儿童剧普通对白")
    parser.add_argument("--text", required=True, help="对白正文，可包含说话者标签")
    parser.add_argument(
        "--duration",
        required=True,
        type=float,
        help="对白实际发声时长（秒），不含静默反应和镜头余量",
    )
    parser.add_argument(
        "--tier",
        required=True,
        choices=tuple(TIER_ALIASES),
        help="必填语速档位：慢/中/快，亦可用 slow/medium/fast",
    )
    parser.add_argument(
        "--reason",
        help="语速低于每秒 2.0 字时必填的表演或低龄理解停顿原因",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="输出机器可读 JSON；默认也使用紧凑 JSON，保留此参数供调用方显式声明",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = analyze_timing(args.text, args.duration, args.tier, args.reason)
    except ValueError as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 2

    print(json.dumps(asdict(result), ensure_ascii=False, sort_keys=True))
    return (
        1
        if result.status in {"too_fast", "tier_mismatch", "slow_reason_required"}
        else 0
    )


if __name__ == "__main__":
    raise SystemExit(main())
