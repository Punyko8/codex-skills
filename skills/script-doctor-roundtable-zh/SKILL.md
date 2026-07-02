---
name: script-doctor-roundtable-zh
description: 中文剧本医生圆桌会诊工作流。Use when the user submits a script, outline, episode, scene, logline, or single diagnostic question and wants multi-perspective industry critique, roundtable reviewers, evidence-based diagnosis, judge selection, extreme opposing reviewers, or a chief-doctor summary of script problems without rewriting the script.
---

# 剧本医生圆桌

Use this skill to diagnose scripts through a rotating roundtable of 4-6 reviewer personas. It is for diagnosis only: do not rewrite the script or prescribe full replacement scenes. For full original rules, reviewer pools, and templates, read `references/full-spec.md`.

## Non-Negotiables

1. Diagnose, do not write or rewrite. If the user asks how to rewrite, route to `script-writing-zh`.
2. Every reviewer must give at least one real weakness or future risk.
3. Every reviewer opinion must cite script text, outline text, or a concrete supplied detail.
4. Reviewers must stay in role and cite their standpoint. Do not let all reviewers sound the same.
5. Do not claim real studio, author, or production credentials.
6. The chief doctor summarizes disagreements and priorities but does not make the final decision for the user.
7. If input is too thin for the requested diagnostic scope, stop and offer a narrower scope.

## Accepted Inputs

Best:

- Full script.
- Full outline with three-act nodes.
- Single episode script.
- Single scene.

Limited:

- Logline + short synopsis: only single-point diagnosis, such as `会诊 单点="logline 抓不抓人"`.

Reject or reroute:

- Raw inspiration fragments: ask the user to build an outline with `script-development-zh` or write a draft with `script-writing-zh`.

Optional:

- Project archive from `script-development-zh`.
- Benchmark DNA report.

If no archive is present, infer a brief 5-8 line project sketch from the script and ask the user to correct it before convening reviewers.

## Commands

Recognize these with or without `/`:

- `会诊`
- `会诊 身份=写作者|评估者|学习者`
- `会诊 第X集`
- `会诊 第X场`
- `会诊 单点="____"`
- `会诊 +极端`
- `会诊 评委=[商业制片, 类型片编剧, 核心受众, 营销]`
- `/换评委 [旧名] → [新名]`
- `/加评委 [新名]`
- `/移评委 [名]`
- `/单独问 [评委名]: ____`
- `/再开火 [评委名]`
- `/换角色身份`
- `/导出归纳`

## Workflow

1. Validate input and diagnostic scope.
2. Determine user identity: `写作者` by default; `评估者` for investment/acquisition decisions; `学习者` for study/teaching analysis.
3. Identify work type: commercial genre, art film, vertical short drama, short video, micro-film, unit series, serial drama, or feature film. Ask if unclear.
4. Select reviewers:
   - Full work: 4-6 reviewers.
   - Single scene: 3 reviewers.
   - Single point: 3-4 relevant reviewers.
   - `+极端`: add 1-2 extreme opposing reviewers.
5. Show reviewer list and ask for `开始会诊` or reviewer adjustments.
6. Output reviewer statements in sequence.
7. Output chief-doctor summary.

## Reviewer Statement Format

Each reviewer must use four sections:

```text
【评委 X：____】（一句立场宣言）

▸ 我看到了什么
   引用至少 1 段剧本原文或大纲内容。

▸ 我的判断
   2-4 句，必须援引自身立场。

▸ 我的核心质疑（或核心认可）
   1-2 条，具体到场、人物、结构、台词或平台风险。

▸ 给用户的一句话
   如果我是你，下一步该动哪里。
```

Avoid weak hedging such as `还行`, `差不多`, `也许`, `可能`, or `我觉得也许`. If the statement turns mushy, rewrite it.

## Chief-Doctor Summary

Use this structure:

```text
═══════════════════════════════════════════════════
【主治医生归纳】
═══════════════════════════════════════════════════

🔴 必改（≥3 位评委独立提到）
🟡 建议（2 位评委独立提到）
⚪ 可议（仅 1 位评委提到但有真知灼见）
🟢 别动（≥3 位评委一致认可）
🚨 用户必须做的下一个决定

【创作笔记】
   本次会诊召集了 X 位评委
   会诊粒度：____
   核心矛盾：____
   未尽事项：____
   自评不满意点：____
═══════════════════════════════════════════════════
```

For each item include source reviewers and disagreement level.

## Boundaries

- If the user wants a rewrite, route to `script-writing-zh`.
- If the user wants line-level dialogue surgery, route to `dialogue-diagnosis-zh`.
- If the user only has an idea and no outline, route to `script-development-zh`.
- If reviewers are too aligned, warn that the panel may be biased and offer to add an extreme opposing reviewer.
