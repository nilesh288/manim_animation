from manim import *
from framework.core.scenes import Technical3DScene
from framework.systems_3d.primitives import world_label, hud_label


class Framework3DSmokeTest(Technical3DScene):
    def construct(self):
        self.target_duration = 3.0
        self.camera.background_color = "#07111F"
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES, zoom=1.0)

        sphere = Sphere(radius=1.0, resolution=(12, 24), color="#55C7E8")
        sphere.set_fill("#55C7E8", opacity=0.7)
        hud = hud_label(
            self,
            "3D SPATIAL VIEW",
            position=UP * 3.2 + LEFT * 4.7,
            color=WHITE,
            font_size=18,
        )
        label = world_label(
            self,
            "CORE",
            point=[1.05, 0.45, 0.2],
            direction=UP,
            color="#F7E36D",
            font_size=18,
        )

        def establish():
            self.play(FadeIn(sphere), run_time=0.9)

        self.beat(0.9, 0.3, establish, "establish 3D object")

        def camera_reveal():
            self.move_camera_to(
                phi=58 * DEGREES,
                theta=-20 * DEGREES,
                run_time=1.0,
            )

        self.beat(1.0, 0.3, camera_reveal, "3D camera reveal")
        self.beat(0.0, 0.5, None, "final readable hold")
        self.finalize()
