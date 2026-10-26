#!/usr/bin/env python3
"""
sanitize_scene.py
Automated AST & Syntax Pre-Flight Sanitizer for Manim Scene Code-Gen.
Eliminates common LLM syntax errors, decimal function names, and scope issues
without changing any visual styling, narration text, or animation durations.
"""
import ast
import re
import sys
from pathlib import Path


def sanitize_code_text(code: str) -> tuple[str, list[str]]:
    fixes = []

    # 1. Strip Markdown fences if accidentally included by code-gen
    if "```" in code:
        code = re.sub(r"^```(?:python)?\s*", "", code, flags=re.MULTILINE)
        code = re.sub(r"^```\s*$", "", code, flags=re.MULTILINE)
        fixes.append("Removed markdown code fences")

    # 2. Fix decimal beat function names: `def act_1.1():` -> `def act_1_1():`
    decimal_def_pattern = re.compile(r"def\s+([a-zA-Z_]+)_([0-9]+)\.([0-9]+)\s*\(")
    if decimal_def_pattern.search(code):
        code = decimal_def_pattern.sub(r"def \1_\2_\3(", code)
        fixes.append("Sanitized decimal function identifiers (e.g. act_1.1 -> act_1_1)")

    # 3. Fix action references: `action=act_1.1` -> `action=act_1_1`
    decimal_act_pattern = re.compile(r"action\s*=\s*([a-zA-Z_]+)_([0-9]+)\.([0-9]+)")
    if decimal_act_pattern.search(code):
        code = decimal_act_pattern.sub(r"action=\1_\2_\3", code)
        fixes.append("Sanitized decimal action arguments (e.g. action=act_1.1 -> action=act_1_1)")

    # 4. Fix accidental Unicode math variable typos in code identifiers (e.g. `Δx` in variable assignments)
    # Python 3 allows many unicode identifiers, but some rate_func references or typos might need normalization
    return code, fixes


def validate_syntax(code: str, filename: str = "<scene>") -> None:
    try:
        ast.parse(code, filename=filename)
    except SyntaxError as e:
        raise SyntaxError(
            f"Syntax error at line {e.lineno}, col {e.offset}: {e.msg}\n"
            f"  --> {e.text}"
        ) from e


def sanitize_file(file_path: Path) -> bool:
    if not file_path.is_file():
        print(f"❌ Error: Scene file not found: {file_path}")
        return False

    original = file_path.read_text(encoding="utf-8")
    sanitized, fixes = sanitize_code_text(original)

    try:
        validate_syntax(sanitized, str(file_path))
    except SyntaxError as err:
        print(f"❌ Syntax Validation Failed in {file_path.name}:\n{err}")
        return False

    if sanitized != original:
        file_path.write_text(sanitized, encoding="utf-8")
        print(f"✨ Auto-sanitized {file_path.name}:")
        for fix in fixes:
            print(f"   • {fix}")
    else:
        print(f"✅ Syntax check passed for {file_path.name}")

    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python sanitize_scene.py <path_to_scene.py>")
        sys.exit(1)

    scene_path = Path(sys.argv[1]).resolve()
    success = sanitize_file(scene_path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
