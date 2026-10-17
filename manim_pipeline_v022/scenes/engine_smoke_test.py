from manim import *
from engine_2d import InfographicScene, PALETTE, VectorArrow

class EngineSmokeTest(InfographicScene):
    target_duration = 2.0

    def construct(self):
        title = Text(
            "ENGINE TEST",
            color=PALETTE["text"],
            font_size=36,
        )
        arrow = VectorArrow(
            LEFT * 1.5,
            RIGHT * 1.5,
            color=PALETTE["coral"],
        )

        def show_scene():
            self.play(
                FadeIn(title),
                Create(arrow),
                run_time=1.0,
            )

        self.beat(1.0, 1.0, show_scene)
        self.finalize()
