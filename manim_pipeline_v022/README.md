# Manim Premium Technical-Documentary Pipeline (v0.22.0)

A reusable pipeline for premium 2D, 3D, and hybrid technical/scientific documentaries using Manim Community Edition v0.22.0.

## Project objective

Turn an approved technical narration into a scientifically clear, visually rich storyboard, then compile it into reliable Manim scenes, validate and render them, inspect actual output, and assemble a finished video. Visual strategies are selected per topic and scene; this is not a fixed-template slideshow generator.

## Read first

- [Pipeline architecture and acceptance criteria](docs/PIPELINE_ARCHITECTURE.md)
- [Premium Visual Director prompt](prompts/01_visual_director_premium.md)
- [Manim Compiler prompt](prompts/02_manim_compiler.md)

## Current components

- Premium untimed storyboard prompt with strict JSON contract.
- Storyboard structure and narration-anchor validator.
- Audio alignment and timing validator.
- Manim Community v0.22.0 2D engine and scene/render examples.
- Preview rendering to temporary storage under `/dev/shm` to reduce microSD writes.

## Important status

This branch is an in-progress implementation, not yet a complete automated production pipeline. In particular, a reusable 3D framework, end-to-end code-generation/repair orchestration, rendered-video visual QA, and final assembly orchestration still require implementation and testing. Do not treat prompt/schema validation or a successful render as proof of visual quality.

## Target settings

- Preview: 854x480, 15 FPS.
- Final: 1920x1080, 30 FPS.
- Runtime: Manim Community Edition v0.22.0.
- Target development environment: Raspberry Pi 5, 8 GB RAM.
- No Ollama dependency.

## Acceptance topics

Test the same pipeline on jet engine, GPS navigation, and MRI scanner storyboards. Each must pass JSON/schema validation, timing validation, code validation, rendering, and visual QA before the pipeline is considered reliable for general use.
