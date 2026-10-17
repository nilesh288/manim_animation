"""Explicit 3D camera wrapper; 3D scenes do not use MovingCameraScene.frame."""


def move_3d_camera(
    scene,
    *,
    phi=None,
    theta=None,
    gamma=None,
    zoom=None,
    focal_distance=None,
    frame_center=None,
    run_time=0.8,
    rate_func=None,
):
    """Animate a Manim CE ThreeDScene camera move."""
    kwargs = {"run_time": run_time}
    if rate_func is not None:
        kwargs["rate_func"] = rate_func
    scene.move_camera(
        phi=phi,
        theta=theta,
        gamma=gamma,
        zoom=zoom,
        focal_distance=focal_distance,
        frame_center=frame_center,
        **kwargs,
    )
