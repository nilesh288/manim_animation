# Premium Manim Technical-Documentary Pipeline

## Mission

Build a reusable production pipeline for premium technical and scientific documentaries using Manim Community Edition v0.22.0. It must support topic-adaptive 2D, 3D, and hybrid explanations. It is not a fixed-template slideshow generator.

The visual goal is explanatory clarity first, with cinematic composition, purposeful motion, readable technical graphics, spatial continuity, and restrained topic-appropriate art direction. Never promise photorealism or physically accurate simulation unless the implementation actually supports it.

## Source-of-truth policy

- Active development is isolated on the `manim_v22_premium_pipeline` branch, based on `manim_v22_v1`.
- `manim_pipeline/manim_V_1.0` is a reference for proven legacy behavior and components; do not modify it as part of this work.
- Preserve existing working narration-alignment/timing behavior unless a regression test proves a change is required.
- Do not introduce an Ollama dependency.
- Do not claim a stage is complete until its acceptance checks have passed.

## Production stages and contracts

### 0. Research and narration

The narration and any supplied research/source notes are the factual input. Technical claims must be supportable. Visual design may add explanatory labels, equations, or relationships when they are established by the supplied material or are standard and unambiguous, but it must not invent measurements or mechanisms.

### 1. Master Prompt 1 — Chief Visual Director

The Visual Director is the single owner of the final creative direction. It performs specialist reviews internally: subject-matter accuracy, narrative structure, 2D/3D visualization, cinematography/art direction, timing readiness, and schema correctness. These are review responsibilities, not independent competing storyboards.

The prompt must:
- preserve narration verbatim;
- organize original sentences into scenes, beats, and contiguous narration-anchor sub-beats;
- choose a topic-appropriate visual strategy scene by scene;
- make visible actions, spatial relationships, camera behavior, and transitions concrete;
- plan feasible Manim visuals without assuming unverified helper classes or renderer features;
- return one complete untimed JSON object only.

### 2. Parse and validate the untimed storyboard

A strict JSON parser must reject malformed or truncated JSON. Schema validation then checks required fields, types, arrays, IDs, allowed enums, and exact narration-anchor reconstruction. JSON syntax validity is not a substitute for visual or scientific review.

Reject invalid output or attempt a bounded, non-redesigning repair. A repair must preserve the existing visual decisions and narration; it must not quietly replace the storyboard with a simpler design.

### 3. Audio alignment and timing

Use the existing alignment/timing tools. They add timing fields to the approved storyboard; they do not redesign scenes or change narration anchors. Run the timing validator before compilation. Numeric timing belongs to this stage, not Master Prompt 1.

### 4. Master Prompt 2 — Manim Compiler

The compiler translates the timed storyboard into executable Manim code using verified framework capabilities. It must preserve the approved visual intent and timing contract.

It must not silently downgrade a requested 3D cutaway to a flat generic diagram merely because a helper is missing. If a required capability is unavailable, it must identify the capability gap or use a clearly equivalent feasible construction that preserves the explanation.

The compiler contract must explicitly distinguish 2D camera operations from 3D camera operations and only use APIs verified for Manim CE v0.22.0.

### 5. Code validation and bounded repair

Check Python syntax and imports, framework/API compatibility, scene class and ID, and timing conservation. On failure, provide the compiler/repair step with the precise error and relevant source. Limit retries, retain logs, and stop with a useful diagnostic rather than looping indefinitely.

Repairs must be local and preserve storyboard intent. A successful syntax check alone does not establish that the scene is visually correct.

### 6. Preview rendering

Render to temporary storage under `/dev/shm` to reduce microSD writes on the Raspberry Pi. Current target settings:
- Preview: 854x480 at 15 FPS.
- Final: 1920x1080 at 30 FPS.

Keep the temporary-storage behavior and validate rendered duration against the timed storyboard.

### 7. Rendered-video QA

Inspect actual frames or a contact sheet and, where practical, motion between frames. Check:
- clipping, overlap, unreadable labels, and low contrast;
- whether the intended subject and action are visible;
- whether the rendered sequence matches the approved composition and visual strategy;
- spatial continuity, camera behavior, and transition quality;
- scientific clarity and absence of misleading visual claims;
- duration, frame size, frame rate, and missing/blank frames.

A render can pass code checks and still fail visual QA. When the implementation is wrong, repair code while preserving the storyboard. Revisit the storyboard only when the approved visual plan itself is defective.

### 8. Final assembly

After scene-level QA passes, assemble scenes in order and combine narration, music, and sound effects as provided. Verify total duration, audio/video synchronization, and the final export settings.

## Acceptance test set

Use at least three different topic families before calling the general pipeline reliable:
1. Jet engine — machinery, internal anatomy, flow, and spatial/cinematic explanation.
2. GPS navigation — orbital/spatial systems, signals, and abstract information flow.
3. MRI scanner — technical equipment, magnetic-field concepts, and human-scale/internal explanation.

A pass requires more than valid JSON: it requires schema compliance, preserved narration, valid timing, successful render, and visual review against the approved storyboard.

## Current audit snapshot

At the time this document was added, the v0.22 branch contains a premium Visual Director prompt, a compiler prompt, a basic storyboard validator, audio alignment/timing scripts, a monolithic 2D engine, and example storyboards/renders. The branch does not yet contain a complete reusable 3D framework, integrated model-driven code-generation/repair orchestration, automated rendered-frame QA, or final documentary assembly orchestration. These are open implementation tasks, not completed capabilities.
