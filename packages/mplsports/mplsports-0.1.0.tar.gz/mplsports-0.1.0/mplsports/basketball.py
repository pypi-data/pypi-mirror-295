import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc
from .base import BasePitch
from .dimensions import BasketballDimensions


class BasketballPitch(BasePitch):
    def __init__(
        self,
        court_color="#dfbb85",
        line_color="black",
        paint_color="#c1e1ec",
        court_type="nba",
        axis=False,
        label=False,
        tick=False,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.court_color = court_color
        self.line_color = line_color
        self.paint_color = paint_color
        self.court_type = court_type
        self.axis = axis
        self.label = label
        self.tick = tick
        self.dimensions = BasketballDimensions(court_type)

    def _draw_field(self):
        self.ax.set_facecolor(self.court_color)

        # Main court outline
        self.ax.add_patch(
            Rectangle(
                (0, 0),
                self.dimensions.length,
                self.dimensions.width,
                fill=False,
                ec=self.line_color,
            )
        )

        # Paint area
        for x in [0, self.dimensions.length - self.dimensions.key_height]:
            self.ax.add_patch(
                Rectangle(
                    (x, (self.dimensions.width - self.dimensions.key_width) / 2),
                    self.dimensions.key_height,
                    self.dimensions.key_width,
                    fill=True,
                    fc=self.paint_color,
                    ec=self.line_color,
                )
            )

        # Free throw line
        for x in [
            self.dimensions.free_throw_line_distance,
            self.dimensions.length - self.dimensions.free_throw_line_distance,
        ]:
            self.ax.add_line(
                plt.Line2D(
                    [x, x],
                    [
                        (self.dimensions.width - self.dimensions.key_width) / 2,
                        (self.dimensions.width + self.dimensions.key_width) / 2,
                    ],
                    color=self.line_color,
                )
            )

        # Free throw circle
        for x in [
            self.dimensions.free_throw_line_distance,
            self.dimensions.length - self.dimensions.free_throw_line_distance,
        ]:
            self.ax.add_patch(
                Arc(
                    (x, self.dimensions.width / 2),
                    self.dimensions.free_throw_circle_radius * 2,
                    self.dimensions.free_throw_circle_radius * 2,
                    theta1=0,
                    theta2=180,
                    ec=self.line_color,
                )
            )

        # Backboard
        for x in [
            self.dimensions.backboard_distance,
            self.dimensions.length - self.dimensions.backboard_distance,
        ]:
            self.ax.add_line(
                plt.Line2D(
                    [x, x],
                    [
                        (self.dimensions.width / 2) - (self.dimensions.backboard_width / 2),
                        (self.dimensions.width / 2) + (self.dimensions.backboard_width / 2),
                    ],
                    color=self.line_color,
                )
            )

        # Hoop
        for x in [0, self.dimensions.length]:
            self.ax.add_patch(
                Circle(
                    (x, self.dimensions.width / 2),
                    radius=self.dimensions.rim_diameter / 2,
                    fill=False,
                    ec=self.line_color,
                )
            )

        # Restricted Area
        for x in [0, self.dimensions.length]:
            self.ax.add_patch(
                Arc(
                    (x, self.dimensions.width / 2),
                    self.dimensions.restricted_area_radius * 2,
                    self.dimensions.restricted_area_radius * 2,
                    theta1=0,
                    theta2=180,
                    ec=self.line_color,
                )
            )

        # Three-point line
        self.ax.add_patch(
            Arc(
                (0, self.dimensions.width / 2),
                self.dimensions.three_point_radius * 2,
                self.dimensions.three_point_radius * 2,
                theta1=270,
                theta2=90,
                ec=self.line_color,
            )
        )
        self.ax.add_patch(
            Arc(
                (self.dimensions.length, self.dimensions.width / 2),
                self.dimensions.three_point_radius * 2,
                self.dimensions.three_point_radius * 2,
                theta1=90,
                theta2=270,
                ec=self.line_color,
            )
        )

        # Three-point line straight parts
        self.ax.add_line(
            plt.Line2D(
                [self.dimensions.three_point_line_distance, self.dimensions.three_point_line_distance],
                [
                    self.dimensions.width / 2 - self.dimensions.three_point_radius,
                    self.dimensions.width / 2 + self.dimensions.three_point_radius,
                ],
                color=self.line_color,
            )
        )
        self.ax.add_line(
            plt.Line2D(
                [
                    self.dimensions.length - self.dimensions.three_point_line_distance,
                    self.dimensions.length - self.dimensions.three_point_line_distance,
                ],
                [
                    self.dimensions.width / 2 - self.dimensions.three_point_radius,
                    self.dimensions.width / 2 + self.dimensions.three_point_radius,
                ],
                color=self.line_color,
            )
        )

        # Center line
        self.ax.add_line(
            plt.Line2D(
                [self.dimensions.length / 2, self.dimensions.length / 2],
                [0, self.dimensions.width],
                color=self.line_color,
            )
        )

        # Center circles
        self.ax.add_patch(
            Circle(
                (self.dimensions.length / 2, self.dimensions.width / 2),
                radius=self.dimensions.center_circle_radius,
                fill=False,
                ec=self.line_color,
            )
        )
        self.ax.add_patch(
            Circle(
                (self.dimensions.length / 2, self.dimensions.width / 2),
                radius=self.dimensions.free_throw_circle_radius,
                fill=False,
                ec=self.line_color,
            )
        )

        # Lane lines
        for x in [
            self.dimensions.lane_line_distance,
            self.dimensions.length - self.dimensions.lane_line_distance,
        ]:
            self.ax.add_line(
                plt.Line2D(
                    [x, x],
                    [0, self.dimensions.width],
                    color=self.line_color,
                )
            )

        # No-charge semi-circle
        for x in [0, self.dimensions.length]:
            self.ax.add_patch(
                Arc(
                    (x, self.dimensions.width / 2),
                    self.dimensions.no_charge_semi_circle_radius * 2,
                    self.dimensions.no_charge_semi_circle_radius * 2,
                    theta1=0,
                    theta2=180,
                    ec=self.line_color,
                )
            )

        # Lower Defensive Box
        for x in [
            self.dimensions.lower_defensive_box_distance,
            self.dimensions.length - self.dimensions.lower_defensive_box_distance,
        ]:
            self.ax.add_line(
                plt.Line2D(
                    [x, x],
                    [
                        (self.dimensions.width / 2) - (self.dimensions.key_width / 2),
                        (self.dimensions.width / 2) + (self.dimensions.key_width / 2),
                    ],
                    color=self.line_color,
                    linestyle='--'
                )
            )

        # Coaching Box and Team Bench Area
        self.ax.add_patch(
            Rectangle(
                (self.dimensions.length / 2 - self.dimensions.coaching_box_distance / 2, 0),
                self.dimensions.coaching_box_distance,
                self.dimensions.width,
                fill=False,
                ec=self.line_color,
                linestyle='--'
            )
        )

        # Substitution Box
        self.ax.add_patch(
            Rectangle(
                (self.dimensions.length / 2 - self.dimensions.substitution_box_distance / 2, self.dimensions.width / 2 - 1),
                self.dimensions.substitution_box_distance,
                2,
                fill=False,
                ec=self.line_color,
                linestyle='--'
            )
        )

        # Game Officials and Scorers Table
        self.ax.add_patch(
            Rectangle(
                (self.dimensions.length / 2 - self.dimensions.game_officials_table_distance / 2, self.dimensions.width / 2 - 2),
                self.dimensions.game_officials_table_distance,
                4,
                fill=False,
                ec=self.line_color,
                linestyle='--'
            )
        )

        # Midcourt Area Marker (Hash Mark or Throw-in Line)
        self.ax.add_line(
            plt.Line2D(
                [self.dimensions.length / 2, self.dimensions.length / 2],
                [0, self.dimensions.width],
                color=self.line_color,
                linestyle='--'
            )
        )

        # Baseline or Endline
        self.ax.add_line(
            plt.Line2D(
                [0, self.dimensions.length],
                [0, 0],
                color=self.line_color
            )
        )
        self.ax.add_line(
            plt.Line2D(
                [0, self.dimensions.length],
                [self.dimensions.width, self.dimensions.width],
                color=self.line_color
            )
        )

        # Sideline
        self.ax.add_line(
            plt.Line2D(
                [0, 0],
                [0, self.dimensions.width],
                color=self.line_color
            )
        )
        self.ax.add_line(
            plt.Line2D(
                [self.dimensions.length, self.dimensions.length],
                [0, self.dimensions.width],
                color=self.line_color
            )
        )

        # Center Circle or Restraining Circle
        self.ax.add_patch(
            Circle(
                (self.dimensions.length / 2, self.dimensions.width / 2),
                radius=self.dimensions.center_circle_radius,
                fill=False,
                ec=self.line_color
            )
        )

        # Half-court Line (Midcourt Line, Division Line, Center Line, Ten-second Line, Time Line)
        self.ax.add_line(
            plt.Line2D(
                [self.dimensions.length / 2, self.dimensions.length / 2],
                [0, self.dimensions.width],
                color=self.line_color
            )
        )

        # Three-Point Line (The Arc)
        self.ax.add_patch(
            Arc(
                (0, self.dimensions.width / 2),
                self.dimensions.three_point_radius * 2,
                self.dimensions.three_point_radius * 2,
                theta1=270,
                theta2=90,
                ec=self.line_color
            )
        )
        self.ax.add_patch(
            Arc(
                (self.dimensions.length, self.dimensions.width / 2),
                self.dimensions.three_point_radius * 2,
                self.dimensions.three_point_radius * 2,
                theta1=90,
                theta2=270,
                ec=self.line_color
            )
        )

        # Free-throw Circle or Restraining Circle
        self.ax.add_patch(
            Circle(
                (self.dimensions.free_throw_line_distance, self.dimensions.width / 2),
                radius=self.dimensions.free_throw_circle_radius,
                fill=False,
                ec=self.line_color
            )
        )
        self.ax.add_patch(
            Circle(
                (self.dimensions.length - self.dimensions.free_throw_line_distance, self.dimensions.width / 2),
                radius=self.dimensions.free_throw_circle_radius,
                fill=False,
                ec=self.line_color
            )
        )

        # Foul Line or Free-throw Line
        self.ax.add_line(
            plt.Line2D(
                [self.dimensions.free_throw_line_distance, self.dimensions.free_throw_line_distance],
                [
                    (self.dimensions.width - self.dimensions.key_width) / 2,
                    (self.dimensions.width + self.dimensions.key_width) / 2,
                ],
                color=self.line_color
            )
        )
        self.ax.add_line(
            plt.Line2D(
                [self.dimensions.length - self.dimensions.free_throw_line_distance, self.dimensions.length - self.dimensions.free_throw_line_distance],
                [
                    (self.dimensions.width - self.dimensions.key_width) / 2,
                    (self.dimensions.width + self.dimensions.key_width) / 2,
                ],
                color=self.line_color
            )
        )

        # Lane Line
        for x in [
            self.dimensions.lane_line_distance,
            self.dimensions.length - self.dimensions.lane_line_distance,
        ]:
            self.ax.add_line(
                plt.Line2D(
                    [x, x],
                    [
                        (self.dimensions.width - self.dimensions.key_width) / 2,
                        (self.dimensions.width + self.dimensions.key_width) / 2,
                    ],
                    color=self.line_color
                )
            )

        # No-charge Semi-circle
        for x in [self.dimensions.backboard_distance, self.dimensions.length - self.dimensions.backboard_distance]:
            self.ax.add_patch(
                Arc(
                    (x, self.dimensions.width / 2),
                    self.dimensions.no_charge_semi_circle_radius * 2,
                    self.dimensions.no_charge_semi_circle_radius * 2,
                    theta1=0,
                    theta2=180,
                    ec=self.line_color
                )
            )

        # Basket or Hoop
        for x in [self.dimensions.backboard_distance, self.dimensions.length - self.dimensions.backboard_distance]:
            self.ax.add_patch(
                Circle(
                    (x, self.dimensions.width / 2),
                    radius=self.dimensions.rim_diameter / 2,
                    fill=False,
                    ec=self.line_color
                )
            )

        # Backboard
        for x in [
            self.dimensions.backboard_distance,
            self.dimensions.length - self.dimensions.backboard_distance,
        ]:
            self.ax.add_line(
                plt.Line2D(
                    [x, x],
                    [
                        (self.dimensions.width / 2) - (self.dimensions.backboard_width / 2),
                        (self.dimensions.width / 2) + (self.dimensions.backboard_width / 2),
                    ],
                    color=self.line_color
                )
            )

    def _set_field_dimensions(self):
        self.ax.set_xlim(-2, self.dimensions.length + 2)
        self.ax.set_ylim(-2, self.dimensions.width + 2)
        self.ax.set_aspect("equal")

        if not self.axis:
            self.ax.axis("off")
        if not self.tick:
            self.ax.set_xticks([])
            self.ax.set_yticks([])
        if self.label:
            self.ax.set_xlabel("X")
            self.ax.set_ylabel("Y")

    def scatter(self, x, y, **kwargs):
        return self.ax.scatter(x, y, **kwargs)

    def heatmap(self, x, y, **kwargs):
        return self.ax.hexbin(
            x, y, extent=[0, self.dimensions.length, 0, self.dimensions.width], **kwargs
        )
