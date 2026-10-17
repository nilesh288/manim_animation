from manim import *
from framework.core.scenes import Technical2DScene
from framework.systems_2d.primitives import DirectLeaderLabel, VectorArrow


class Framework2DSmokeTest(Technical2DScene):
    def construct(self):
        self.target_duration = 2.0
        self.camera.background_color = "#07111F"

        body = Circle(radius=0.8, color="#55C7E8", stroke_width=3)
        label = DirectLeaderLabel(
            "REFERENCE BODY",
            body,
            direction=UP,
            color=WHITE,
            line_color="#D5DEE7",
            font_size=18,
        )
        vector = VectorArrow(
            body.get_center(),
            body.get_center() + RIGHT * 1.5,
            color="#FFB454",
        )

        def reveal():
            self.play(Create(body), run_time=0.8)
            self.play(FadeIn(label), GrowArrow(vector), run_time=0.7)

        self.beat(1.5, 0.3, reveal, "2D primitive smoke test")
        self.beat(0.0, 0.2, None, "final hold")
        self.finalize()
