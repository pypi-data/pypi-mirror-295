import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Arc, Circle
from .base import BasePitch
from .dimensions import SoccerDimensions


class SoccerPitch(BasePitch):
    def __init__(
        self,
        pitch_color="#a8bc95",
        line_color="black",
        pitch_length=105,
        pitch_width=68,
        axis=False,
        label=False,
        tick=False,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.pitch_color = pitch_color
        self.line_color = line_color
        self.pitch_length = pitch_length
        self.pitch_width = pitch_width
        self.axis = axis
        self.label = label
        self.tick = tick
        self.dimensions = SoccerDimensions(pitch_length, pitch_width)

    def _draw_field(self):
        # Pitch outline
        self.ax.add_patch(
            Rectangle(
                (0, 0),
                self.dimensions.length,
                self.dimensions.width,
                ec=self.line_color,
                fc=self.pitch_color,  # Change 'none' to self.pitch_color
            )
        )

        # Left penalty area
        self.ax.add_patch(
            Rectangle(
                (
                    0,
                    (self.dimensions.width - self.dimensions.penalty_area_width) / 2,
                ),
                self.dimensions.penalty_area_length,
                self.dimensions.penalty_area_width,
                ec=self.line_color,
                fc="none",
            )
        )

        # Right penalty area
        self.ax.add_patch(
            Rectangle(
                (
                    self.dimensions.length - self.dimensions.penalty_area_length,
                    (self.dimensions.width - self.dimensions.penalty_area_width) / 2,
                ),
                self.dimensions.penalty_area_length,
                self.dimensions.penalty_area_width,
                ec=self.line_color,
                fc="none",
            )
        )
        # Left 6-yard box
        self.ax.add_patch(
            Rectangle(
                (
                    0,
                    (self.dimensions.width - self.dimensions.six_yard_box_width) / 2,
                ),
                self.dimensions.six_yard_box_length,
                self.dimensions.six_yard_box_width,
                ec=self.line_color,
                fc="none",
            )
        )

        # Right 6-yard box
        self.ax.add_patch(
            Rectangle(
                (
                    self.dimensions.length - self.dimensions.six_yard_box_length,
                    (self.dimensions.width - self.dimensions.six_yard_box_width) / 2,
                ),
                self.dimensions.six_yard_box_length,
                self.dimensions.six_yard_box_width,
                ec=self.line_color,
                fc="none",
            )
        )

        # Halfway line
        self.ax.plot(
            [self.dimensions.length / 2, self.dimensions.length / 2],
            [0, self.dimensions.width],
            color=self.line_color,
        )

        # Center circle
        center_circle = plt.Circle(
            (self.dimensions.length / 2, self.dimensions.width / 2),
            self.dimensions.center_circle_radius,
            color=self.line_color,
            fill=False,
        )
        self.ax.add_artist(center_circle)

        # Penalty spots
        self.ax.plot(
            self.dimensions.penalty_spot_distance,
            self.dimensions.width / 2,
            "o",
            color=self.line_color,
            markersize=2,
        )
        self.ax.plot(
            self.dimensions.length - self.dimensions.penalty_spot_distance,
            self.dimensions.width / 2,
            "o",
            color=self.line_color,
            markersize=2,
        )

        # Penalty arcs
        left_arc = Arc(
            (self.dimensions.penalty_spot_distance, self.dimensions.width / 2),
            height=self.dimensions.penalty_arc_radius * 2,
            width=self.dimensions.penalty_arc_radius * 2,
            angle=0,
            theta1=307,
            theta2=53,
            color=self.line_color,
        )
        self.ax.add_patch(left_arc)

        right_arc = Arc(
            (
                self.dimensions.length - self.dimensions.penalty_spot_distance,
                self.dimensions.width / 2,
            ),
            height=self.dimensions.penalty_arc_radius * 2,
            width=self.dimensions.penalty_arc_radius * 2,
            angle=0,
            theta1=127,
            theta2=233,
            color=self.line_color,
        )
        self.ax.add_patch(right_arc)

        # Add goal posts
        self._draw_goal_posts()

    def _draw_goal_posts(self):
        # Left goal
        self.ax.plot([0, 0], 
                     [(self.dimensions.width - self.dimensions.goal_width) / 2, 
                      (self.dimensions.width + self.dimensions.goal_width) / 2],
                     color=self.line_color, linewidth=2)
        
        # Right goal
        self.ax.plot([self.dimensions.length, self.dimensions.length], 
                     [(self.dimensions.width - self.dimensions.goal_width) / 2, 
                      (self.dimensions.width + self.dimensions.goal_width) / 2],
                     color=self.line_color, linewidth=2)

    def _set_field_dimensions(self):
        self.ax.set_xlim(-5, self.dimensions.length + 5)
        self.ax.set_ylim(-5, self.dimensions.width + 5)
        self.ax.set_aspect("equal")

        if not self.axis:
            self.ax.axis("off")
        else:
            self.ax.spines["top"].set_visible(False)
            self.ax.spines["right"].set_visible(False)
            self.ax.spines["bottom"].set_visible(False)
            self.ax.spines["left"].set_visible(False)

        if not self.tick:
            self.ax.set_xticks([])
            self.ax.set_yticks([])
        else:
            self.ax.set_xticks(range(0, int(self.dimensions.length) + 1, 10))
            self.ax.set_yticks(range(0, int(self.dimensions.width) + 1, 10))
            self.ax.tick_params(axis="both", which="both", length=0)

        if self.label:
            self.ax.set_xlabel("Length (m)")
            self.ax.set_ylabel("Width (m)")
        else:
            self.ax.set_xlabel("")
            self.ax.set_ylabel("")

    def scatter(self, x, y, **kwargs):
        return self.ax.scatter(x, y, **kwargs)

    def heatmap(self, x, y, **kwargs):
        return self.ax.hexbin(
            x,
            y,
            extent=[0, self.dimensions.length, 0, self.dimensions.width],
            **kwargs,
        )
