"""
sample_reactor.py - Editorial Infographic Scene: Induced Nuclear Fission
10-Second synchronized breakdown of Uranium-235 splitting inside a reactor.
"""
from manim import *
import numpy as np

# Editorial Pastel Palette
PALETTE = {
    "bg": "#F8F9FA",           # Warm off-white
    "stroke": "#2D3748",       # Deep charcoal
    "stroke_light": "#CBD5E0", # Subtle gray for leader paths
    "text": "#1A202C",         # Slate black
    "text_dim": "#718096",     # Muted caption gray
    "indigo": "#5A67D8",       # U-235 core / protons
    "blue": "#4299E1",         # Thermal neutron / trajectory
    "amber": "#ED8936",        # Released thermal energy (200 MeV)
    "coral": "#E53E3E",        # Unstable state / daughter nucleus 1
    "mint": "#38A169",         # Daughter nucleus 2 (Krypton)
}


class AtomicNucleus(VGroup):
    """Clean vector depiction of a heavy nucleus made of clustered nucleons."""
    def __init__(self, radius=0.45, primary_color=PALETTE["indigo"], sec_color=PALETTE["coral"], **kwargs):
        super().__init__(**kwargs)
        # Outer boundary ring
        boundary = Circle(radius=radius, color=primary_color, stroke_width=2.0, fill_color=primary_color, fill_opacity=0.15)
        self.add(boundary)

        # Clustered sub-nucleons (protons and neutrons)
        np.random.seed(42)
        for _ in range(14):
            r = np.random.uniform(0.05, radius * 0.72)
            theta = np.random.uniform(0, 2 * PI)
            pos = np.array([r * np.cos(theta), r * np.sin(theta), 0])
            col = primary_color if np.random.rand() > 0.45 else sec_color
            nucleon = Dot(pos, radius=0.065, color=col)
            self.add(nucleon)


class ReactorFissionScene(Scene):
    def construct(self):
        self.camera.background_color = PALETTE["bg"]

        # ---------------------------------------------------------
        # Spatial Setup: Reactor Fuel Lattice Field
        # ---------------------------------------------------------
        # 1. Subtle background grid representing the fuel channel / moderator
        lattice_ring1 = Circle(radius=3.2, color="#E2E8F0", stroke_width=1.2).set_z_index(-1)
        lattice_ring2 = Circle(radius=2.2, color="#EDF2F7", stroke_width=1.5).set_z_index(-1)

        # 2. Heavy Uranium-235 Target Nucleus
        core_pos = ORIGIN
        u235 = AtomicNucleus(radius=0.52, primary_color=PALETTE["indigo"], sec_color=PALETTE["coral"]).move_to(core_pos)

        # Leader callout for Uranium-235 (Angled line, no card)
        c_start = core_pos + UP * 0.4 + RIGHT * 0.3
        c_mid = c_start + UP * 0.8 + RIGHT * 0.8
        c_end = c_mid + RIGHT * 1.2
        c_path = VMobject(color=PALETTE["stroke_light"], stroke_width=1.4)
        c_path.set_points_as_corners([c_start, c_mid, c_end])
        
        u_label = Text("URANIUM-235", font="sans-serif", font_size=13, color=PALETTE["text"]).next_to(c_end, UP, buff=0.06, aligned_edge=LEFT)
        u_sub = Text("FISSILE TARGET // 92p + 143n", font="monospace", font_size=10, color=PALETTE["text_dim"]).next_to(c_end, DOWN, buff=0.06, aligned_edge=LEFT)
        u_callout = VGroup(c_path, u_label, u_sub)

        # 3. Incoming Thermal Neutron
        neutron_start = LEFT * 5.5 + UP * 0.1
        neutron = Dot(neutron_start, radius=0.08, color=PALETTE["blue"])
        n_track = DashedLine(neutron_start, core_pos + LEFT * 0.5, color=PALETTE["blue"], stroke_width=1.5, dash_length=0.15)
        n_label = Text("THERMAL NEUTRON (0.025 eV)", font="monospace", font_size=11, color=PALETTE["blue"]).next_to(neutron_start, UP, buff=0.15, aligned_edge=LEFT)

        # ---------------------------------------------------------
        # BEAT 1: Incoming Neutron & Stable Target (Duration: 3.20s)
        # Motion: 1.20s | Hold: 2.00s
        # ---------------------------------------------------------
        self.play(
            Create(lattice_ring1, run_time=1.0),
            Create(lattice_ring2, run_time=1.0),
            FadeIn(u235, scale=0.6, run_time=0.9),
            Write(u_callout, run_time=0.9),
            Create(n_track, run_time=1.0),
            FadeIn(neutron, run_time=0.6),
            Write(n_label, run_time=0.8),
        )
        self.wait(2.00)

        # ---------------------------------------------------------
        # BEAT 2: Impact & Critical Fission Split (Duration: 3.30s)
        # Motion: 1.20s | Hold: 2.10s
        # ---------------------------------------------------------
        # Daughter fragments
        frag_ba_pos = UP * 1.6 + RIGHT * 1.4
        frag_kr_pos = DOWN * 1.6 + LEFT * 1.2

        frag_ba = AtomicNucleus(radius=0.34, primary_color=PALETTE["coral"], sec_color=PALETTE["indigo"]).move_to(core_pos)
        frag_kr = AtomicNucleus(radius=0.28, primary_color=PALETTE["mint"], sec_color=PALETTE["indigo"]).move_to(core_pos)

        # Labels for fragments
        ba_label = Text("BARIUM-141", font="sans-serif", font_size=12, color=PALETTE["coral"]).next_to(frag_ba_pos, UP, buff=0.1)
        kr_label = Text("KRYPTON-92", font="sans-serif", font_size=12, color=PALETTE["mint"]).next_to(frag_kr_pos, DOWN, buff=0.1)

        # Radiant Energy Wavefront
        energy_burst = Circle(radius=0.2, arc_center=core_pos, color=PALETTE["amber"], stroke_width=2.5)
        energy_tag = Text("ΔE ≈ 200 MeV [HEAT]", font="monospace", font_size=14, color=PALETTE["amber"]).move_to(RIGHT * 2.2 + UP * 0.2)

        self.play(
            # Neutron enters the core
            neutron.animate(rate_func=rate_functions.ease_in_quad, run_time=0.4).move_to(core_pos),
            FadeOut(n_track, n_label, u_callout, run_time=0.3),
        )

        # Nucleus splits into two daughters while releasing radiant shockwave
        self.play(
            FadeOut(u235, neutron, run_time=0.2),
            energy_burst.animate(rate_func=rate_functions.ease_out_quad, run_time=1.0).scale(12.0).set_stroke(opacity=0),
            Write(energy_tag, run_time=0.8),
            frag_ba.animate(rate_func=rate_functions.ease_out_cubic, run_time=1.1).move_to(frag_ba_pos),
            frag_kr.animate(rate_func=rate_functions.ease_out_cubic, run_time=1.1).move_to(frag_kr_pos),
            Write(ba_label, run_time=0.8),
            Write(kr_label, run_time=0.8),
        )
        self.wait(2.10)

        # ---------------------------------------------------------
        # BEAT 3: 3 Secondary Neutrons Propagate (Duration: 3.50s)
        # Motion: 1.20s | Hold: 2.30s
        # ---------------------------------------------------------
        # Three newly emitted fast neutrons triggering the chain reaction
        angles = [PI * 0.15, -PI * 0.45, PI * 0.85]
        fast_neutrons = VGroup()
        arrows = VGroup()

        for ang in angles:
            end_pt = np.array([3.4 * np.cos(ang), 3.4 * np.sin(ang), 0])
            start_pt = np.array([0.4 * np.cos(ang), 0.4 * np.sin(ang), 0])
            
            dot = Dot(start_pt, radius=0.075, color=PALETTE["blue"])
            arr = Arrow(start_pt, end_pt, buff=0, stroke_width=2.0, max_tip_length_to_length_ratio=0.18, color=PALETTE["blue"])
            fast_neutrons.add(dot)
            arrows.add(arr)

        chain_callout = Text(
            "3 FAST NEUTRONS -> SUSTAINED CHAIN REACTION",
            font="monospace",
            font_size=12,
            color=PALETTE["blue"]
        ).to_edge(DOWN, buff=0.8)

        self.play(
            FadeIn(fast_neutrons, scale=0.5, run_time=0.4),
            Create(arrows, run_time=1.0),
            Write(chain_callout, run_time=0.8),
        )
        self.wait(2.30)
