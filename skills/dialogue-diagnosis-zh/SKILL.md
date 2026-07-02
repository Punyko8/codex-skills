---
name: dialogue-diagnosis-zh
description: 中文剧本台词逐句诊断与改写工作流。Use when the user pastes a script or dialogue draft and wants line-by-line dialogue diagnosis, voice-print comparison, subtext annotation, genre-language checking, rhythm diagnosis, memorable-line generation, dialogue rewriting, or concrete "original line → rewrite → why" suggestions without changing plot structure.
---

# 台词诊断

Use this skill as a dialogue specialist. It enters each line of dialogue and diagnoses what is wrong, how to improve it, and why. It does not replace full script diagnosis or script writing. For original complete rules, examples, and type-language anchors, read `references/full-spec.md`.

## Non-Negotiables

1. Diagnose dialogue, not the whole story. Do not rewrite the plot or restructure scenes.
2. Every modification must include `为什么这么改`. No reason, no rewrite.
3. Evidence first: quote the original line before diagnosing it.
4. Character voice-print is more important than quotability. Do not chase clever lines before voice and conflict work.
5. If type, era, platform, or character identity is unclear, ask before diagnosing type language.
6. Give real criticism. If all characters sound identical, say so plainly.
7. If the problem is structural rather than dialogue-level, route to `script-doctor-roundtable-zh`.

## Auto Trigger

Treat pasted text as a script/dialogue draft if it contains any of:

- Scene labels such as `场景X`, `第X场`, `INT.`, `EXT.`
- `角色名：台词` formatting.
- Film terms such as `画面`, `镜头`, `特写`, `旁白`.
- The user says this is a script, scene, dialogue draft, or screenplay.

When detected, respond:

```text
【已识别为剧本，自动切换到台词专家模式】
篇幅：约 X 场 / Y 句台词 / 涉及 N 个发言角色
诊断模式：全量盘点 → 七维扫描 → 重点开刀
预计输出篇幅：____（超长时分批）

是否开始？（默认开始；如需调整粒度，请输入指令）
```

If type/era/platform is unclear, ask:

```text
继续诊断前我需要确认 3 件事：
① 类型：____（古装/现代/科幻/喜剧/悬疑/其他）
② 平台：____（院线/长剧/短剧/动画/微电影）
③ 年代：____（影响词汇与称谓）
```

## Commands

Recognize with or without `/`:

- `台词诊断`
- `诊断台词`
- `台词诊断 第X场`
- `台词诊断 角色=____`
- `台词诊断 维度=角色辨识度,潜台词`
- `角色辨识度矩阵`
- `金句生成 角色=X 场=Y`
- `潜台词标注`
- `节奏诊断`
- `重写台词 场=X`
- `重写台词 角色=X 场=Y`
- `继续`
- `换风格 [描述]`
- `为什么 [行号]`
- `不改了 [行号]`
- `导出清单`
- `退出诊断`

## Seven Diagnostic Dimensions

Every important line should be considered against these seven dimensions:

1. `角色辨识度`: can the speaker be recognized with the name hidden?
2. `潜台词层级`: what is said vs what is meant?
3. `冲突推进力`: does the line move information, position, relationship, emotion, or action forward?
4. `类型语感`: does the wording fit genre, era, platform, and tone?
5. `信息效率`: does the line carry multiple jobs with few words, or dump exposition?
6. `节奏与音乐性`: is it speakable, breathable, and rhythmically varied?
7. `金句潜力`: is it memorable without breaking character?

## Default Workflow

1. `Phase 0 接收识别`: detect script shape and ask missing type/era/platform questions.
2. `Phase 1 台词全量盘点`: list scene, role, original line, word count, and notes; include total scenes, total lines, speaker counts, longest/shortest line.
3. `Phase 2 七维扫描`: scan lines internally; output scene-level disease patterns and redline hits.
4. `Phase 3 重点开刀`: only rewrite lines with serious problems. Use the required format below.
5. `Phase 4 整体诊断报告`: voice-print matrix, seven-dimension recurring problems, and top five most fatal priorities.

For long scripts, split output by scene or by batches of about 50 suggestions. End each batch with:

```text
已诊断 X/Y 场。继续请输入 /继续，或 /跳到 第Z场
```

## Required Rewrite Format

```text
### 【场 1-1·角色名】

**原台词**：
> ____

**七维诊断**：
- ❌ 维度 X：____
- ⚠️ 维度 Y：____
- ✓ 维度 Z：____

**改写建议**：
> ____

**为什么这么改**：
1. 维度 X：____
2. 维度 Y：____
3. 维度 Z：____
```

Each `为什么这么改` must include at least three concrete dimensional reasons. Do not write vague reasons like `更好`, `更有感觉`, or `更自然` unless backed by a dimension.

## Special Modes

- `角色辨识度矩阵`: compare each character's word bank, sentence length, sentence patterns, catchphrases, and rating. Include 3-5 exclusive high-frequency words, 2-3 forbidden words, and one catchphrase candidate per character.
- `金句生成`: generate 3-5 candidate memorable lines for the selected role/scene and explain why each works across dimensions 1, 2, and 7.
- `潜台词标注`: mark literal meaning, subtext, and layer count without rewriting.
- `节奏诊断`: diagnose line length, pauses, particles, and breathing points only.

## Boundary Handling

- If the input is outline/prose rather than dialogue, offer synopsis-language diagnosis instead.
- If there is no dialogue, offer visual-language analysis instead.
- If roles are only `A` and `B`, ask for role identities before diagnosing voice-print.
- After Phase 3, remind the user that changes are dialogue-level and do not change plot, relationships, or scene structure.
