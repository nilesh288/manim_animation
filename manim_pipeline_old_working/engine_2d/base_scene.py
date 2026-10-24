"""
2d_engine/base_scene.py
Base Scene with strict beat-synchronization and editorial canvas.
"""
from manim import Scene
from .theme import PALETTE


class InfographicScene(Scene):
    target_duration = 0.0

    def setup(self):
        super().setup()
        self.camera.background_color = PALETTE["bg"]

    def beat(self, motion_time: float, hold_time: float, action=None, description=""):
        """
        Executes a synchronized beat:
        - action(): Performs the motion animations (strictly taking motion_time)
        - wait(): Holds still for hold_time so narration finishes
        """
        if action:
            action()
        elif motion_time > 0:
            self.wait(motion_time)
            
        if hold_time > 0:
            self.wait(hold_time)

    def finalize(self):
        """End of scene cleanup."""
        pass
