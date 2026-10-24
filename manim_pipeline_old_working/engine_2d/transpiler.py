"""
engine_2d/transpiler.py
Deterministic compiler from Infographic JSON Blueprint to Manim Python.
"""
import json
import sys
import argparse
from pathlib import Path


def transpile_scene(bp: dict) -> str:
    scene_id = bp.get("scene_id", "scene_01")
    class_name = "".join(p.capitalize() for p in scene_id.split("_"))
    total_dur = bp.get("total_duration", 10.0)

    lines = []
    lines.append(f"class {class_name}(InfographicScene):")
    lines.append(f"    target_duration = {total_dur:.2f}\n")
    lines.append("    def construct(self):")

    # 1. Elements declaration
    lines.append("        # --- Elements ---")
    for el in bp.get("elements", []):
        eid = el["id"]
        etype = el["type"]
        pos = el.get("position", [0, 0, 0])
        props = el.get("props", {})
        col = props.get("color", "indigo")
        
        if etype == "Point":
            rad = props.get("radius", 0.08)
            lines.append(f"        {eid} = Dot(point=[{pos[0]}, {pos[1]}, {pos[2]}], radius={rad}, color=PALETTE['{col}'])")
        elif etype == "CircleBoundary":
            rad = props.get("radius", 2.0)
            sw = props.get("stroke_width", 2.0)
            lines.append(f"        {eid} = Circle(radius={rad}, arc_center=[{pos[0]}, {pos[1]}, {pos[2]}], color=PALETTE['{col}'], stroke_width={sw})")
        elif etype == "ArcBoundary":
            rad = props.get("radius", 5.0)
            sa = props.get("start_angle", 0.0)
            ang = props.get("angle", 1.57)
            sw = props.get("stroke_width", 2.0)
            lines.append(f"        {eid} = Arc(radius={rad}, start_angle={sa}, angle={ang}, arc_center=[{pos[0]}, {pos[1]}, {pos[2]}], color=PALETTE['{col}'], stroke_width={sw})")
        elif etype == "LeaderCallout":
            target = props.get("target_point", pos)
            title = props.get("title", "")
            sub = props.get("subtitle", None)
            d_str = props.get("direction", "UP+RIGHT")
            sub_arg = f', subtitle="{sub}"' if sub else ""
            lines.append(f'        {eid} = LeaderCallout([{target[0]}, {target[1]}, {target[2]}], "{title}"{sub_arg}, direction={d_str})')
        elif etype == "DimensionRuler":
            start = props["start"]
            end = props["end"]
            label = props.get("label", "")
            lines.append(f'        {eid} = DimensionRuler([{start[0]}, {start[1]}, {start[2]}], [{end[0]}, {end[1]}, {end[2]}], "{label}", color=PALETTE["{col}"])')
        elif etype == "VectorArrow":
            start = props["start"]
            end = props["end"]
            label = props.get("label", "")
            lines.append(f'        {eid} = VectorArrow([{start[0]}, {start[1]}, {start[2]}], [{end[0]}, {end[1]}, {end[2]}], label="{label}", color=PALETTE["{col}"])')

    lines.append("")
    lines.append("        # --- Beats Choreography ---")

    # 2. Beats
    for b in bp.get("beats", []):
        bid = b["beat_id"]
        m_time = b.get("motion_time", 1.2)
        h_time = b.get("hold_time", 1.8)
        sentence = b.get("sentence", "").replace('"', '\\"')[:80]
        
        lines.append(f"        def beat_{bid}():")
        anims = []
        for act in b.get("actions", []):
            verb = act["verb"]
            target = act.get("target")
            targets = act.get("targets", [target] if target else [])
            
            if verb == "CREATE":
                for t in targets:
                    anims.append(f"Create({t})")
            elif verb == "FADE_IN":
                for t in targets:
                    anims.append(f"FadeIn({t})")
            elif verb == "FADE_OUT":
                for t in targets:
                    anims.append(f"FadeOut({t})")
            elif verb == "WRITE":
                for t in targets:
                    anims.append(f"Write({t})")
            elif verb == "TRANSLATE":
                dest = act["to"]
                rate = act.get("rate_func", "ease_in_quad")
                anims.append(f"{target}.animate(rate_func=rate_functions.{rate}).move_to([{dest[0]}, {dest[1]}, {dest[2]}])")
            elif verb == "WAVE_BURST":
                center = act.get("center", [0, 0, 0])
                count = act.get("count", 3)
                radius = act.get("radius", 3.5)
                col = act.get("color", "indigo")
                anims.append(f"WaveEmitter.create_burst([{center[0]}, {center[1]}, {center[2]}], count={count}, max_radius={radius}, color=PALETTE['{col}'], run_time={m_time})")
            elif verb == "PULSE_RETICLE":
                center = act.get("center", [0, 0, 0])
                col = act.get("color", "coral")
                anims.append(f"PulseReticle.create_burst([{center[0]}, {center[1]}, {center[2]}], color=PALETTE['{col}'], run_time={m_time})")

        if anims:
            lines.append(f"            self.play({', '.join(anims)}, run_time={m_time})")
        else:
            lines.append(f"            self.wait({m_time})")

        lines.append(f'        self.beat(motion_time={m_time}, hold_time={h_time}, action=beat_{bid}, description="{sentence}")\n')

    lines.append("        self.finalize()\n")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Transpile Infographic Blueprint JSON to Manim code.")
    parser.add_argument("blueprint", help="Path to Blueprint JSON")
    parser.add_argument("-o", "--output", default="scenes/rendered_scene.py", help="Output .py file path")
    args = parser.parse_args()

    bp_path = Path(args.blueprint)
    if not bp_path.exists():
        print(f"Error: {bp_path} not found.")
        sys.exit(1)

    with open(bp_path, "r", encoding="utf-8") as f:
        bp_data = json.load(f)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    header = (
        "from manim import *\n"
        "from engine_2d import (\n"
        "    PALETTE,\n"
        "    FONTS,\n"
        "    InfographicScene,\n"
        "    LeaderCallout,\n"
        "    DimensionRuler,\n"
        "    VectorArrow,\n"
        "    WaveEmitter,\n"
        "    PulseReticle,\n"
        ")\n\n\n"
    )

    code = header + transpile_scene(bp_data)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(code)

    print(f"✅ Transpiled successfully -> {out_path}")


if __name__ == "__main__":
    main()
