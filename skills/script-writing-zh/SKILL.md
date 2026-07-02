---
name: script-writing-zh
description: 中文剧本写作扩写工作流。Use when the user has a project archive/项目档案 and outline/大纲 and wants to write a complete script, continue scenes or episodes, choose standard screenplay vs novelized narrative format, switch rhythm styles, polish dialogue, expand or shorten scenes, rewrite specific scenes/episodes, or check beats/DNA alignment.
---

# 剧本写作

Use this skill downstream of `script-development-zh`: turn a locked project archive and outline into a complete Chinese script.

Read `references/full-spec.md` for the original full single-file spec, exact menus, long examples, and edge cases.

## Non-Negotiables

1. Require the project archive and outline before writing. Stop if hard fields are missing.
2. Give real feedback. Every substantive output must include at least one weakness or risk.
3. End every writing output with:

```text
【创作笔记】
- 核心情绪：____
- 取舍：____
- 自评不满意点：____
- 引用 DNA 规律（如已激活）：____
```

4. Do not invent characters, powers, places, factions, or background facts missing from the archive. Mark unknowns as `【待用户确认】`.
5. If a confirmed benchmark DNA report is present, cite at least one confirmed rule in every substantive output.
6. Stop and ask when the archive, outline, or user request conflicts.
7. Never claim studio, author, or production credentials.

## Required Inputs

Hard required:

- Project metadata: project name, work type, core logline.
- Character archive: at least two characters.
- Plot line or outline.

Soft required:

- Style/tone.
- Worldbuilding.
- Benchmark DNA report, if available.

If hard fields are missing, respond:

```text
检测到项目档案不完整（缺少：____）。
请补全后重新粘贴，或回到 script-development-zh 跑完七步流程。
```

If a separately pasted outline conflicts with the archive, ask whether to use the new outline as source of truth.

## Trigger Commands

Recognize these commands with or without `/`:

- `开始写作`
- `开始写作 模式=[标准|小说化] 节奏=[短剧|连续剧|短视频|单元剧|微电影|长篇电影] [分集=是|否]`
- `#标准 #短剧 +分集`
- `#小说化 #微电影`
- `继续写下一场`
- `继续写第 X 集`

Writing-time commands:

- `/模式 标准` or `/模式 小说化`
- `/节奏 短剧|连续剧|短视频|单元剧|微电影|长篇电影`
- `/分集 是` or `/分集 否`
- `/对白调优 第X场`
- `/扩写 第X场`
- `/减字 第X场 [目标字数]`
- `/节拍检查`
- `/对照 DNA`
- `/重写第X场`
- `/重写第X集`
- `批量模式`

## Modes

Mode is required:

- `M1 标准影视剧本`: scene heading, action lines, character names, dialogue, concise performance notes. Use when the script must be shootable or handoff-ready.
- `M2 小说化叙事剧本`: literary narrative paragraphs with embedded dialogue. Use for AI-video prompt pipelines, IP prose drafts, or mood-heavy scripts.

Episode switch is separate:

- `分集=否`: single work.
- `分集=是`: adds episode hook, episode body, episode-end hook, and continuity wrapper.

Default episode switch:

- Single films, micro-films, shorts, one-shot animation: `否`.
- Series, vertical drama, unit series, mini-series: `是`.

## Rhythm Styles

- `短剧`: 90 seconds-3 minutes per episode, high hook density.
- `连续剧`: 30-50 minute episodes, main/subplot interweaving.
- `短视频`: 15 seconds-3 minutes, first 3 seconds must retain attention.
- `单元剧`: independent episode plus shared world.
- `微电影`: 5-30 minutes, theme-led.
- `长篇电影`: 45-180 minutes, standard three-act structure.

## Workflow

1. Validate archive, outline, work type, DNA status, and episode/single-work status.
2. If the user says `开始写作`, show the mode menu, rhythm menu, and episode-switch default.
3. If the user gives a direct command, skip menus and parse mode/rhythm/switch.
4. Before writing, ask one final configuration check:

```text
即将开始写作。配置如下：

  模式：____
  节奏：____
  分集开关：____
  作品类型：____
  集数：____
  输出规模预估：约 ____ 字
  预计篇幅：____ 场
  DNA 状态：____

如有特殊要求请现在告诉我。没有的话回复“开始”，我即开始输出。
```

5. Write in manageable batches. For long work, pause after each batch unless the user enabled `批量模式`.
6. Keep continuity with already written scenes. If the user switches mode/rhythm midstream, warn about format fracture and ask whether to rewrite previous parts.

## Output Rules

For standard screenplay:

- Scene heading: scene number + day/night + interior/exterior + location.
- Action lines: third person, present tense, no long psychological explanation.
- Dialogue below character name.
- Use performance notes sparingly.
- Do not write director commentary.

For novelized narrative:

- Paragraphs of 3-6 sentences.
- Embed dialogue in quotes.
- Use sensory detail and controlled interiority.
- Keep direct psychological writing under about 30%.

For dialogue tuning, rewriting, expansion, or shortening, preserve plot continuity and explain what changed in the creative note.
