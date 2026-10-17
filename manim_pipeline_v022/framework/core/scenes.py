"""Manim CE v0.22.0 scene bases for 2D and 3D technical explainers."""

from manim import MovingCameraScene, ThreeDScene

from .timing import TimingContractMixin


class Technical2DScene(TimingContractMixin, MovingCameraScene):
    """2D scene base with a moving camera and strict beat timing."""

    def __init__(self, background_color="#07111F", **kwargs):
        super().__init__(**kwargs)
        self.camera.background_color = background_color
        self.initialize_timing_contract()

    def zoom_camera(
        self, factor, run_time=0.8, point=None, rate_func=None, added_anims=None
    ):
        """Animate a 2D camera-frame zoom, optionally with parallel animations."""
        animation = self.camera.frame.animate.scale(factor)
        if point is not None:
            animation = animation.move_to(point)
        play_kwargs = {"run_time": run_time}
        if rate_func is not None:
            play_kwargs["rate_func"] = rate_func
        self.play(animation, *(added_anims or []), **play_kwargs)


class Technical3DScene(TimingContractMixin, ThreeDScene):
    """3D scene base with explicit camera APIs and optional fixed overlays."""

    def __init__(self, background_color="#07111F", **kwargs):
        super().__init__(**kwargs)
        self.camera.background_color = background_color
        self.initialize_timing_contract()

    def add_hud(self, *mobjects):
        """Add labels/equations fixed to the screen while the 3D camera moves."""
        self.add_fixed_in_frame_mobjects(*mobjects)
        return mobjects

    def add_world_labels(self, *mobjects):
        """Keep 3D labels facing the camera while retaining world positions."""
        self.add_fixed_orientation_mobjects(*mobjects)
        return mobjects

    def move_camera_to(
        self,
        *,
        phi=None,
        theta=None,
        gamma=None,
        zoom=None,
        focal_distance=None,
        frame_center=None,
        run_time=0.8,
        rate_func=None,
        added_anims=None,
    ):
        """Move a ThreeDScene camera, optionally with parallel animations."""
        kwargs = {"run_time": run_time}
        if rate_func is not None:
            kwargs["rate_func"] = rate_func
        self.move_camera(
            phi=phi,
            theta=theta,
            gamma=gamma,
            zoom=zoom,
            focal_distance=focal_distance,
            frame_center=frame_center,
            added_anims=added_anims or [],
            **kwargs,
        )
