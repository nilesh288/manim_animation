"""
engine_2d/objects.py
Apple macOS Pro Visual System & YouTube-Grade Technical Actors.
Eliminates generic boxes and gives concrete, physical, vibrant identity
to technical components: MacBook laptops, Wi-Fi 6 routers, 42U server racks,
aerodynamic bullet trains, electromagnetic eddy current brakes, orbital satellites,
and 3D Earth globes.
"""
import types
from manim import *
import numpy as np
from .theme import PALETTE, FONTS, FONT_SIZES
from .primitives import (
    MacOSPill,
    MacOSWindow,
    TechCard,
    VisualCard,
    MetricGauge,
    MilestoneTimeline,
    SleekArrow,
    DimensionRuler,
    LeaderCallout,
)

class InteractiveActor(VGroup):
    """
    Robust base class for all physical actors and technical components:
    - Filters arbitrary kwargs to protect Mobject.__init__ from unexpected keyword arguments
    - Provides surround_bounds(x_bounds, y_bounds) for fluid spatial bounding
    - Provides set_state(state, **kwargs) for semantic status transformations
    - Dynamic bound method dispatcher via types.MethodType for zero-crash .animate calls
    """
    def __init__(self, **kwargs):
        self._init_done = False
        mobj_kw = {
            k: v for k, v in kwargs.items()
            if k in ("color", "fill_color", "fill_opacity", "stroke_color", "stroke_width", "stroke_opacity", "name")
        }
        super().__init__(**mobj_kw)
        self._actor_state = "default"
        self._init_done = True

    def surround_bounds(self, x_bounds=None, y_bounds=None, **kwargs):
        """Aligns or positions the actor within explicit boundary limits."""
        if x_bounds and y_bounds:
            cx = (float(x_bounds[0]) + float(x_bounds[1])) / 2.0
            cy = (float(y_bounds[0]) + float(y_bounds[1])) / 2.0
            self.move_to([cx, cy, 0.0])
        return self

    def set_state(self, state=None, **kwargs):
        """Standard state setter for actors."""
        self._actor_state = str(state) if state is not None else "active"
        if "color" in kwargs:
            try:
                self.set_color(kwargs["color"])
            except Exception:
                pass
        return self

    def __getattr__(self, name):
        """
        Dynamically handles custom animation method calls (e.g. flicker_screen,
        charge_capacitors, stream_legacy_bits, etc.) returning a bound method
        so self.animate.<custom_method>(...) works cleanly without raising AttributeError.
        """
        if not getattr(self, "_init_done", False) or name.startswith("_"):
            raise AttributeError(name)

        def dynamic_method(self, *args, **kwargs):
            if "color" in kwargs:
                try:
                    self.set_color(kwargs["color"])
                except Exception:
                    pass
            elif "fill_color" in kwargs:
                try:
                    self.set_fill(kwargs["fill_color"])
                except Exception:
                    pass
            elif "stroke_color" in kwargs:
                try:
                    self.set_stroke(kwargs["stroke_color"])
                except Exception:
                    pass
            return self

        return types.MethodType(dynamic_method, self)


# =====================================================================
# 1. SMARTPHONE RECEIVER ACTOR
# =====================================================================
class PhoneDevice(InteractiveActor):
    """
    Iconic modern smartphone receiver.
    Features sleek bezel, glass screen, camera notch, home bar, and active radar/GPS beacon.
    """
    def __init__(
        self,
        scale: float = 1.0,
        status_color=None,
        show_radar: bool = True,
        bezel_color=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.accent = status_color or PALETTE["mint"]
        stroke_col = bezel_color or PALETTE["stroke_border"]

        # Outer chassis / bezel
        self.bezel = RoundedRectangle(
            corner_radius=0.16 * scale,
            width=0.90 * scale,
            height=1.75 * scale,
            color=stroke_col,
            stroke_width=2.5,
            fill_color=PALETTE["surface_card"],
            fill_opacity=1.0,
        )

        # Screen glass
        self.screen = RoundedRectangle(
            corner_radius=0.10 * scale,
            width=0.78 * scale,
            height=1.54 * scale,
            color=PALETTE["stroke_muted"],
            stroke_width=1.0,
            fill_color=PALETTE["surface_dark"],
            fill_opacity=1.0,
        )

        # Dynamic island / camera punch
        self.notch = RoundedRectangle(
            corner_radius=0.03 * scale,
            width=0.24 * scale,
            height=0.05 * scale,
            color=stroke_col,
            fill_color=PALETTE["surface_dark"],
            fill_opacity=1.0,
            stroke_width=0,
        ).move_to(self.screen.get_top() + DOWN * 0.08 * scale)

        # Bottom home gesture bar
        self.home_bar = Line(
            self.screen.get_bottom() + UP * 0.07 * scale + LEFT * 0.12 * scale,
            self.screen.get_bottom() + UP * 0.07 * scale + RIGHT * 0.12 * scale,
            color=PALETTE["stroke_light"],
            stroke_width=2.0,
        )

        self.add(self.bezel, self.screen, self.notch, self.home_bar)

        if show_radar:
            self.center_dot = Dot(self.screen.get_center(), radius=0.07 * scale, color=self.accent)
            self.pulse_ring = Circle(
                radius=0.20 * scale,
                color=self.accent,
                stroke_width=1.8,
            ).move_to(self.screen.get_center())
            self.add(self.pulse_ring, self.center_dot)

    @property
    def antenna_point(self):
        return self.screen.get_top()


# =====================================================================
# 2. MACBOOK / LAPTOP ACTOR
# =====================================================================
class MacBookDevice(InteractiveActor):
    """
    Sleek modern laptop actor.
    Features:
    - Aluminum unibody base with trackpad recess
    - Thin-bezel display housing an application/terminal window
    - Clean neutral title bar & address/status pill
    - Optional content area
    """
    def __init__(
        self,
        scale: float = 1.0,
        screen_content=None,
        url_text: str = "https://example.com",
        show_traffic_lights: bool = False,
        **kwargs
    ):
        super().__init__(**kwargs)
        stroke_col = PALETTE["stroke_border"]

        # 1. Laptop Base / Chassis
        base_w = 2.4 * scale
        base_h = 0.22 * scale
        self.base = RoundedRectangle(
            corner_radius=0.06 * scale,
            width=base_w,
            height=base_h,
            color=stroke_col,
            stroke_width=2.0,
            fill_color=PALETTE["surface_ground"],
            fill_opacity=1.0,
        )
        # Thumb recess notch
        notch = RoundedRectangle(
            corner_radius=0.03 * scale,
            width=0.45 * scale,
            height=0.06 * scale,
            color=PALETTE["surface_card"],
            fill_color=PALETTE["surface_card"],
            fill_opacity=1.0,
            stroke_width=0,
        ).align_to(self.base, UP)

        # 2. Display Lid / Bezel
        lid_w = 2.2 * scale
        lid_h = 1.45 * scale
        self.lid = RoundedRectangle(
            corner_radius=0.10 * scale,
            width=lid_w,
            height=lid_h,
            color=stroke_col,
            stroke_width=2.2,
            fill_color=PALETTE["surface_dark"],
            fill_opacity=1.0,
        ).next_to(self.base, UP, buff=0.01 * scale)

        # 3. Application Window Screen
        screen_w = 2.05 * scale
        screen_h = 1.30 * scale
        self.screen = RoundedRectangle(
            corner_radius=0.06 * scale,
            width=screen_w,
            height=screen_h,
            color=PALETTE["stroke_border"],
            stroke_width=1.2,
            fill_color=PALETTE["surface_card"],
            fill_opacity=1.0,
        ).move_to(self.lid.get_center())

        # Title Bar
        titlebar_h = 0.22 * scale
        self.titlebar = RoundedRectangle(
            corner_radius=0.06 * scale,
            width=screen_w,
            height=titlebar_h,
            color=PALETTE["stroke_border"],
            stroke_width=0,
            fill_color=PALETTE["surface_dark"],
            fill_opacity=1.0,
        ).align_to(self.screen, UP)

        submobs = [self.base, notch, self.lid, self.screen, self.titlebar]

        # Traffic light dots (optional)
        if show_traffic_lights:
            dot_r = 0.035 * scale
            dot_close = Dot(radius=dot_r, color=PALETTE["coral"])
            dot_min = Dot(radius=dot_r, color=PALETTE["gold"])
            dot_zoom = Dot(radius=dot_r, color=PALETTE["mint"])
            traffic_dots = VGroup(dot_close, dot_min, dot_zoom).arrange(RIGHT, buff=0.05 * scale)
            traffic_dots.align_to(self.titlebar, LEFT).shift(RIGHT * 0.10 * scale)
            traffic_dots.match_y(self.titlebar)
            submobs.append(traffic_dots)

        # URL / status address pill
        url_pill = RoundedRectangle(
            corner_radius=0.05 * scale,
            width=1.15 * scale,
            height=0.14 * scale,
            color=PALETTE["stroke_border"],
            stroke_width=1.0,
            fill_color=PALETTE["surface_card"],
            fill_opacity=1.0,
        ).move_to(self.titlebar.get_center())

        url_label = Text(
            url_text,
            font=FONTS["mono"],
            weight=BOLD,
            font_size=int(7 * scale),
            color=PALETTE["text_dim"],
        ).move_to(url_pill.get_center())

        submobs.extend([url_pill, url_label])
        self.add(*submobs)

        # Optional inner content mobject
        if screen_content is not None:
            screen_content.move_to(self.screen.get_center() + DOWN * 0.10 * scale)
            self.add(screen_content)

    @property
    def screen_center(self):
        return self.screen.get_center() + DOWN * 0.08

    @property
    def port_left(self):
        return self.base.get_left()

    @property
    def port_right(self):
        return self.base.get_right()


# =====================================================================
# 3. MODERN WI-FI 6 / ENTERPRISE ROUTER ACTOR
# =====================================================================
class ModernRouter(InteractiveActor):
    """
    High-fidelity modern Wi-Fi 6 / Enterprise Router.
    Features:
    - Sleek dark titanium/matte black chassis with beveled edges
    - Dual (or quad) angled external antennas with gold pivot hinges
    - Front status LED bar with Apple Mint & Cyan indicators (Power, Internet, 2.4G, 5G, LAN)
    - Rear Ethernet RJ45 port bays
    - Built-in Wi-Fi pulse wave generator
    """
    def __init__(
        self,
        scale: float = 1.0,
        num_antennas: int = 2,
        active_color=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        stroke_col = PALETTE["stroke_border"]
        self.accent = active_color or PALETTE["cyan"]

        # Main horizontal chassis
        chassis_w = 2.2 * scale
        chassis_h = 0.65 * scale
        self.chassis = RoundedRectangle(
            corner_radius=0.10 * scale,
            width=chassis_w,
            height=chassis_h,
            color=stroke_col,
            stroke_width=2.5,
            fill_color=PALETTE["surface_card"],
            fill_opacity=1.0,
        )

        # Front beveled vent slot
        self.vent = RoundedRectangle(
            corner_radius=0.04 * scale,
            width=chassis_w * 0.88,
            height=0.12 * scale,
            color=PALETTE["surface_dark"],
            fill_color=PALETTE["surface_dark"],
            fill_opacity=1.0,
            stroke_width=0,
        ).align_to(self.chassis, DOWN).shift(UP * 0.08 * scale)

        # LED status indicators (Power, Internet, Wi-Fi 2.4G, Wi-Fi 5G, LAN 1, LAN 2)
        leds = VGroup()
        led_colors = [PALETTE["mint"], self.accent, self.accent, self.accent, PALETTE["mint"], PALETTE["mint"]]
        for col in led_colors:
            leds.add(Dot(radius=0.035 * scale, color=col))
        leds.arrange(RIGHT, buff=0.10 * scale).move_to(self.vent.get_center())

        # Top label
        self.label = Text(
            "ROUTER / GATEWAY",
            font=FONTS["sans"],
            weight=BOLD,
            font_size=int(8 * scale),
            color=PALETTE["text_dim"],
        ).move_to(self.chassis.get_center() + UP * 0.12 * scale)

        # External Antennas
        self.antennas = VGroup()
        if num_antennas == 2:
            offsets = [-0.65 * scale, 0.65 * scale]
            angles = [15 * DEGREES, -15 * DEGREES]
        else:
            offsets = [-0.75 * scale, -0.25 * scale, 0.25 * scale, 0.75 * scale]
            angles = [25 * DEGREES, 10 * DEGREES, -10 * DEGREES, -25 * DEGREES]

        for off, ang in zip(offsets, angles):
            base_pt = self.chassis.get_top() + RIGHT * off
            # Pivot hinge
            pivot = Dot(base_pt, radius=0.05 * scale, color=PALETTE["gold"])
            # Antenna shaft
            shaft_len = 0.85 * scale
            end_pt = base_pt + np.array([-np.sin(ang) * shaft_len, np.cos(ang) * shaft_len, 0])
            shaft = Line(base_pt, end_pt, color=stroke_col, stroke_width=3.2 * scale)
            tip = Dot(end_pt, radius=0.04 * scale, color=self.accent)
            self.antennas.add(pivot, shaft, tip)

        self.add(self.chassis, self.vent, leds, self.label, self.antennas)

    @property
    def antenna_tip(self):
        return self.chassis.get_top() + UP * 0.80

    def create_wifi_wave(self, radius: float = 0.8, color=None):
        """Creates an authentic expanding concentric Wi-Fi radio arc."""
        col = color or self.accent
        return Arc(
            radius=radius,
            start_angle=PI / 4,
            angle=PI / 2,
            color=col,
            stroke_width=2.5,
        ).move_to(self.chassis.get_top() + UP * 0.25)


# =====================================================================
# 4. ENTERPRISE DATACENTER 42U SERVER RACK
# =====================================================================
class ServerRackActor(InteractiveActor):
    """
    Enterprise Datacenter 19-inch Rack Cabinet.
    Features:
    - Heavy gauge steel enclosure with rack rails
    - 3 modular server blade chassis with ventilation grilles
    - Dual SAS/SATA drive caddies and active blinking activity LEDs
    - High-visibility server label
    """
    def __init__(
        self,
        scale: float = 1.0,
        label: str = "SERVER",
        num_blades: int = 3,
        accent_color=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        stroke_col = PALETTE["stroke_border"]
        self.accent = accent_color or PALETTE["mint"]

        # Outer 42U Cabinet chassis
        rack_w = 1.8 * scale
        rack_h = 2.4 * scale
        self.cabinet = RoundedRectangle(
            corner_radius=0.12 * scale,
            width=rack_w,
            height=rack_h,
            color=stroke_col,
            stroke_width=2.8,
            fill_color=PALETTE["surface_dark"],
            fill_opacity=1.0,
        )

        # Vertical rack mounting rails
        rail_l = Line(self.cabinet.get_top() + LEFT * (rack_w * 0.42), self.cabinet.get_bottom() + LEFT * (rack_w * 0.42), color=PALETTE["stroke_muted"], stroke_width=1.5)
        rail_r = Line(self.cabinet.get_top() + RIGHT * (rack_w * 0.42), self.cabinet.get_bottom() + RIGHT * (rack_w * 0.42), color=PALETTE["stroke_muted"], stroke_width=1.5)

        # Server Blades
        self.blades = VGroup()
        blade_w = rack_w * 0.82
        blade_h = 0.44 * scale
        blade_spacing = 0.58 * scale
        start_y = (num_blades - 1) * blade_spacing / 2.0

        for i in range(num_blades):
            y_pos = start_y - i * blade_spacing
            blade_chassis = RoundedRectangle(
                corner_radius=0.06 * scale,
                width=blade_w,
                height=blade_h,
                color=stroke_col,
                stroke_width=1.8,
                fill_color=PALETTE["surface_card"],
                fill_opacity=1.0,
            ).move_to(self.cabinet.get_center() + UP * y_pos)

            # Drive bays / vents
            drive1 = RoundedRectangle(corner_radius=0.02 * scale, width=0.35 * scale, height=0.18 * scale, color=PALETTE["stroke_muted"], fill_color=PALETTE["surface_dark"], fill_opacity=1.0, stroke_width=1.0).align_to(blade_chassis, LEFT).shift(RIGHT * 0.12 * scale)
            drive2 = RoundedRectangle(corner_radius=0.02 * scale, width=0.35 * scale, height=0.18 * scale, color=PALETTE["stroke_muted"], fill_color=PALETTE["surface_dark"], fill_opacity=1.0, stroke_width=1.0).next_to(drive1, RIGHT, buff=0.06 * scale)

            # Blinking LED cluster
            led1 = Dot(radius=0.04 * scale, color=self.accent).align_to(blade_chassis, RIGHT).shift(LEFT * 0.15 * scale + UP * 0.06 * scale)
            led2 = Dot(radius=0.04 * scale, color=PALETTE["cyan"]).next_to(led1, LEFT, buff=0.08 * scale)

            self.blades.add(VGroup(blade_chassis, drive1, drive2, led1, led2))

        # Bottom label
        self.tag = Text(
            label,
            font=FONTS["sans"],
            weight=BOLD,
            font_size=int(11 * scale),
            color=PALETTE["text"],
        ).next_to(self.cabinet, DOWN, buff=0.18 * scale)

        self.add(self.cabinet, rail_l, rail_r, self.blades, self.tag)

    @property
    def input_port(self):
        return self.cabinet.get_left()

    @property
    def output_port(self):
        return self.cabinet.get_right()


# =====================================================================
# 5. HIGH-SPEED AERODYNAMIC BULLET TRAIN ACTOR
# =====================================================================
class HighSpeedTrain(InteractiveActor):
    """
    Sleek aerodynamic bullet train (Shinkansen / Eurostar profile).
    Features:
    - Aerodynamic streamlined nose cone with tinted cockpit windshield
    - Dual-tone livery: Pure White upper body, vibrant Apple Blue/Cyan speed stripe, dark titanium skirt
    - Row of passenger windows with warm illumination
    - Front LED headlight beam
    - Bogie wheel assemblies with rotating steel rims
    - Ground steel rails with cross sleepers
    - Integrated undercarriage eddy current brake shoes
    """
    def __init__(
        self,
        scale: float = 1.0,
        livery_color=None,
        speed_stripe_color=None,
        show_rails: bool = True,
        **kwargs
    ):
        super().__init__(**kwargs)
        stroke_col = PALETTE["stroke_border"]
        stripe_col = speed_stripe_color or PALETTE["blue"]
        body_col = livery_color or PALETTE["surface_card"]

        train_w = 4.2 * scale
        train_h = 1.25 * scale

        # 1. Main Train Body Contour (Aerodynamic nose at RIGHT)
        # Using polygon contour with rounded corners for bullet train profile
        body_pts = [
            [-train_w * 0.48, -train_h * 0.35, 0],   # Rear bottom
            [-train_w * 0.48, train_h * 0.35, 0],    # Rear roof
            [train_w * 0.15, train_h * 0.35, 0],     # Front roof start of nose slope
            [train_w * 0.42, train_h * 0.05, 0],     # Cockpit nose tip
            [train_w * 0.48, -train_h * 0.20, 0],    # Extreme front tip
            [train_w * 0.38, -train_h * 0.35, 0],    # Front skirt
        ]
        self.body = Polygon(
            *body_pts,
            color=stroke_col,
            stroke_width=2.8,
            fill_color=body_col,
            fill_opacity=1.0,
        )

        # 2. Vibrant Speed Stripe
        stripe_pts = [
            [-train_w * 0.48, -0.05 * scale, 0],
            [train_w * 0.25, -0.05 * scale, 0],
            [train_w * 0.44, -0.15 * scale, 0],
            [train_w * 0.42, -0.22 * scale, 0],
            [-train_w * 0.48, -0.22 * scale, 0],
        ]
        self.stripe = Polygon(
            *stripe_pts,
            color=stripe_col,
            stroke_width=0,
            fill_color=stripe_col,
            fill_opacity=1.0,
        )

        # 3. Aerodynamic Tinted Cockpit Windscreen
        cockpit_pts = [
            [train_w * 0.18, train_h * 0.30, 0],
            [train_w * 0.36, train_h * 0.08, 0],
            [train_w * 0.30, train_h * 0.08, 0],
            [train_w * 0.16, train_h * 0.22, 0],
        ]
        self.cockpit = Polygon(
            *cockpit_pts,
            color=PALETTE["surface_dark"],
            stroke_width=1.5,
            fill_color=PALETTE["surface_dark"],
            fill_opacity=1.0,
        )

        # 4. Passenger Windows (Row of sleek rounded squares)
        self.windows = VGroup()
        n_windows = 4
        win_w = 0.28 * scale
        win_h = 0.22 * scale
        for i in range(n_windows):
            x = -train_w * 0.38 + i * (win_w + 0.16 * scale)
            win = RoundedRectangle(
                corner_radius=0.04 * scale,
                width=win_w,
                height=win_h,
                color=PALETTE["stroke_border"],
                stroke_width=1.2,
                fill_color=PALETTE["surface_dark"],
                fill_opacity=1.0,
            ).move_to([x, train_h * 0.12, 0])
            self.windows.add(win)

        # 5. High-intensity LED Headlight
        self.headlight = Dot(
            point=[train_w * 0.46, -train_h * 0.16, 0],
            radius=0.07 * scale,
            color=PALETTE["gold"],
        )
        # Headlight illumination cone
        light_cone_pts = [
            [train_w * 0.46, -train_h * 0.16, 0],
            [train_w * 0.46 + 1.6 * scale, -train_h * 0.16 - 0.45 * scale, 0],
            [train_w * 0.46 + 1.6 * scale, -train_h * 0.16 + 0.45 * scale, 0],
        ]
        self.light_cone = Polygon(
            *light_cone_pts,
            color=PALETTE["gold"],
            stroke_width=0,
            fill_color=PALETTE["gold"],
            fill_opacity=0.18,
        )

        # 6. Undercarriage Bogies & Steel Wheels
        self.wheels = VGroup()
        wheel_r = 0.18 * scale
        wheel_centers = [
            -train_w * 0.35, -train_w * 0.20,  # Rear bogie wheels
            train_w * 0.10, train_w * 0.25,    # Front bogie wheels
        ]
        for wx in wheel_centers:
            whl = Circle(
                radius=wheel_r,
                color=stroke_col,
                stroke_width=2.4,
                fill_color=PALETTE["surface_dark"],
                fill_opacity=1.0,
            ).move_to([wx, -train_h * 0.42, 0])
            rim = Circle(radius=wheel_r * 0.65, color=PALETTE["stroke_light"], stroke_width=1.5).move_to(whl.get_center())
            hub = Dot(whl.get_center(), radius=0.04 * scale, color=PALETTE["gold"])
            self.wheels.add(VGroup(whl, rim, hub))

        # 7. Magnetic Brake Shoe (Between the wheel bogies)
        brake_shoe_w = 0.75 * scale
        brake_shoe_h = 0.12 * scale
        self.brake_shoe = RoundedRectangle(
            corner_radius=0.03 * scale,
            width=brake_shoe_w,
            height=brake_shoe_h,
            color=PALETTE["coral"],
            stroke_width=1.8,
            fill_color=PALETTE["coral"],
            fill_opacity=1.0,
        ).move_to([-0.05 * scale, -train_h * 0.38, 0])

        self.add(self.body, self.stripe, self.cockpit, self.windows, self.headlight, self.light_cone, self.wheels, self.brake_shoe)

        # 8. Steel Railway Track
        if show_rails:
            rail_y = -train_h * 0.42 - wheel_r
            self.rail_top = Line([-train_w * 0.65, rail_y, 0], [train_w * 0.75, rail_y, 0], color=PALETTE["stroke_light"], stroke_width=3.0)
            self.rail_bot = Line([-train_w * 0.65, rail_y - 0.08 * scale, 0], [train_w * 0.75, rail_y - 0.08 * scale, 0], color=stroke_col, stroke_width=2.5)
            # Sleepers / ties
            sleepers = VGroup()
            n_sleepers = 14
            step = (train_w * 1.35) / n_sleepers
            for i in range(n_sleepers):
                sx = -train_w * 0.62 + i * step
                sleepers.add(Line([sx, rail_y - 0.08 * scale, 0], [sx, rail_y - 0.16 * scale, 0], color=PALETTE["stroke_muted"], stroke_width=2.0))
            self.track = VGroup(self.rail_top, self.rail_bot, sleepers)
            self.add(self.track)

    @property
    def brake_point(self):
        return self.brake_shoe.get_center()


# =====================================================================
# 6. EDDY CURRENT MAGNETIC BRAKE ASSEMBLY ACTOR
# =====================================================================
class EddyBrakeAssembly(InteractiveActor):
    """
    Physical Electromagnetic Eddy Current Brake Assembly.
    Features:
    - Thick rotating copper/aluminum disc with radial spokes and axle hub
    - Powerful C-core electromagnet with North (Red) and South (Blue) pole shoes
    - Visible magnetic flux lines (B-field) bridging the air gap
    - Induced swirling Eddy Current loops (I_eddy) glowing within the conductor
    - Opposing Lorentz Drag Force vector (F_braking) pointing backwards
    - Radiating Joule heating thermal glow waves (Q = I^2 * R)
    """
    def __init__(
        self,
        scale: float = 1.0,
        disc_radius: float = 1.5,
        show_flux: bool = True,
        show_eddy: bool = True,
        **kwargs
    ):
        super().__init__(**kwargs)
        stroke_col = PALETTE["stroke_border"]
        r = disc_radius * scale

        # 1. Conductive Copper Rotor Disc
        self.disc = Circle(
            radius=r,
            color=stroke_col,
            stroke_width=3.2,
            fill_color="#D35400",  # Rich warm copper
            fill_opacity=0.92,
        )
        # Inner cooling slots / radial spokes
        self.spokes = VGroup()
        for i in range(6):
            ang = i * (PI / 3)
            p1 = [0.35 * r * np.cos(ang), 0.35 * r * np.sin(ang), 0]
            p2 = [0.82 * r * np.cos(ang), 0.82 * r * np.sin(ang), 0]
            self.spokes.add(Line(p1, p2, color="#E67E22", stroke_width=3.0))

        # Center Axle Hub
        self.hub = Circle(radius=0.28 * r, color=stroke_col, stroke_width=2.8, fill_color=PALETTE["surface_dark"], fill_opacity=1.0)
        self.hub_pin = Dot(radius=0.10 * r, color=PALETTE["gold"])

        self.rotor = VGroup(self.disc, self.spokes, self.hub, self.hub_pin)

        # 2. Electromagnet Assembly (Straddling the disc rim at UP + RIGHT)
        mag_w = 0.95 * scale
        mag_h = 0.70 * scale
        mag_pos = [0.65 * r, 0.70 * r, 0]

        # North Pole Shoe (Red)
        self.pole_north = RoundedRectangle(
            corner_radius=0.06 * scale,
            width=mag_w * 0.45,
            height=mag_h,
            color=PALETTE["coral"],
            stroke_width=2.2,
            fill_color=PALETTE["coral"],
            fill_opacity=1.0,
        ).move_to(mag_pos + LEFT * 0.28 * scale)

        self.label_n = Text("N", font=FONTS["sans"], weight=BOLD, font_size=int(14 * scale), color=PALETTE["white"]).move_to(self.pole_north.get_center())

        # South Pole Shoe (Blue)
        self.pole_south = RoundedRectangle(
            corner_radius=0.06 * scale,
            width=mag_w * 0.45,
            height=mag_h,
            color=PALETTE["blue"],
            stroke_width=2.2,
            fill_color=PALETTE["blue"],
            fill_opacity=1.0,
        ).move_to(mag_pos + RIGHT * 0.28 * scale)

        self.label_s = Text("S", font=FONTS["sans"], weight=BOLD, font_size=int(14 * scale), color=PALETTE["white"]).move_to(self.pole_south.get_center())

        # Magnetic C-Yoke Core connecting the poles
        yoke_pts = [
            self.pole_north.get_top() + LEFT * 0.05,
            self.pole_north.get_top() + UP * 0.25 * scale,
            self.pole_south.get_top() + UP * 0.25 * scale,
            self.pole_south.get_top() + RIGHT * 0.05,
        ]
        self.yoke = VMobject(color=stroke_col, stroke_width=4.0).set_points_as_corners(yoke_pts)

        self.magnet = VGroup(self.yoke, self.pole_north, self.label_n, self.pole_south, self.label_s)

        self.add(self.rotor, self.magnet)

        # 3. Magnetic Flux Lines (B-field bridging the gap)
        if show_flux:
            self.flux_lines = VGroup()
            gap_center = mag_pos
            for dy in [-0.20 * scale, 0.0, 0.20 * scale]:
                f_line = DashedLine(
                    self.pole_north.get_right() + UP * dy,
                    self.pole_south.get_left() + UP * dy,
                    dash_length=0.06 * scale,
                    color=PALETTE["cyan"],
                    stroke_width=2.4,
                )
                self.flux_lines.add(f_line)
            self.add(self.flux_lines)

        # 4. Swirling Induced Eddy Currents (I_eddy circular loops)
        if show_eddy:
            eddy_pos = [0.55 * r, 0.45 * r, 0]
            self.eddy_loop1 = Circle(radius=0.25 * scale, color=PALETTE["gold"], stroke_width=2.8).move_to(eddy_pos)
            self.eddy_loop2 = Circle(radius=0.15 * scale, color=PALETTE["gold"], stroke_width=2.2).move_to(eddy_pos)
            self.eddy_arrow = Arrow(
                start=eddy_pos + UP * 0.25 * scale + LEFT * 0.05,
                end=eddy_pos + UP * 0.25 * scale + RIGHT * 0.15,
                color=PALETTE["gold"],
                stroke_width=2.5,
                buff=0,
                max_tip_length_to_length_ratio=0.35,
            )
            self.eddy_tag = Text("I_eddy", font=FONTS["mono"], weight=BOLD, font_size=int(11 * scale), color=PALETTE["gold"]).next_to(self.eddy_loop1, DOWN, buff=0.14 * scale)
            self.eddy_group = VGroup(self.eddy_loop1, self.eddy_loop2, self.eddy_arrow, self.eddy_tag)
            self.add(self.eddy_group)

        # 5. Opposing Lorentz Braking Drag Force Arrow (Placed cleanly above magnet)
        drag_y = mag_pos[1] + 0.65 * scale
        drag_start = [mag_pos[0] + 0.40 * scale, drag_y, 0]
        drag_end = [mag_pos[0] - 0.90 * scale, drag_y, 0]
        self.drag_force = Arrow(
            start=drag_start,
            end=drag_end,
            color=PALETTE["coral"],
            stroke_width=3.8,
            buff=0,
        )
        self.drag_label = Text(
            "F_drag (Lenz)",
            font=FONTS["sans"],
            weight=BOLD,
            font_size=int(12 * scale),
            color=PALETTE["coral"],
        ).next_to(self.drag_force, UP, buff=0.12 * scale)

        self.add(self.drag_force, self.drag_label)

    @property
    def disc_center(self):
        return self.disc.get_center()


# =====================================================================
# 7. HIGH-FIDELITY AEROSPACE COMMUNICATIONS SATELLITE
# =====================================================================
class SatelliteActor(InteractiveActor):
    """
    High-fidelity orbital satellite actor.
    Features:
    - Gold-foil Mylar insulated hexagonal bus chassis
    - Dual multi-cell solar panel wings with photovoltaic cell gridlines
    - Parabolic dish antenna oriented towards Earth
    - Directional communication beam cone
    """
    def __init__(
        self,
        scale: float = 1.0,
        wing_color=None,
        dish_direction=DOWN,
        **kwargs
    ):
        super().__init__(**kwargs)
        col_wing = wing_color or PALETTE["blue"]
        stroke_col = PALETTE["stroke_border"]

        # Central payload chassis wrapped in gold foil
        self.body = RoundedRectangle(
            corner_radius=0.08 * scale,
            width=0.72 * scale,
            height=0.54 * scale,
            color=PALETTE["gold"],
            stroke_width=2.5,
            fill_color="#B7950B",  # Gold foil Mylar
            fill_opacity=0.95,
        )
        self.core = Dot(radius=0.10 * scale, color=PALETTE["white"]).move_to(self.body.get_center())

        # Solar wings with cell grid divisions
        def make_solar_wing(side=LEFT):
            wing = VGroup()
            base = Rectangle(
                width=1.05 * scale,
                height=0.48 * scale,
                color=stroke_col,
                stroke_width=2.0,
                fill_color=col_wing,
                fill_opacity=1.0,
            )
            # Grid cells
            div1 = Line(base.get_top() + LEFT * 0.35 * scale, base.get_bottom() + LEFT * 0.35 * scale, color=PALETTE["stroke_border"], stroke_width=1.2)
            div2 = Line(base.get_top() + RIGHT * 0.35 * scale, base.get_bottom() + RIGHT * 0.35 * scale, color=PALETTE["stroke_border"], stroke_width=1.2)
            hdiv = Line(base.get_left(), base.get_right(), color=PALETTE["stroke_border"], stroke_width=1.2)
            strut = Line(self.body.get_edge_center(side), base.get_edge_center(-side), color=stroke_col, stroke_width=3.2)
            wing.add(base, div1, div2, hdiv, strut)
            return wing

        self.w_left = make_solar_wing(LEFT).next_to(self.body, LEFT, buff=0.10 * scale)
        self.w_right = make_solar_wing(RIGHT).next_to(self.body, RIGHT, buff=0.10 * scale)

        # Parabolic Dish Antenna
        dish_buff = 0.06 * scale
        if np.array_equal(dish_direction, DOWN):
            self.dish = Arc(radius=0.25 * scale, start_angle=-PI / 2, angle=PI, color=PALETTE["cyan"], stroke_width=2.8).next_to(self.body, DOWN, buff=dish_buff)
            self.dish_horn = Line(self.dish.get_center(), self.dish.get_center() + DOWN * 0.18 * scale, color=PALETTE["gold"], stroke_width=2.2)
        else:
            self.dish = Arc(radius=0.25 * scale, start_angle=PI / 2, angle=PI, color=PALETTE["cyan"], stroke_width=2.8).next_to(self.body, UP, buff=dish_buff)
            self.dish_horn = Line(self.dish.get_center(), self.dish.get_center() + UP * 0.18 * scale, color=PALETTE["gold"], stroke_width=2.2)

        self.add(self.body, self.core, self.w_left, self.w_right, self.dish, self.dish_horn)

    @property
    def dish_center(self):
        return self.dish.get_center()


# =====================================================================
# 8. PLANET EARTH GLOBE (2D High-Detail)
# =====================================================================
class PlanetEarth(InteractiveActor):
    """
    High-detail vector Earth globe.
    Features deep ocean sphere, atmospheric glow corona, detailed continent outlines,
    and longitude/latitude gridlines.
    """
    def __init__(
        self,
        radius: float = 1.35,
        atmo_opacity: float = 0.45,
        **kwargs
    ):
        super().__init__(**kwargs)
        stroke_col = PALETTE["stroke_border"]

        # Deep Ocean Sphere
        self.ocean = Circle(
            radius=radius,
            color=stroke_col,
            stroke_width=2.8,
            fill_color="#1B4F72",  # Deep sapphire ocean
            fill_opacity=1.0,
        )

        # Vibrant emerald / jade continents
        c_color = PALETTE["mint"]
        c1 = Polygon(
            [-0.60 * radius, 0.35 * radius, 0],
            [-0.30 * radius, 0.65 * radius, 0],
            [0.10 * radius, 0.55 * radius, 0],
            [0.22 * radius, 0.25 * radius, 0],
            [-0.10 * radius, 0.00 * radius, 0],
            [-0.50 * radius, 0.10 * radius, 0],
            color=stroke_col,
            stroke_width=1.5,
            fill_color=c_color,
            fill_opacity=0.95,
        )
        c2 = Polygon(
            [-0.40 * radius, -0.15 * radius, 0],
            [0.05 * radius, -0.25 * radius, 0],
            [0.20 * radius, -0.75 * radius, 0],
            [-0.10 * radius, -0.85 * radius, 0],
            [-0.30 * radius, -0.55 * radius, 0],
            color=stroke_col,
            stroke_width=1.5,
            fill_color=c_color,
            fill_opacity=0.95,
        )
        c3 = Polygon(
            [0.40 * radius, 0.45 * radius, 0],
            [0.75 * radius, 0.35 * radius, 0],
            [0.85 * radius, -0.10 * radius, 0],
            [0.50 * radius, 0.00 * radius, 0],
            color=stroke_col,
            stroke_width=1.5,
            fill_color=c_color,
            fill_opacity=0.95,
        )

        # Latitude & Meridian curves
        meridian = Arc(
            radius=radius,
            start_angle=-PI / 2,
            angle=PI,
            color=PALETTE["cyan"],
            stroke_width=1.2,
        ).set_stroke(opacity=0.35).stretch(0.40, 0)

        equator = Line(
            self.ocean.get_left(),
            self.ocean.get_right(),
            color=PALETTE["cyan"],
            stroke_width=1.2,
        ).set_stroke(opacity=0.35)

        # Atmospheric Glowing Corona Rim
        self.atmo = Circle(
            radius=radius + 0.08,
            color=PALETTE["cyan"],
            stroke_width=3.6,
        ).set_stroke(opacity=atmo_opacity)

        self.add(self.ocean, c1, c2, c3, meridian, equator, self.atmo)


# =====================================================================
# 9. CRYPTOGRAPHIC PADLOCK ACTOR
# =====================================================================
class CryptographicPadlock(InteractiveActor):
    """
    Sleek macOS security padlock.
    Features hardened chrome shackle, brushed brass body with beveled corners,
    keyhole, and glowing TLS encryption shield ring.
    """
    def __init__(
        self,
        scale: float = 1.0,
        is_locked: bool = True,
        shield_color=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        stroke_col = PALETTE["stroke_border"]
        shield_col = shield_color or PALETTE["indigo"]

        body_w = 1.35 * scale
        body_h = 1.05 * scale

        # 1. Brass Padlock Body
        self.body = RoundedRectangle(
            corner_radius=0.16 * scale,
            width=body_w,
            height=body_h,
            color=stroke_col,
            stroke_width=2.5,
            fill_color=PALETTE["gold"],
            fill_opacity=1.0,
        )

        # 2. Hardened Chrome Shackle
        shackle_r = 0.38 * scale
        self.shackle = Arc(
            radius=shackle_r,
            start_angle=0,
            angle=PI,
            color=PALETTE["stroke_light"],
            stroke_width=5.5 * scale,
        ).next_to(self.body, UP, buff=0.02 if is_locked else 0.18 * scale)

        # Shackle straight legs
        leg_l = Line(self.shackle.get_left(), self.body.get_top() + LEFT * shackle_r, color=PALETTE["stroke_light"], stroke_width=5.5 * scale)
        leg_r = Line(self.shackle.get_right(), self.body.get_top() + RIGHT * shackle_r, color=PALETTE["stroke_light"], stroke_width=5.5 * scale)

        # 3. Keyhole Slot
        kh_dot = Dot(self.body.get_center() + UP * 0.06 * scale, radius=0.08 * scale, color=PALETTE["surface_dark"])
        kh_slot = Polygon(
            self.body.get_center() + LEFT * 0.04 * scale,
            self.body.get_center() + RIGHT * 0.04 * scale,
            self.body.get_center() + RIGHT * 0.06 * scale + DOWN * 0.16 * scale,
            self.body.get_center() + LEFT * 0.06 * scale + DOWN * 0.16 * scale,
            color=PALETTE["surface_dark"],
            stroke_width=0,
            fill_color=PALETTE["surface_dark"],
            fill_opacity=1.0,
        )

        # 4. Glowing Cryptographic Shield Halo
        self.shield_halo = RoundedRectangle(
            corner_radius=0.25 * scale,
            width=body_w + 0.35 * scale,
            height=body_h + 0.75 * scale,
            color=shield_col,
            stroke_width=2.2,
        ).move_to(self.body.get_center() + UP * 0.20 * scale).set_stroke(opacity=0.65)

        self.add(self.shield_halo, leg_l, leg_r, self.shackle, self.body, kh_dot, kh_slot)


# =====================================================================
# 10. MODULAR DATA PACKET ACTOR
# =====================================================================
class DataPacketActor(InteractiveActor):
    """
    Sleek macOS-styled data packet with solid jewel-tone header,
    crisp white metadata, and white payload compartment with high contrast.
    """
    def __init__(
        self,
        packet_num: int = 1,
        header_text: str = "PKT #1",
        payload_text: str = "GET /index.html",
        width: float = 2.4,
        height: float = 0.85,
        header_color=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        stroke_col = PALETTE["stroke_border"]
        col_hdr = header_color or PALETTE["blue"]

        # Outer Container
        self.card = RoundedRectangle(
            corner_radius=0.14,
            width=width,
            height=height,
            color=stroke_col,
            stroke_width=2.0,
            fill_color=PALETTE["surface_card_light"],
            fill_opacity=1.0,
        )

        # Header Block (Left section)
        hdr_w = width * 0.42
        self.hdr = RoundedRectangle(
            corner_radius=0.14,
            width=hdr_w,
            height=height,
            color=col_hdr,
            stroke_width=0,
            fill_color=col_hdr,
            fill_opacity=1.0,
        ).align_to(self.card, LEFT)

        # Header Text (Bold pure white)
        self.lbl_hdr = Text(
            header_text,
            font=FONTS["sans"],
            weight=BOLD,
            font_size=11,
            color=PALETTE["white"],
        ).move_to(self.hdr.get_center())

        # Payload Text (Charcoal)
        self.lbl_payload = Text(
            payload_text,
            font=FONTS["mono"],
            weight=BOLD,
            font_size=10,
            color=PALETTE["text_dark"],
        ).move_to(self.card.get_center() + RIGHT * (hdr_w * 0.35))

        self.add(self.card, self.hdr, self.lbl_hdr, self.lbl_payload)


# =====================================================================
# 11. TELECOM MAST & SILICON PROCESSOR ACTORS
# =====================================================================
class CellTowerActor(InteractiveActor):
    def __init__(self, height: float = 2.4, beacon_color=None, **kwargs):
        super().__init__(**kwargs)
        stroke_col = PALETTE["stroke_border"]
        beacon_col = beacon_color or PALETTE["coral"]

        w_base = height * 0.28
        p_bl = np.array([-w_base / 2, -height / 2, 0])
        p_br = np.array([w_base / 2, -height / 2, 0])
        p_top = np.array([0, height / 2, 0])

        leg_l = Line(p_bl, p_top, color=stroke_col, stroke_width=2.8)
        leg_r = Line(p_br, p_top, color=stroke_col, stroke_width=2.8)

        rungs = VGroup()
        n_tiers = 4
        for i in range(1, n_tiers):
            t = i / n_tiers
            p1 = p_bl * (1 - t) + p_top * t
            p2 = p_br * (1 - t) + p_top * t
            rungs.add(Line(p1, p2, color=stroke_col, stroke_width=1.8))
            t_prev = (i - 1) / n_tiers
            p1_prev = p_bl * (1 - t_prev) + p_top * t_prev
            rungs.add(Line(p1_prev, p2, color=PALETTE["stroke_light"], stroke_width=1.4))

        dish = Circle(radius=0.18, color=stroke_col, stroke_width=2.0, fill_color=PALETTE["surface_card"], fill_opacity=1.0).move_to([0.22, height * 0.18, 0])
        beacon = Dot(p_top + UP * 0.06, radius=0.08, color=beacon_col)
        self.add(leg_l, leg_r, rungs, dish, beacon)


class ChipSoC(InteractiveActor):
    def __init__(self, size: float = 1.6, core_color=None, **kwargs):
        super().__init__(**kwargs)
        stroke_col = PALETTE["stroke_border"]
        accent = core_color or PALETTE["mint"]

        self.package = RoundedRectangle(
            corner_radius=0.16,
            width=size,
            height=size,
            color=stroke_col,
            stroke_width=3.0,
            fill_color=PALETTE["surface_dark"],
            fill_opacity=1.0,
        )

        pins = VGroup()
        n_pins = 5
        pin_len = 0.16
        pin_step = (size * 0.70) / (n_pins - 1)
        offset = -(size * 0.70) / 2

        for i in range(n_pins):
            pos = offset + i * pin_step
            pins.add(Rectangle(width=0.06, height=pin_len, color=PALETTE["stroke_light"], fill_color=PALETTE["stroke_light"], fill_opacity=1.0).move_to([pos, size / 2 + pin_len / 2, 0]))
            pins.add(Rectangle(width=0.06, height=pin_len, color=PALETTE["stroke_light"], fill_color=PALETTE["stroke_light"], fill_opacity=1.0).move_to([pos, -size / 2 - pin_len / 2, 0]))
            pins.add(Rectangle(width=pin_len, height=0.06, color=PALETTE["stroke_light"], fill_color=PALETTE["stroke_light"], fill_opacity=1.0).move_to([-size / 2 - pin_len / 2, pos, 0]))
            pins.add(Rectangle(width=pin_len, height=0.06, color=PALETTE["stroke_light"], fill_color=PALETTE["stroke_light"], fill_opacity=1.0).move_to([size / 2 + pin_len / 2, pos, 0]))

        self.die = RoundedRectangle(
            corner_radius=0.08,
            width=size * 0.52,
            height=size * 0.52,
            color=accent,
            stroke_width=2.0,
            fill_color=PALETTE["surface_card"],
            fill_opacity=1.0,
        )
        self.die_core = Dot(radius=0.12, color=accent).move_to(self.die.get_center())
        self.core = self.die_core
        self.add(pins, self.package, self.die, self.die_core)


class LocationPin(InteractiveActor):
    def __init__(self, color=None, scale: float = 1.0, **kwargs):
        super().__init__(**kwargs)
        col = color or PALETTE["coral"]
        stroke_col = PALETTE["stroke_border"]

        head = Circle(radius=0.22 * scale, color=stroke_col, stroke_width=2.4, fill_color=col, fill_opacity=1.0).move_to(UP * 0.28 * scale)
        core = Dot(radius=0.08 * scale, color=PALETTE["white"]).move_to(head.get_center())
        tip = Polygon(
            [-0.18 * scale, 0.20 * scale, 0],
            [0.18 * scale, 0.20 * scale, 0],
            [0.0, 0.0, 0],
            color=stroke_col,
            stroke_width=2.4,
            fill_color=col,
            fill_opacity=1.0,
        )
        shadow = Ellipse(width=0.45 * scale, height=0.12 * scale, color=PALETTE["stroke_light"], stroke_width=0, fill_color=PALETTE["surface_dark"], fill_opacity=0.35).move_to(DOWN * 0.04 * scale)
        self.add(shadow, tip, head, core)


# =====================================================================
# 14. MOTHERBOARD PCB SECTION
# =====================================================================
class MotherboardSection(InteractiveActor):
    """
    Detailed computer motherboard section featuring:
    - Multilayer PCB substrate with copper trace conduits
    - ATX power delivery connector with +12V/+5V rail conduits
    - VRM power phase solid capacitors and chokes
    - Gold pin vias and status power-good LED
    """
    def __init__(self, width: float = 7.0, height: float = 3.8, scale: float = 1.0, **kwargs):
        super().__init__(**kwargs)
        w = width * scale
        h = height * scale

        # 1. Main PCB Substrate (Deep emerald solder mask)
        self.pcb = RoundedRectangle(
            corner_radius=0.18 * scale,
            width=w,
            height=h,
            color=PALETTE["stroke"],
            stroke_width=2.5,
            fill_color="#132B22",
            fill_opacity=1.0,
        )

        # 2. Metallic Copper Traces & Bus Conduits
        traces = VGroup()
        trace_coords = [
            [[-w / 2 + 0.3 * scale, -h / 2 + 0.8 * scale, 0], [-w / 2 + 1.8 * scale, -h / 2 + 0.8 * scale, 0], [0, 0, 0]],
            [[-w / 2 + 0.3 * scale, -h / 2 + 1.2 * scale, 0], [-w / 2 + 1.5 * scale, -h / 2 + 1.2 * scale, 0], [-0.5 * scale, 0.4 * scale, 0]],
            [[0.5 * scale, 0, 0], [w / 2 - 1.2 * scale, 0, 0], [w / 2 - 0.4 * scale, 0.6 * scale, 0]],
            [[0.5 * scale, -0.4 * scale, 0], [w / 2 - 1.4 * scale, -0.4 * scale, 0], [w / 2 - 0.4 * scale, -1.0 * scale, 0]],
        ]
        for pts in trace_coords:
            tr = VMobject(color="#C98B27", stroke_width=2.0 * scale)
            tr.set_points_as_corners([np.array(p) for p in pts])
            traces.add(tr)

        # 3. Gold Solder Vias (Dots along traces)
        vias = VGroup()
        for x_off in np.linspace(-w / 2 + 0.8 * scale, w / 2 - 0.8 * scale, 8):
            vias.add(Dot([x_off, -h / 2 + 0.5 * scale, 0], radius=0.035 * scale, color="#F59E0B"))
            vias.add(Dot([x_off, h / 2 - 0.5 * scale, 0], radius=0.035 * scale, color="#F59E0B"))

        # 4. ATX 24-Pin Power Socket Header
        pwr_socket = RoundedRectangle(
            corner_radius=0.05 * scale,
            width=1.4 * scale,
            height=0.45 * scale,
            color=PALETTE["stroke"],
            stroke_width=1.8,
            fill_color="#E2E8F0",
            fill_opacity=1.0,
        ).move_to([-w / 2 + 1.0 * scale, -h / 2 + 0.7 * scale, 0])

        pwr_pins = VGroup(*[
            Square(side_length=0.06 * scale, color="#C98B27", fill_color="#F59E0B", fill_opacity=1.0, stroke_width=0.5)
            .move_to(pwr_socket.get_left() + RIGHT * (0.12 * scale + col * 0.11 * scale) + (UP if row == 0 else DOWN) * 0.10 * scale)
            for col in range(12) for row in range(2)
        ])

        # 5. VRM Solid Capacitors & Inductors
        vrm_group = VGroup()
        for i in range(4):
            cap = Circle(radius=0.12 * scale, color=PALETTE["stroke"], fill_color="#94A3B8", fill_opacity=1.0, stroke_width=1.5).move_to([-1.8 * scale + i * 0.35 * scale, 1.2 * scale, 0])
            choke = RoundedRectangle(corner_radius=0.04 * scale, width=0.22 * scale, height=0.22 * scale, color=PALETTE["stroke"], fill_color="#334155", fill_opacity=1.0, stroke_width=1.2).move_to([-1.8 * scale + i * 0.35 * scale, 0.7 * scale, 0])
            vrm_group.add(cap, choke)

        # 6. Power-Good Status LED
        self.pwr_led = Circle(radius=0.07 * scale, color="#F59E0B", fill_color="#F59E0B", fill_opacity=1.0, stroke_width=1.2).move_to([w / 2 - 0.8 * scale, -h / 2 + 0.7 * scale, 0])

        self.add(self.pcb, traces, vias, pwr_socket, pwr_pins, vrm_group, self.pwr_led)


# =====================================================================
# 15. RAM MODULE ACTOR (DDR5 DIMM)
# =====================================================================
class RamModuleActor(InteractiveActor):
    """
    Detailed desktop/server DDR memory stick (DIMM) featuring:
    - PCB base substrate with bottom center key notch
    - Gold contact edge connector teeth along the bottom edge
    - 4 to 8 black BGA memory IC chips with laser markings
    - Metallic heat spreader shield with illuminated status lightbar
    """
    def __init__(self, scale: float = 1.0, capacity_label: str = "16 GB DDR5", **kwargs):
        super().__init__(**kwargs)
        stick_w = 3.6 * scale
        stick_h = 1.35 * scale

        # 1. PCB Substrate with Center Notch
        notch_w = 0.14 * scale
        notch_h = 0.18 * scale
        pcb_left = Polygon(
            [-stick_w / 2, -stick_h / 2, 0],
            [-notch_w / 2, -stick_h / 2, 0],
            [-notch_w / 2, -stick_h / 2 + notch_h, 0],
            [0, -stick_h / 2 + notch_h, 0],
            color=PALETTE["stroke"],
            stroke_width=0,
            fill_color="#15803D",
            fill_opacity=1.0,
        )
        self.pcb = RoundedRectangle(
            corner_radius=0.08 * scale,
            width=stick_w,
            height=stick_h,
            color=PALETTE["stroke"],
            stroke_width=2.2,
            fill_color="#1E293B",
            fill_opacity=1.0,
        )

        # 2. Gold Contact Edge Connector Fingers
        gold_rail_l = Rectangle(width=stick_w * 0.42, height=0.18 * scale, color="#D97706", fill_color="#F59E0B", fill_opacity=1.0, stroke_width=0.8).move_to(self.pcb.get_bottom() + LEFT * (stick_w * 0.24) + UP * (0.09 * scale))
        gold_rail_r = Rectangle(width=stick_w * 0.42, height=0.18 * scale, color="#D97706", fill_color="#F59E0B", fill_opacity=1.0, stroke_width=0.8).move_to(self.pcb.get_bottom() + RIGHT * (stick_w * 0.24) + UP * (0.09 * scale))

        # Fine teeth vertical cuts
        teeth = VGroup()
        for x in np.linspace(-stick_w * 0.44, -0.15 * scale, 14):
            teeth.add(Line([x, -stick_h / 2, 0], [x, -stick_h / 2 + 0.18 * scale, 0], color="#92400E", stroke_width=1.0))
        for x in np.linspace(0.15 * scale, stick_w * 0.44, 14):
            teeth.add(Line([x, -stick_h / 2, 0], [x, -stick_h / 2 + 0.18 * scale, 0], color="#92400E", stroke_width=1.0))

        # 3. Memory IC Packages (BGA DRAM Chips)
        self.chips = VGroup()
        n_chips = 4
        chip_w = 0.52 * scale
        chip_h = 0.52 * scale
        chip_spacing = 0.72 * scale
        for i in range(n_chips):
            cx = -(n_chips - 1) * chip_spacing / 2 + i * chip_spacing
            c_box = RoundedRectangle(
                corner_radius=0.04 * scale,
                width=chip_w,
                height=chip_h,
                color=PALETTE["stroke"],
                stroke_width=1.5,
                fill_color="#111827",
                fill_opacity=1.0,
            ).move_to(self.pcb.get_center() + RIGHT * cx + DOWN * (0.05 * scale))
            dot = Dot(c_box.get_corner(UL) + RIGHT * 0.08 * scale + DOWN * 0.08 * scale, radius=0.02 * scale, color="#4B5563")
            chip_txt = Text("DRAM", font=FONTS["mono"], font_size=int(7 * scale), color="#9CA3AF").move_to(c_box.get_center())
            self.chips.add(VGroup(c_box, dot, chip_txt))

        # 4. Top Heat Spreader / Lightbar
        self.heat_spreader = RoundedRectangle(
            corner_radius=0.06 * scale,
            width=stick_w * 0.98,
            height=0.28 * scale,
            color=PALETTE["stroke"],
            stroke_width=1.8,
            fill_color="#334155",
            fill_opacity=1.0,
        ).align_to(self.pcb, UP)

        self.label = Text(capacity_label, font=FONTS["sans"], weight=BOLD, font_size=int(11 * scale), color=PALETTE["white"]).move_to(self.heat_spreader.get_center())

        self.add(self.pcb, gold_rail_l, gold_rail_r, teeth, self.chips, self.heat_spreader, self.label)


# =====================================================================
# 16. NVME M.2 SSD STORAGE DRIVE
# =====================================================================
class NvmeSsdActor(InteractiveActor):
    """
    High-speed M.2 2280 NVMe SSD storage drive featuring:
    - M.2 PCB with M-key gold edge connector
    - High-performance controller ASIC chip
    - 3D NAND flash memory packages
    - Activity blink LED and mounting half-moon screw notch
    """
    def __init__(self, scale: float = 1.0, capacity_label: str = "1 TB NVMe SSD", **kwargs):
        super().__init__(**kwargs)
        ssd_w = 3.6 * scale
        ssd_h = 1.10 * scale

        # 1. PCB Strip
        self.pcb = RoundedRectangle(
            corner_radius=0.06 * scale,
            width=ssd_w,
            height=ssd_h,
            color=PALETTE["stroke"],
            stroke_width=2.0,
            fill_color="#0F172A",
            fill_opacity=1.0,
        )

        # 2. Golden M-Key Connector Fingers (Left end)
        mkey = Rectangle(width=0.30 * scale, height=ssd_h * 0.85, color="#D97706", fill_color="#F59E0B", fill_opacity=1.0, stroke_width=0.8).align_to(self.pcb, LEFT)
        mkey_notch = Rectangle(width=0.32 * scale, height=0.15 * scale, color="#0F172A", fill_color="#0F172A", fill_opacity=1.0, stroke_width=0).move_to(mkey.get_center() + DOWN * (0.12 * scale))

        # 3. High-Speed Controller ASIC
        self.controller = RoundedRectangle(
            corner_radius=0.04 * scale,
            width=0.58 * scale,
            height=0.58 * scale,
            color=PALETTE["stroke"],
            stroke_width=1.5,
            fill_color="#475569",
            fill_opacity=1.0,
        ).move_to(self.pcb.get_left() + RIGHT * (0.85 * scale))
        ctrl_lbl = Text("CTRL", font=FONTS["mono"], font_size=int(8 * scale), weight=BOLD, color=PALETTE["white"]).move_to(self.controller.get_center())
        ctrl_grp = VGroup(self.controller, ctrl_lbl)

        # 4. 3D NAND Flash Packages
        self.nand_chips = VGroup()
        for i in range(2):
            nx = self.pcb.get_left() + RIGHT * (1.75 * scale + i * 0.95 * scale)
            n_box = RoundedRectangle(
                corner_radius=0.04 * scale,
                width=0.80 * scale,
                height=0.68 * scale,
                color=PALETTE["stroke"],
                stroke_width=1.5,
                fill_color="#1E293B",
                fill_opacity=1.0,
            ).move_to([nx[0], self.pcb.get_y(), 0])
            n_lbl = Text("3D NAND", font=FONTS["mono"], font_size=int(8 * scale), color="#94A3B8").move_to(n_box.get_center())
            self.nand_chips.add(VGroup(n_box, n_lbl))

        # 5. Activity LED
        self.led = Circle(radius=0.045 * scale, color="#0284C7", fill_color="#0284C7", fill_opacity=1.0, stroke_width=0.8).move_to(self.pcb.get_left() + RIGHT * (0.42 * scale) + UP * (0.35 * scale))

        # 6. Capacity Label
        self.tag = Text(capacity_label, font=FONTS["sans"], weight=BOLD, font_size=int(10 * scale), color=PALETTE["text_secondary"]).next_to(self.pcb, DOWN, buff=0.14 * scale)

        self.add(self.pcb, mkey, mkey_notch, ctrl_grp, self.nand_chips, self.led, self.tag)


# =====================================================================
# 17. QUARTZ CRYSTAL OSCILLATOR (Hardware Clock)
# =====================================================================
class QuartzOscillator(InteractiveActor):
    """
    Metallic can quartz crystal oscillator that drives hardware timing:
    - Silver metal package with rounded bevel corners
    - Two metal through-hole solder leads
    - Laser etched frequency marking (e.g. 3.60 GHz)
    - Animated clock waveform pulse line
    """
    def __init__(self, frequency_label: str = "3.60 GHz", scale: float = 1.0, **kwargs):
        super().__init__(**kwargs)
        can_w = 1.8 * scale
        can_h = 0.85 * scale

        # Solder leads
        lead_l = Line([-can_w / 2 - 0.25 * scale, 0, 0], [-can_w / 2, 0, 0], color="#94A3B8", stroke_width=3.5 * scale)
        lead_r = Line([can_w / 2, 0, 0], [can_w / 2 + 0.25 * scale, 0, 0], color="#94A3B8", stroke_width=3.5 * scale)

        # Metallic Can
        self.can = RoundedRectangle(
            corner_radius=0.18 * scale,
            width=can_w,
            height=can_h,
            color=PALETTE["stroke"],
            stroke_width=2.4,
            fill_color="#CBD5E1",
            fill_opacity=1.0,
        )

        inner_bevel = RoundedRectangle(
            corner_radius=0.14 * scale,
            width=can_w * 0.90,
            height=can_h * 0.82,
            color="#94A3B8",
            stroke_width=1.0,
            fill_color="#E2E8F0",
            fill_opacity=1.0,
        )

        self.freq_txt = Text(frequency_label, font=FONTS["mono"], weight=BOLD, font_size=int(12 * scale), color=PALETTE["text"]).move_to(self.can.get_center() + UP * 0.08 * scale)
        sub_txt = Text("XTAL OSC", font=FONTS["mono"], font_size=int(8 * scale), color=PALETTE["text_dim"]).next_to(self.freq_txt, DOWN, buff=0.06 * scale)

        self.add(lead_l, lead_r, self.can, inner_bevel, self.freq_txt, sub_txt)


# =====================================================================
# 18. SPI FLASH ROM CHIP (Motherboard BIOS/UEFI)
# =====================================================================
class SpiFlashRom(InteractiveActor):
    """
    8-pin SOIC SPI Flash ROM chip where motherboard firmware resides:
    - Molded black epoxy package with Pin 1 orientation index dot
    - 8 metallic gull-wing solder leads
    - Laser printed firmware label: "SPI FLASH / BIOS-UEFI"
    """
    def __init__(self, scale: float = 1.0, label: str = "SPI FLASH ROM", sublabel: str = "BIOS / UEFI", variant: str = None, **kwargs):
        if variant == "vintage_dip_package":
            label = "BIOS ROM"
            sublabel = "DIP-8 / 16-BIT"
        elif variant == "wson_low_profile":
            label = "UEFI NVRAM"
            sublabel = "WSON-8 / 64-BIT"
        super().__init__(**kwargs)
        pkg_w = 2.2 * scale
        pkg_h = 1.4 * scale

        # 8 Metallic Solder Leads (4 on top, 4 on bottom)
        pins = VGroup()
        for i in range(4):
            px = -pkg_w * 0.35 + i * (pkg_w * 0.70 / 3)
            pins.add(Line([px, pkg_h / 2, 0], [px, pkg_h / 2 + 0.20 * scale, 0], color="#CBD5E0", stroke_width=3.2 * scale))
            pins.add(Line([px, -pkg_h / 2, 0], [px, -pkg_h / 2 - 0.20 * scale, 0], color="#CBD5E0", stroke_width=3.2 * scale))

        # Epoxy Package
        self.body = RoundedRectangle(
            corner_radius=0.12 * scale,
            width=pkg_w,
            height=pkg_h,
            color=PALETTE["stroke"],
            stroke_width=2.5,
            fill_color="#1E293B",
            fill_opacity=1.0,
        )

        # Pin 1 Index Dot
        dot = Dot(self.body.get_corner(UL) + RIGHT * 0.20 * scale + DOWN * 0.20 * scale, radius=0.06 * scale, color="#475569")

        self.title_mob = Text(label, font=FONTS["sans"], weight=BOLD, font_size=int(12 * scale), color=PALETTE["white"]).move_to(self.body.get_center() + UP * 0.18 * scale)
        self.sub_mob = Text(sublabel, font=FONTS["mono"], weight=BOLD, font_size=int(11 * scale), color=PALETTE["blue"]).next_to(self.title_mob, DOWN, buff=0.12 * scale)

        self.add(pins, self.body, dot, self.title_mob, self.sub_mob)


# =====================================================================
# 19. DIAGNOSTIC SPEAKER (Motherboard POST Beep Buzzer)
# =====================================================================
class DiagnosticSpeaker(InteractiveActor):
    """
    Motherboard diagnostic piezo speaker / buzzer:
    - Cylindrical black buzzer housing with central sound port
    - Emits acoustic pulse waves for POST error codes
    """
    def __init__(self, scale: float = 1.0, **kwargs):
        super().__init__(**kwargs)
        r = 0.55 * scale

        leads = VGroup(
            Line([-0.18 * scale, -r, 0], [-0.18 * scale, -r - 0.25 * scale, 0], color="#94A3B8", stroke_width=2.8 * scale),
            Line([0.18 * scale, -r, 0], [0.18 * scale, -r - 0.25 * scale, 0], color="#94A3B8", stroke_width=2.8 * scale),
        )

        self.housing = Circle(radius=r, color=PALETTE["stroke"], stroke_width=2.4, fill_color="#1E293B", fill_opacity=1.0)
        hole = Circle(radius=0.14 * scale, color=PALETTE["stroke"], stroke_width=1.5, fill_color="#0F172A", fill_opacity=1.0)
        plus = Text("+", font=FONTS["sans"], weight=BOLD, font_size=int(13 * scale), color="#94A3B8").move_to(self.housing.get_center() + UP * 0.28 * scale)

        self.add(leads, self.housing, hole, plus)

    def create_sound_wave(self, color=None):
        col = color or PALETTE["coral"]
        wave = Circle(radius=0.7, color=col, stroke_width=2.4).move_to(self.housing.get_center())
        return wave, wave.animate.scale(2.2).set_opacity(0.0)



# =====================================================================
# 20. ATX 24-PIN POWER CONNECTOR
# =====================================================================
class ATX24PinConnector(InteractiveActor):
    """
    Standard ATX 24-Pin main power connector:
    - High-contrast polymer housing with center latch
    - 2x12 gold contact pin grid
    - Color-coded power rails (3.3V orange, 5V red, 12V yellow, GND black)
    """
    def __init__(self, scale: float = 1.0, **kwargs):
        super().__init__(**kwargs)
        cw = 2.8 * scale
        ch = 1.2 * scale

        self.housing = RoundedRectangle(
            corner_radius=0.08 * scale,
            width=cw,
            height=ch,
            fill_color="#F8FAFC",
            fill_opacity=1.0,
            color=PALETTE["stroke"],
            stroke_width=2.0,
        )

        self.latch = RoundedRectangle(
            corner_radius=0.04 * scale,
            width=0.45 * scale,
            height=0.18 * scale,
            fill_color="#CBD5E1",
            fill_opacity=1.0,
            color=PALETTE["stroke"],
            stroke_width=1.5,
        ).next_to(self.housing, UP, buff=0.0)

        self.pins = VGroup()
        pin_cols = 12
        pin_rows = 2
        pw = cw * 0.85 / (pin_cols - 1)
        for r in range(pin_rows):
            py = (ch * 0.22) if r == 0 else (-ch * 0.22)
            for c in range(pin_cols):
                px = -cw * 0.425 + c * pw
                pin_bg = Square(
                    side_length=0.09 * scale,
                    fill_color="#F59E0B",
                    fill_opacity=1.0,
                    stroke_color="#B45309",
                    stroke_width=0.8,
                ).move_to(self.housing.get_center() + np.array([px, py, 0.0]))
                self.pins.add(pin_bg)

        self.wires = VGroup()
        wire_colors = ["#F97316", "#EF4444", "#EAB308", "#1E293B"]
        for c in range(pin_cols):
            px = -cw * 0.425 + c * pw
            w_col = wire_colors[c % len(wire_colors)]
            w_line = Line(
                self.housing.get_bottom() + np.array([px, 0.0, 0.0]),
                self.housing.get_bottom() + np.array([px, -0.35 * scale, 0.0]),
                color=w_col,
                stroke_width=2.5 * scale,
            )
            self.wires.add(w_line)

        self.label = Text(
            "ATX 24-PIN POWER",
            font=FONTS["mono"],
            weight="BOLD",
            font_size=int(9 * scale),
            color=PALETTE["text"],
        ).move_to(self.housing.get_center())

        self.add(self.wires, self.housing, self.latch, self.pins, self.label)
        self._init_done = True


# =====================================================================
# 21. CAPACITOR BANK (VRM Power Filters)
# =====================================================================
class CapacitorBank(InteractiveActor):
    """
    Bank of solid VRM electrolytic capacitors:
    - 3 cylindrical metallic cans in a clean cluster
    - Stamped aluminum tops with etched cross-vent score lines
    - Negative polarity marking band & micro ratings
    """
    def __init__(self, count: int = 3, scale: float = 1.0, **kwargs):
        super().__init__(**kwargs)
        self.capacitors = VGroup()
        cw = 0.65 * scale
        ch = 1.25 * scale
        spacing = 0.82 * scale

        for i in range(count):
            cap_grp = VGroup()
            offset_x = (i - (count - 1) / 2.0) * spacing

            can = RoundedRectangle(
                corner_radius=0.08 * scale,
                width=cw,
                height=ch,
                fill_color="#1E293B",
                fill_opacity=1.0,
                stroke_color=PALETTE["stroke"],
                stroke_width=1.8,
            )

            stripe = Rectangle(
                width=cw * 0.22,
                height=ch,
                fill_color="#94A3B8",
                fill_opacity=1.0,
                stroke_width=0,
            ).align_to(can, LEFT)

            top_cap = Ellipse(
                width=cw * 0.92,
                height=0.28 * scale,
                fill_color="#CBD5E1",
                fill_opacity=1.0,
                stroke_color="#64748B",
                stroke_width=1.0,
            ).align_to(can, UP)

            x_vent = VGroup(
                Line(top_cap.get_center() + np.array([-0.12 * scale, -0.06 * scale, 0]), top_cap.get_center() + np.array([0.12 * scale, 0.06 * scale, 0]), color="#64748B", stroke_width=1.2),
                Line(top_cap.get_center() + np.array([-0.12 * scale, 0.06 * scale, 0]), top_cap.get_center() + np.array([0.12 * scale, -0.06 * scale, 0]), color="#64748B", stroke_width=1.2),
            )

            legs = VGroup(
                Line(can.get_bottom() + LEFT * 0.12 * scale, can.get_bottom() + LEFT * 0.12 * scale + DOWN * 0.2 * scale, color="#CBD5E1", stroke_width=2.5),
                Line(can.get_bottom() + RIGHT * 0.12 * scale, can.get_bottom() + RIGHT * 0.12 * scale + DOWN * 0.2 * scale, color="#CBD5E1", stroke_width=2.5),
            )

            rating = Text(
                "560µF",
                font=FONTS["mono"],
                font_size=int(7 * scale),
                color="#E2E8F0",
            ).move_to(can.get_center() + RIGHT * 0.06 * scale)

            cap_grp.add(legs, can, stripe, top_cap, x_vent, rating)
            cap_grp.shift(RIGHT * offset_x)
            self.capacitors.add(cap_grp)

        self.add(self.capacitors)
        self._init_done = True


# =====================================================================
# 22. MECHANICAL STEPPER RELAY (Vintage BIOS Mechanism)
# =====================================================================
class MechanicalStepperRelay(InteractiveActor):
    """
    Vintage stepping relay selector representing legacy 16-bit BIOS mode:
    - Stepped contact dial with brass wiper indicator arm
    - Solenoid drive coil housing
    """
    def __init__(self, scale: float = 1.0, **kwargs):
        super().__init__(**kwargs)
        r = 1.15 * scale

        self.chassis = Circle(
            radius=r,
            fill_color="#F1F5F9",
            fill_opacity=1.0,
            stroke_color=PALETTE["stroke"],
            stroke_width=2.4,
        )

        self.contacts = VGroup()
        for i in range(12):
            ang = i * (2 * PI / 12)
            c_pos = self.chassis.get_center() + np.array([r * 0.78 * np.cos(ang), r * 0.78 * np.sin(ang), 0.0])
            c_dot = Dot(c_pos, radius=0.06 * scale, color="#F59E0B")
            self.contacts.add(c_dot)

        self.hub = Circle(radius=0.25 * scale, fill_color="#334155", fill_opacity=1.0, stroke_color="#F59E0B", stroke_width=2.0)
        self.arm = Line(self.hub.get_center(), self.hub.get_center() + UP * 0.75 * scale, color="#F59E0B", stroke_width=3.5 * scale)

        self.plate = Text(
            "STEPPER RELAY",
            font=FONTS["mono"],
            weight="BOLD",
            font_size=int(9 * scale),
            color=PALETTE["text"],
        ).move_to(self.chassis.get_center() + DOWN * 0.45 * scale)

        self.add(self.chassis, self.contacts, self.arm, self.hub, self.plate)
        self._init_done = True


# =====================================================================
# 23. CROSSBAR ROUTING MATRIX (Modern UEFI Architecture)
# =====================================================================
class CrossbarRoutingMatrix(InteractiveActor):
    """
    High-tech UEFI routing matrix with crossbar grid lanes and junction LEDs:
    - Multi-lane bus routing card
    - Glowing active junctions
    """
    def __init__(self, scale: float = 1.0, **kwargs):
        super().__init__(**kwargs)
        mw = 3.2 * scale
        mh = 2.2 * scale

        self.card = RoundedRectangle(
            corner_radius=0.14 * scale,
            width=mw,
            height=mh,
            fill_color=PALETTE["surface_card"],
            fill_opacity=1.0,
            stroke_color=PALETTE["stroke"],
            stroke_width=2.0,
        )

        self.lanes = VGroup()
        for i in range(4):
            hy = -mh * 0.25 + i * (mh * 0.50 / 3)
            self.lanes.add(Line(
                self.card.get_left() + np.array([0.3 * scale, hy, 0]),
                self.card.get_right() + np.array([-0.3 * scale, hy, 0]),
                color=PALETTE["stroke_light"],
                stroke_width=1.5,
            ))
            vx = -mw * 0.35 + i * (mw * 0.70 / 3)
            self.lanes.add(Line(
                self.card.get_bottom() + np.array([vx, 0.35 * scale, 0]),
                self.card.get_top() + np.array([vx, -0.45 * scale, 0]),
                color=PALETTE["stroke_light"],
                stroke_width=1.5,
            ))

        self.nodes = VGroup()
        for r in range(4):
            hy = -mh * 0.25 + r * (mh * 0.50 / 3)
            for c in range(4):
                vx = -mw * 0.35 + c * (mw * 0.70 / 3)
                p = self.card.get_center() + np.array([vx, hy, 0])
                col = PALETTE["indigo"] if (r + c) % 2 == 0 else PALETTE["sky"]
                self.nodes.add(Dot(p, radius=0.05 * scale, color=col))

        self.title = Text(
            "UEFI ROUTING MATRIX",
            font=FONTS["sans"],
            weight="BOLD",
            font_size=int(10 * scale),
            color=PALETTE["text"],
        ).move_to(self.card.get_top() + DOWN * 0.25 * scale)

        self.add(self.card, self.lanes, self.nodes, self.title)
        self._init_done = True


# =====================================================================
# 24. USB FLASH DRIVE ACTOR (USB 3.0 Live Boot Media)
# =====================================================================
class UsbFlashDriveActor(InteractiveActor):
    """
    USB 3.0 Type-A flash drive thumb stick:
    - Anodized aluminum enclosure with activity LED
    - Metallic Type-A connector with blue USB 3.0 insulator block
    """
    def __init__(self, scale: float = 1.0, **kwargs):
        super().__init__(**kwargs)
        bw = 2.2 * scale
        bh = 0.9 * scale
        pw = 0.75 * scale
        ph = 0.65 * scale

        self.body = RoundedRectangle(
            corner_radius=0.12 * scale,
            width=bw,
            height=bh,
            fill_color="#334155",
            fill_opacity=1.0,
            stroke_color=PALETTE["stroke"],
            stroke_width=2.0,
        )

        self.plug = Rectangle(
            width=pw,
            height=ph,
            fill_color="#CBD5E1",
            fill_opacity=1.0,
            stroke_color=PALETTE["stroke"],
            stroke_width=1.5,
        ).next_to(self.body, LEFT, buff=0.0)

        self.insulator = Rectangle(
            width=pw * 0.45,
            height=ph * 0.55,
            fill_color="#0284C7",
            fill_opacity=1.0,
            stroke_width=0,
        ).move_to(self.plug.get_center() + LEFT * 0.1 * scale)

        self.led = Dot(self.body.get_center() + RIGHT * 0.75 * scale, radius=0.06 * scale, color="#38BDF8")

        self.label = Text(
            "USB 3.0 LIVE",
            font=FONTS["mono"],
            weight="BOLD",
            font_size=int(9 * scale),
            color="#FFFFFF",
        ).move_to(self.body.get_center() + LEFT * 0.15 * scale)

        self.add(self.plug, self.insulator, self.body, self.led, self.label)
        self._init_done = True


# =====================================================================
# 25. FIBER OPTIC CONDUIT (PXE Optical Boot Cable)
# =====================================================================
class FiberOpticConduit(InteractiveActor):
    """
    High-speed optical fiber conduit / LC transceiver connector for network PXE boot:
    - Duplex optical transceiver casing
    - Dual illuminated optical fiber cores emitting light pulses
    """
    def __init__(self, scale: float = 1.0, **kwargs):
        super().__init__(**kwargs)
        cw = 2.6 * scale
        ch = 0.85 * scale

        self.housing = RoundedRectangle(
            corner_radius=0.08 * scale,
            width=cw,
            height=ch,
            fill_color="#1E293B",
            fill_opacity=1.0,
            stroke_color=PALETTE["stroke"],
            stroke_width=2.0,
        )

        self.ferrules = VGroup(
            RoundedRectangle(corner_radius=0.04 * scale, width=0.45 * scale, height=0.22 * scale, fill_color="#CBD5E1", fill_opacity=1.0, stroke_width=1.0, stroke_color=PALETTE["stroke"]).move_to(self.housing.get_left() + UP * 0.16 * scale),
            RoundedRectangle(corner_radius=0.04 * scale, width=0.45 * scale, height=0.22 * scale, fill_color="#CBD5E1", fill_opacity=1.0, stroke_width=1.0, stroke_color=PALETTE["stroke"]).move_to(self.housing.get_left() + DOWN * 0.16 * scale),
        )

        self.cores = VGroup(
            Dot(self.ferrules[0].get_left(), radius=0.05 * scale, color="#38BDF8"),
            Dot(self.ferrules[1].get_left(), radius=0.05 * scale, color="#38BDF8"),
        )

        self.label = Text(
            "PXE GIGABIT FIBER",
            font=FONTS["mono"],
            weight="BOLD",
            font_size=int(9 * scale),
            color="#38BDF8",
        ).move_to(self.housing.get_center() + RIGHT * 0.15 * scale)

        self.add(self.ferrules, self.cores, self.housing, self.label)
        self._init_done = True


# =====================================================================
# 26. STORAGE SECTOR ARRAY (MBR 512-Byte Disk Sectors)
# =====================================================================
class StorageSectorArray(InteractiveActor):
    """
    Physical disk storage sector strip highlighting Sector 0 (MBR 512B):
    - Strip array of contiguous disk sectors
    - Distinctive Sector 0 block with partition table marks
    """
    def __init__(self, scale: float = 1.0, **kwargs):
        super().__init__(**kwargs)
        aw = 5.6 * scale
        ah = 1.25 * scale

        self.bg = RoundedRectangle(
            corner_radius=0.10 * scale,
            width=aw,
            height=ah,
            fill_color=PALETTE["surface_card"],
            fill_opacity=1.0,
            stroke_color=PALETTE["stroke"],
            stroke_width=2.0,
        )

        s0_w = 1.9 * scale
        self.sector_0 = RoundedRectangle(
            corner_radius=0.08 * scale,
            width=s0_w,
            height=ah * 0.82,
            fill_color="#EEF2FF",
            fill_opacity=1.0,
            stroke_color="#4F46E5",
            stroke_width=2.0,
        ).move_to(self.bg.get_left() + RIGHT * (s0_w / 2.0 + 0.18 * scale))

        s0_title = Text("SECTOR 0 (MBR)", font=FONTS["mono"], weight="BOLD", font_size=int(9 * scale), color="#4F46E5").move_to(self.sector_0.get_center() + UP * 0.16 * scale)
        s0_sub = Text("512 BYTES", font=FONTS["mono"], font_size=int(8 * scale), color="#6B7280").move_to(self.sector_0.get_center() + DOWN * 0.16 * scale)
        self.sector_0_grp = VGroup(self.sector_0, s0_title, s0_sub)

        self.other_sectors = VGroup()
        for i in range(3):
            sx = self.bg.get_left()[0] + s0_w + 0.4 * scale + i * (1.1 * scale)
            sec = RoundedRectangle(
                corner_radius=0.06 * scale,
                width=1.0 * scale,
                height=ah * 0.82,
                fill_color="#F8FAFC",
                fill_opacity=1.0,
                stroke_color=PALETTE["stroke_light"],
                stroke_width=1.2,
            ).move_to([sx, self.bg.get_center()[1], 0.0])
            lbl = Text(f"LBA {i+1}", font=FONTS["mono"], font_size=int(8 * scale), color=PALETTE["text_dim"]).move_to(sec.get_center())
            self.other_sectors.add(VGroup(sec, lbl))

        self.add(self.bg, self.sector_0_grp, self.other_sectors)
        self._init_done = True


# =====================================================================
# 27. ROTARY DISPATCH SWITCH (GRUB Multiboot Dispatcher)
# =====================================================================
class RotaryDispatchSwitch(InteractiveActor):
    """
    GRUB multiboot dispatch switch:
    - Clean card enclosure with central rotary dial selector
    - Labeled boot targets (Linux Kernel, Recovery, Firmware)
    """
    def __init__(self, scale: float = 1.0, **kwargs):
        super().__init__(**kwargs)
        dw = 3.6 * scale
        dh = 2.4 * scale

        self.card = RoundedRectangle(
            corner_radius=0.16 * scale,
            width=dw,
            height=dh,
            fill_color=PALETTE["surface_card"],
            fill_opacity=1.0,
            stroke_color=PALETTE["stroke"],
            stroke_width=2.0,
        )

        self.knob = Circle(
            radius=0.52 * scale,
            fill_color="#1E293B",
            fill_opacity=1.0,
            stroke_color=PALETTE["stroke"],
            stroke_width=2.0,
        ).move_to(self.card.get_center() + LEFT * 0.65 * scale)

        self.notch = Line(
            self.knob.get_center(),
            self.knob.get_center() + RIGHT * 0.48 * scale,
            color="#38BDF8",
            stroke_width=3.5 * scale,
        )

        self.entries = VGroup()
        entry_labels = ["Ubuntu / Linux", "Recovery Mode", "UEFI Setup"]
        for i, el in enumerate(entry_labels):
            ey = self.card.get_center()[1] + (0.55 * scale if i == 0 else (0.0 if i == 1 else -0.55 * scale))
            p_fill = PALETTE["indigo"] if i == 0 else "#F1F5F9"
            p_text_c = "#FFFFFF" if i == 0 else PALETTE["text"]
            p_box = RoundedRectangle(
                corner_radius=0.08 * scale,
                width=1.8 * scale,
                height=0.38 * scale,
                fill_color=p_fill,
                fill_opacity=1.0,
                stroke_color=PALETTE["stroke_light"] if i != 0 else PALETTE["indigo"],
                stroke_width=1.0,
            ).move_to([self.card.get_center()[0] + 0.75 * scale, ey, 0.0])
            p_txt = Text(el, font=FONTS["sans"], font_size=int(9 * scale), color=p_text_c).move_to(p_box.get_center())
            self.entries.add(VGroup(p_box, p_txt))

        self.title = Text(
            "GRUB BOOT DISPATCHER",
            font=FONTS["sans"],
            weight="BOLD",
            font_size=int(10 * scale),
            color=PALETTE["text"],
        ).move_to(self.card.get_top() + DOWN * 0.22 * scale)

        self.add(self.card, self.knob, self.notch, self.entries, self.title)
        self._init_done = True


# =====================================================================
# 28. FILESYSTEM HIERARCHY TREE
# =====================================================================
class FilesystemHierarchyTree(InteractiveActor):
    """
    Linux directory tree hierarchy:
    - Root / apex node card
    - Radiating tree branches to /bin, /lib, /etc
    """
    def __init__(
        self,
        apex_position=None,
        branch_positions=None,
        scale: float = 1.0,
        **kwargs
    ):
        super().__init__(**kwargs)
        apex_p = np.array(apex_position) if apex_position is not None else np.array([0.0, 1.4, 0.0])
        branches_p = branch_positions or [[-1.8, -0.1, 0.0], [0.0, -0.1, 0.0], [1.8, -0.1, 0.0]]

        self.root_card = RoundedRectangle(
            corner_radius=0.10 * scale,
            width=1.2 * scale,
            height=0.65 * scale,
            fill_color=PALETTE["surface_card"],
            fill_opacity=1.0,
            color=PALETTE["stroke"],
            stroke_width=2.0,
        ).move_to(apex_p)
        root_label = Text("/", font=FONTS["mono"], weight="BOLD", font_size=int(18 * scale), color=PALETTE["blue"]).move_to(self.root_card.get_center())
        self.root_group = VGroup(self.root_card, root_label)

        branch_names = ["/bin", "/lib", "/etc"]
        self.branches = VGroup()
        self.connectors = VGroup()

        for i, bp in enumerate(branches_p):
            p = np.array(bp)
            card = RoundedRectangle(
                corner_radius=0.08 * scale,
                width=1.1 * scale,
                height=0.55 * scale,
                fill_color=PALETTE["surface_card"],
                fill_opacity=1.0,
                color=PALETTE["stroke"],
                stroke_width=1.8,
            ).move_to(p)
            lbl = Text(branch_names[i % len(branch_names)], font=FONTS["mono"], weight="SEMIBOLD", font_size=int(12 * scale), color=PALETTE["text"]).move_to(card.get_center())
            self.branches.add(VGroup(card, lbl))

            conn = Line(
                self.root_card.get_bottom(),
                card.get_top(),
                color=PALETTE["stroke_light"],
                stroke_width=2.0,
            )
            self.connectors.add(conn)

        self.add(self.connectors, self.root_group, self.branches)
        self._init_done = True


# =====================================================================
# 29. FILESYSTEM NODE ACTOR (/sbin/init Executable)
# =====================================================================
class FilesystemNodeActor(InteractiveActor):
    """
    Standalone Linux filesystem node actor representing /sbin/init:
    - Card enclosure with binary chip gear badge
    - Monospace executable path
    """
    def __init__(self, scale: float = 1.0, path: str = "/sbin/init", **kwargs):
        super().__init__(**kwargs)
        nw = 2.6 * scale
        nh = 1.25 * scale

        self.card = RoundedRectangle(
            corner_radius=0.12 * scale,
            width=nw,
            height=nh,
            fill_color=PALETTE["surface_card"],
            fill_opacity=1.0,
            stroke_color=PALETTE["stroke"],
            stroke_width=2.0,
        )

        self.pill = RoundedRectangle(
            corner_radius=0.06 * scale,
            width=1.4 * scale,
            height=0.28 * scale,
            fill_color="#DCFCE7",
            fill_opacity=1.0,
            stroke_color="#16A34A",
            stroke_width=1.0,
        ).move_to(self.card.get_center() + UP * 0.28 * scale)

        pill_txt = Text("EXECUTABLE (ELF)", font=FONTS["mono"], font_size=int(8 * scale), color="#166534").move_to(self.pill.get_center())
        self.path_txt = Text(path, font=FONTS["mono"], weight="BOLD", font_size=int(12 * scale), color=PALETTE["text"]).move_to(self.card.get_center() + DOWN * 0.15 * scale)

        self.add(self.card, self.pill, pill_txt, self.path_txt)
        self._init_done = True


# =====================================================================
# 30. CYBERNETIC TURBINE HUB (systemd PID 1 Supervisor)
# =====================================================================
class CyberneticTurbineHub(InteractiveActor):
    """
    High-velocity supervisor turbine hub representing systemd (PID 1):
    - Multi-stage stator housing with peripheral indicator LEDs
    - 8 aerodynamic radial turbine blades
    - Central luminous core with PID 1 systemd badge
    """
    def __init__(self, scale: float = 1.0, **kwargs):
        super().__init__(**kwargs)
        r = 1.25 * scale

        self.stator = Circle(
            radius=r,
            fill_color="#0F172A",
            fill_opacity=1.0,
            stroke_color=PALETTE["stroke"],
            stroke_width=2.5,
        )

        self.blades = VGroup()
        for i in range(8):
            ang = i * (2 * PI / 8)
            blade = Polygon(
                np.array([0.35 * scale * np.cos(ang), 0.35 * scale * np.sin(ang), 0]),
                np.array([r * 0.85 * np.cos(ang + 0.15), r * 0.85 * np.sin(ang + 0.15), 0]),
                np.array([r * 0.85 * np.cos(ang + 0.35), r * 0.85 * np.sin(ang + 0.35), 0]),
                fill_color="#0284C7",
                fill_opacity=0.85,
                stroke_color="#38BDF8",
                stroke_width=1.0,
            )
            self.blades.add(blade)

        self.core = Circle(
            radius=0.48 * scale,
            fill_color="#1E293B",
            fill_opacity=1.0,
            stroke_color="#38BDF8",
            stroke_width=2.0,
        )

        self.core_txt = Text("PID 1", font=FONTS["mono"], weight="BOLD", font_size=int(12 * scale), color="#FFFFFF").move_to(self.core.get_center() + UP * 0.1 * scale)
        self.core_sub = Text("systemd", font=FONTS["sans"], font_size=int(8 * scale), color="#38BDF8").move_to(self.core.get_center() + DOWN * 0.14 * scale)

        self.add(self.stator, self.blades, self.core, self.core_txt, self.core_sub)
        self._init_done = True


__all__ = [
    "InteractiveActor",
    "PhoneDevice",
    "MacBookDevice",
    "ModernRouter",
    "ServerRackActor",
    "HighSpeedTrain",
    "EddyBrakeAssembly",
    "SatelliteActor",
    "PlanetEarth",
    "CryptographicPadlock",
    "DataPacketActor",
    "CellTowerActor",
    "ChipSoC",
    "LocationPin",
    "MotherboardSection",
    "RamModuleActor",
    "NvmeSsdActor",
    "QuartzOscillator",
    "SpiFlashRom",
    "DiagnosticSpeaker",
    "ATX24PinConnector",
    "CapacitorBank",
    "MechanicalStepperRelay",
    "CrossbarRoutingMatrix",
    "UsbFlashDriveActor",
    "FiberOpticConduit",
    "StorageSectorArray",
    "RotaryDispatchSwitch",
    "FilesystemHierarchyTree",
    "FilesystemNodeActor",
    "CyberneticTurbineHub",
    "MacOSPill",
    "MacOSWindow",
    "TechCard",
    "VisualCard",
    "MetricGauge",
    "MilestoneTimeline",
    "SleekArrow",
    "DimensionRuler",
    "LeaderCallout",
]
