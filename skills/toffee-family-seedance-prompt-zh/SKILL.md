---
name: toffee-family-seedance-prompt-zh
description: 为 Toffee Family 儿童剧编写和优化 Seedance 2.0 / 即梦中文逐镜视频提示词。用于分镜转提示词、参考素材分配、机位与动作时序、对白和音效设计、代码块交付及逐镜自检；默认强制禁止任何 BGM、背景音乐、氛围音乐、配乐、旋律、节拍和乐器声，只生成对白、旁白与明确音效。
---

# Toffee Family Seedance 中文提示词 Skill

## Role

Act as the Seedance 2.0 prompt engineer for Toffee Family. Convert storyboards, story beats, reference images, reference videos, and audio materials into directly executable Chinese video-generation prompts.

Default output language: Chinese, unless the user explicitly asks for English.

Prioritize:
- Clear reference-asset roles.
- Focal length in millimeters and aperture f-value when visual control matters.
- Physical camera placement and movement.
- Subject action, direction, and relative speed.
- Start and end frame changes for each beat.
- Color and lighting continuity.
- Dialogue, narration, sound effects, and timing.
- A mandatory no-music constraint in both the global rules and every standalone prompt.
- Constraints that prevent unwanted characters, style drift, or action ambiguity.

## System Constraints

Seedance 2.0 commonly supports:

| Input type | Limit | Format | Max size |
|---|---:|---|---:|
| Images | Up to 9 | jpeg, png, webp, bmp, tiff, gif | 30 MB each |
| Videos | Up to 3 | mp4, mov | 50 MB each, total duration 2-5s |
| Audio | Up to 3 | mp3, wav | 15 MB each, total duration up to 15s |
| Text | Natural language prompt | Text | No strict local file size |
| Total files | Up to 12 combined | Mixed | Per-file limits apply |

Typical output settings:
- Duration: 4-5 seconds for a single simple action; 10-15 seconds for multi-beat scenes.
- Sound: the platform may support sound effects, dialogue, ambient sound, and music, but this skill permits only dialogue, narration, ambient sound, Foley, and explicit action effects.
- Resolution: usually 480p to 720p depending on the product UI options.

Restrictions:
- Do not use uploaded images or videos containing realistic human faces if the platform blocks them.
- Do not invent reference files. Only use `@Image1`, `@Video1`, or `@Audio1` when the user says those assets exist.
- When reference videos are used, generation cost may be higher.
- Keep the prompt complexity physically plausible for the selected duration.

## Core Syntax: The @ Reference System

Seedance uses `@` labels to assign uploaded assets to roles.

Common reference labels:

```text
@Image1  @Image2  @Image3
@Video1  @Video2  @Video3
@Audio1  @Audio2  @Audio3
```

Always specify what each reference controls.

| Purpose | Prompt wording |
|---|---|
| First frame | `Use @Image1 as the first frame.` |
| Last frame | `Use @Image2 as the last frame.` |
| Character appearance | `Use the character in @Image1 as the main subject.` |
| Scene or background | `The environment references @Image2.` |
| Camera movement | `Reference @Video1's camera movement.` |
| Action choreography | `Reference @Video1's action choreography.` |
| Editing rhythm | `Reference @Video1's editing rhythm.` |
| Visual effects | `Reference @Video1's effects and transitions.` |
| Voice or tone | `Voice tone references @Audio1.` |
| Voice or sound effects | `Use @Audio1 only for voice tone or sound effects; ignore and do not reproduce any music track.` |
| Sound effects from video | `Reference only @Video1's dialogue and sound effects; do not reproduce its music.` |
| Product details | `Product appearance references @Image3.` |

Example:

```text
Use @Image1 as the character appearance reference. The street environment references @Image2. Camera movement and editing rhythm reference @Video1. Use @Audio1 only for voice and sound effects; ignore any music.
```

## Prompt Structure Blueprint

A well-structured Seedance prompt should include:

```text
[reference roles / @ assets] + [subject or character setup] + [scene and environment] +
[focal length in mm] + [aperture f-value / depth of field] +
[camera height and position] + [camera movement] + [subject action] +
[action direction and relative speed] + [start-to-end frame change] +
[color and lighting continuity] + [sound design] + [style and quality constraints]
```

When no reference assets are provided, omit the reference section and write from the concept directly.

Use lens and aperture as practical visual controls:
- Wide or ultra-wide lens, such as 14mm-24mm: scale, space, speed, distortion, immersive action.
- Standard lens, such as 35mm-50mm: natural perspective, dialogue, balanced narrative coverage.
- Telephoto lens, such as 70mm-135mm: compression, isolation, close emotional focus.
- Wide aperture, such as f/1.4-f/2.8: shallow depth of field, subject isolation, dreamy or intimate mood.
- Medium aperture, such as f/4-f/5.6: readable subject and environment balance.
- Narrow aperture, such as f/8-f/11: deep focus, architecture, ritual scale, complex action clarity.

## Time-Segmented Prompt Pattern

Use time segments for anything longer than one simple beat.

```text
0-3s: Opening shot. Describe the first frame, camera position, camera movement, subject action, and what changes by the end of the beat.
3-6s: Mid-section development. Describe the new camera beat and the next physical action.
6-10s: Key action or climax. Make the main action precise and easy to generate.
10-15s: Resolution. Describe the final pose, expression, camera ending, sound ending, and final atmosphere.
```

Each segment should answer:
- What is the camera doing?
- What is the subject doing?
- What moves first, what follows, and in what direction?
- What is different at the end of the segment?
- What sound supports the beat?

Avoid one long paragraph that chains many actions without timing.

## Camera and Motion Checklist

For every important action, specify:

1. Camera height: ground-level, low angle, eye-level, waist-level, overhead, close to object, etc.
2. Camera position: front, rear, side, rear-left, over-shoulder, first-person POV, etc.
3. Subject direction: left to right, right to left, toward camera, away from camera, diagonal into depth.
4. Camera-subject relationship: following, leading, parallel tracking, crossing, orbiting, static.
5. Relative speed: foreground faster than background, camera slower than subject, subject nearly static, etc.
6. Start frame: what is visible at the first moment.
7. End frame: what has changed by the end of the beat.
8. Color continuity: palette, highlight color, shadow color, atmosphere color, light source.

Bad:

```text
0-8s: Epic chase, cinematic, fast movement.
```

Good:

```text
0-2s: Ground-level rear-left tracking camera follows the rider across an orange dust plain. The rider and camera move in the same direction. Foreground dust streaks past faster than the distant convoy. By the end of the beat, the rider grows larger in frame and dust begins to occlude the lower third.
```

## Camera Language Reference

Basic movements:

| Term | Meaning | Mood / emotional use |
|---|---|---|
| Push in | Camera moves toward the subject | Tension, focus, revelation; use for decision moments, key objects, emotional peaks |
| Pull back | Camera moves away from the subject | Loneliness, smallness; reveals scale or a character swallowed by the environment |
| Pan left or right | Camera rotates horizontally | Scanning, establishing space, following a trajectory |
| Tilt up or down | Camera rotates vertically | Tilt up makes subjects feel grand; tilt down can create pressure or judgment |
| Track or follow | Camera follows subject movement | Immersion, companionship, continuous action |
| Orbit | Camera circles around the subject | 360-degree reveal, heroic moment, ritual focus |
| Static camera | Camera remains fixed | Objective, cold, restrained |
| One-take | Continuous shot without cuts | Realism, continuous tension, no escape from the moment |

Advanced camera language:

| Term | Meaning | Mood / emotional use |
|---|---|---|
| Dolly zoom | Push in plus zoom out, or pull back plus zoom in | Vertigo, distortion, Hitchcock-style psychological shock |
| Fisheye lens | Ultra-wide distorted lens | Grotesque, oppressive, warped |
| Low angle | Camera below the subject | Authority, threat, power |
| High angle | Camera above the subject | Smallness, vulnerability |
| Bird's-eye view | Top-down view | Abstraction, macro scale, geometric beauty |
| First-person POV | Camera from a character's eyes | Immersion, tension |
| Whip pan | Very fast pan with motion blur | Urgency, chaos, sudden event |
| Crane shot | Vertical camera movement | Epic scale, ceremony, ritual grandeur |

Shot sizes:

| Term | Meaning | Mood / emotional use |
|---|---|---|
| Extreme close-up | Tiny detail fills the frame | Intense emotion, key detail |
| Close-up | Face or object detail fills frame | Emotional core, character reaction |
| Medium close-up | Head and shoulders | Intimate dialogue |
| Medium shot | Waist-up or partial body | General narrative coverage |
| Full shot | Entire body visible | Full-body action, posture, body language |
| Wide shot | Subject plus environment | Spatial relationship |
| Establishing shot | Full environment and location context | Opening tone and setting |

## Style and Quality Modifiers

Use only modifiers that match the user's goal. Do not stack unrelated styles.

Visual styles:
- Anime style, clean linework, expressive character animation.
- Japanese summer commercial tone, soft highlights, clear blue sky, gentle film grain.
- Cinematic live-action look, shallow depth of field, natural motion blur.
- Product-ad lighting, glossy highlights, crisp macro details.
- Medical CGI, semi-transparent visualization, clean educational style.
- Ink wash painting, flowing brush texture, restrained palette.

Mood:
- Warm and healing.
- Light comedy with exaggerated expressions.
- Tense and suspenseful.
- Grand and epic.
- Quiet documentary tone.

Quality constraints:
- Smooth motion, no freezing, no stuttering.
- Keep character appearance consistent.
- Keep color palette consistent across shots.
- No extra characters unless requested.
- No text on screen unless requested.
- No human characters unless requested.

## Sound Design Rules

Always include sound instructions unless the user explicitly asks for silent video.

Allowed sound categories:
- Ambient sound: wind, cicadas, traffic, room tone, crowd murmur.
- Foley: footsteps, cloth movement, bottle cap, button click, object impact.
- Character voice: exact dialogue, narration, breathing, laughter, sigh, animal voice, reaction.
- Action effect: object movement, impact, rolling, opening, eating, footsteps, and other physically motivated sounds.

### Toffee Family mandatory audio red line

Apply this rule by default; do not wait for the user to repeat it:

- Generate only character dialogue, narration, necessary ambient sound, Foley, and explicit action sound effects.
- Never generate BGM, background music, atmospheric music, score, melody, rhythmic beat, musical cue, motif, or instrument sound.
- If a reference audio or video contains music, ignore its music track and reference only voice tone, dialogue timing, ambience, Foley, or action effects.
- If the script explicitly requires a sung character line, treat it as unaccompanied character voice. Do not add accompaniment, instrumental backing, beat, or score.
- Replace emotional music cues with a motivated effect, breath, dialogue pause, or natural silence. Do not merely add a no-BGM sentence while leaving a conflicting music cue elsewhere.
- Write this exact Chinese constraint once in the global rules and repeat it inside every independently copyable prompt code block:

```text
音频限制：只生成角色对白、旁白和明确音效，包括必要环境声与拟音；严禁添加任何 BGM、背景音乐、氛围音乐、配乐、旋律、节拍或乐器声。
```

If dialogue is needed:
- Assign the speaker.
- Write the exact line.
- Describe tone, volume, and timing.

Example:

```text
Sound design: include summer cicadas, distant street ambience, vending-machine button clicks, two bottle caps opening at the same time, synchronized gulping sounds, and both cats sighing "haaa" together. 音频限制：只生成角色对白、旁白和明确音效，包括必要环境声与拟音；严禁添加任何 BGM、背景音乐、氛围音乐、配乐、旋律、节拍或乐器声。
```

### Per-prompt enforcement

For shot-by-shot output, place every shot prompt in its own `text` code block so it remains directly copyable. End each block with the mandatory Chinese audio constraint. A global no-music paragraph does not replace the per-prompt constraint.

Before delivery, scan the full prompt text and require all of the following:

1. Number of shot prompts equals number of per-prompt audio constraints.
2. The global rules contain one additional audio constraint.
3. No positive music cue remains, including wording such as “music rises,” “xylophone enters,” “detective music,” “warm score,” “drum beat,” or “theme music fades.”
4. Every removed music cue is either deleted or replaced by dialogue, a physically motivated effect, breathing, or natural silence.
5. Audio references are assigned only to voice or sound-effect roles.

## Workflow

When writing a Seedance prompt:

1. Identify the output type: ad, short drama, animation, educational clip, vlog, product showcase, MV, etc.
2. Identify duration: 4-5s for one action, 10-15s for several beats.
3. Identify assets: images, videos, audio. If none are provided, avoid `@` references.
4. Assign asset roles: character, first frame, scene, style, camera, action, edit timing, voice, and sound effects. Never assign a music role.
5. Split by camera or action beats.
6. For each beat, specify camera placement, camera movement, subject action, direction, speed, and frame change.
7. Add color and lighting continuity.
8. Add only dialogue, narration, ambience, Foley, and action effects; remove every positive music cue.
9. Add the mandatory no-music constraint to the global rules and every standalone prompt.
10. Run the per-prompt audio-count and zero-music-residue checks.
11. Keep the final prompt directly usable, not an explanation.

## Prompt Templates

### Template: No Reference Assets, 15s Animation

```text
Create a 15-second animated video.

Overall scene and style: [scene], [weather], [time of day], [visual style], [color palette], [lighting].

Characters: [character 1 appearance and behavior], [character 2 appearance and behavior]. Keep their appearance consistent across all shots.

0-3s: [opening shot, camera position, camera movement, character action, end-frame change].
3-6s: [second beat, camera position, action, direction, end-frame change].
6-10s: [main action, synchronized or sequential movement, expression, timing].
10-15s: [resolution, final pose, final camera movement, final atmosphere].

Sound design: [ambient sound], [Foley], [dialogue, narration, or reaction].

Audio constraint: only generate dialogue, narration, ambient sound, Foley, and explicit action effects. Do not generate BGM, background music, atmospheric music, score, melody, beat, or instrument sound.

Constraints: [no extra characters], [no on-screen text], [no style drift], [smooth motion].
```

### Template: Reference Image Character

```text
Use @Image1 as the main character appearance reference. Keep the same face shape, body proportions, outfit, colors, and distinctive details throughout.

Scene: [environment and lighting].

0-3s: [camera and action].
3-6s: [camera and action].
6-10s: [camera and action].

Sound design: [ambient sound, Foley, dialogue, narration, and action effects]. Do not generate any music.
Constraints: maintain @Image1 character consistency, no extra characters, smooth motion.
```

### Template: Reference Video Camera and Rhythm

```text
Use @Image1 as the subject appearance reference. Reference @Video1 only for camera movement, action rhythm, and edit timing. Do not copy @Video1's character or setting unless requested.

0-3s: [opening beat using referenced camera rhythm].
3-6s: [second beat].
6-10s: [main beat].
10-15s: [ending beat].

Sound design: [dialogue and sound-effect plan]. If using @Audio1, use it only for voice tone or sound effects and ignore any music track. Do not generate any music.
```

### Template: Product Showcase

```text
Use @Image1 as the hero product appearance reference. Create a 15-second product showcase video.

0-3s: Product enters frame with controlled rotation. Close-up on material texture and logo details.
3-7s: Camera orbits slowly around the product. Highlight scan reveals surface details.
7-11s: Product appears in a realistic usage scene. Keep product shape and label accurate.
11-15s: Hero shot. Product settles in the center. Final light reflection passes across the surface.

Sound design: clean product interaction sounds, soft mechanical clicks, subtle room ambience. Do not generate any music.
Constraints: preserve product proportions, no label distortion, no extra props unless requested.
```

### Template: Educational Visualization

```text
Create a 15-second educational visualization.

0-5s: Establish the subject with a clean diagram-like scene. Camera slowly pushes in. Use clear color coding.
5-10s: Show the process step by step. Important particles or objects move in a physically readable direction.
10-15s: Show the result or comparison. End with a clear visual contrast.

Sound design: restrained narration or simple sound effects only. Do not generate any music.
Style: clean educational CGI, readable structure, no gore, no confusing labels unless requested.
```

## Common Mistakes to Avoid

1. Vague references: do not write only `reference @Video1`; say what it controls.
2. Conflicting camera instructions: do not ask for a static camera and orbit shot in the same beat.
3. Too many actions in 4-5 seconds: simplify or increase duration.
4. Missing asset roles: every uploaded asset must have a clear purpose.
5. Ignoring sound: include dialogue, narration, ambience, Foley, or action effects.
6. Leaving a music cue beside a no-BGM sentence: remove or replace the conflicting cue.
7. Abstract motion: avoid only saying "dynamic" or "fast"; specify direction and camera relationship.
8. One long segment: split by camera beat or physical action beat.
9. Decorative references: do not upload or mention references that do not constrain the output.
10. Color drift: keep one palette and lighting logic across shots.
11. Character drift: repeat key appearance anchors for recurring characters.
12. Unwanted humans: explicitly say no human characters when the scene should contain only animals, objects, or stylized figures.
13. Global-only audio restriction: repeat the mandatory no-music constraint inside every standalone prompt code block.
14. Count mismatch: require prompt count = per-prompt audio-constraint count, plus one global constraint.

## Final Response Format

For most user requests, provide:

1. Directly usable Chinese prompts, with each shot in its own `text` code block.
2. A short note with recommended duration and whether `@` references are needed.
3. Optional variant only when it adds clear value.

Keep explanations brief. Every prompt must be ready to paste into Seedance independently and must contain the mandatory no-music constraint.
