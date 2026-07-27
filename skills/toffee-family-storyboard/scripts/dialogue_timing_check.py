#!/usr/bin/env python3
"""校验儿童剧普通中文对白的实际发声速度。"""

from __future__ import annotations

import argparse
import json
import math
import re
from dataclasses import asdict, dataclass

MIN_RATE = 2.0
MAX_RATE = 2.33
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
    target_duration_min: float
    target_duration_max: float
    status: str
    warnings: list[str]


def ceil_tenth(value: float) -> float:
    """向上取到 0.1 秒，避免舍入后突破最快语速。"""

    return math.ceil((value - 1e-12) * 10) / 10


def normalize_spoken_text(text: str) -> str:
    """移除说话者标签和默认不发声的括号舞台说明。"""

    without_speaker = SPEAKER_RE.sub("", text.strip(), count=1)
    return BRACKET_RE.sub("", without_speaker)


def analyze_timing(text: str, duration: float) -> TimingResult:
    """返回对白语速、目标时长区间和处理状态。"""

    if duration <= 0:
        raise ValueError("对白实际发声时长必须大于 0")

    spoken_text = normalize_spoken_text(text)
    units = len(CHINESE_RE.findall(spoken_text))
    if units == 0:
        raise ValueError("没有检测到可发音中文汉字")

    warnings: list[str] = []
    if ASCII_RE.search(spoken_text):
        warnings.append("检测到数字或拉丁字母；请先展开为实际中文读音")

    rate = units / duration
    if rate > MAX_RATE + 1e-9:
        status = "too_fast"
    elif rate < MIN_RATE - 1e-9:
        status = "slow_reason_required"
    else:
        status = "target"

    return TimingResult(
        text=text,
        spoken_text=spoken_text,
        spoken_units=units,
        duration_seconds=round(duration, 3),
        rate=round(rate, 3),
        target_duration_min=ceil_tenth(units / MAX_RATE),
        target_duration_max=ceil_tenth(units / MIN_RATE),
        status=status,
        warnings=warnings,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="按每秒 2.0–2.33 个可发音字校验儿童剧普通对白"
    )
    parser.add_argument("--text", required=True, help="对白正文，可包含说话者标签")
    parser.add_argument(
        "--duration",
        required=True,
        type=float,
        help="对白实际发声时长（秒），不含静默反应和镜头余量",
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
        result = analyze_timing(args.text, args.duration)
    except ValueError as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 2

    print(json.dumps(asdict(result), ensure_ascii=False, sort_keys=True))
    return 1 if result.status == "too_fast" else 0


if __name__ == "__main__":
    raise SystemExit(main())
