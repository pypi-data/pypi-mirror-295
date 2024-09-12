from .base import BasePitch
from .dimensions import HandballDimensions
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Arc


class HandballPitch(BasePitch):
    def __init__(
        self,
        court_color="#4a7732",
        line_color="white",
        goal_color="red",
        axis=False,
        label=False,
        tick=False,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.court_color = court_color
        self.line_color = line_color
        self.goal_color = goal_color
        self.dimensions = HandballDimensions()
        self.axis = axis
        self.label = label
        self.tick = tick

    def _draw_field(self):
        # Set court background color
        self.ax.set_facecolor(self.court_color)

        # Draw outer rectangle
        self.ax.add_patch(
            Rectangle(
                (0, 0),
                self.dimensions.length,
                self.dimensions.width,
                fill=False,
                ec=self.line_color,
                lw=self.dimensions.center_line_width * 100,
            )
        )

        # Draw center line
        self.ax.plot(
            [self.dimensions.length / 2, self.dimensions.length / 2],
            [0, self.dimensions.width],
            color=self.line_color,
            lw=self.dimensions.center_line_width * 100,
        )

        # Draw goal areas
        for x in [0, self.dimensions.length]:
            self.ax.add_patch(
                Rectangle(
                    (
                        x if x == 0 else x - self.dimensions.goal_area_length,
                        (self.dimensions.width - self.dimensions.goal_width) / 2,
                    ),
                    self.dimensions.goal_area_length,
                    self.dimensions.goal_width,
                    fill=False,
                    ec=self.line_color,
                    lw=self.dimensions.goal_area_line_width * 100,
                )
            )

        # Draw free throw lines
        for x in [
            self.dimensions.free_throw_line_distance,
            self.dimensions.length - self.dimensions.free_throw_line_distance,
        ]:
            self.ax.add_patch(
                Arc(
                    (x, self.dimensions.width / 2),
                    height=self.dimensions.width,
                    width=self.dimensions.width,
                    theta1=90,
                    theta2=270 if x < self.dimensions.length / 2 else -90,
                    color=self.line_color,
                    lw=self.dimensions.center_line_width * 100,
                )
            )

        # Draw 7-meter lines
        for x in [
            self.dimensions.seven_meter_line,
            self.dimensions.length - self.dimensions.seven_meter_line,
        ]:
            self.ax.plot(
                [x, x],
                [self.dimensions.width / 2 - 0.5, self.dimensions.width / 2 + 0.5],
                color=self.line_color,
                lw=self.dimensions.center_line_width * 100,
            )

        # Draw goals
        for x in [0, self.dimensions.length]:
            self.ax.add_patch(
                Rectangle(
                    (
                        x if x == 0 else x - 0.5,
                        (self.dimensions.width - self.dimensions.goal_width) / 2,
                    ),
                    0.5,
                    self.dimensions.goal_width,
                    fill=False,
                    ec=self.goal_color,
                    lw=self.dimensions.center_line_width * 100,
                )
            )

        # Draw substitution areas
        for y in [0, self.dimensions.width]:
            self.ax.plot(
                [
                    self.dimensions.length / 2
                    - self.dimensions.substitution_area_length,
                    self.dimensions.length / 2
                    + self.dimensions.substitution_area_length,
                ],
                [y, y],
                color=self.line_color,
                lw=self.dimensions.center_line_width * 100,
            )

    def _set_field_dimensions(self):
        self.ax.set_xlim(-1, self.dimensions.length + 1)
        self.ax.set_ylim(-1, self.dimensions.width + 1)
        self.ax.set_aspect("equal")

        if not self.axis:
            self.ax.axis("off")
        if not self.tick:
            self.ax.set_xticks([])
            self.ax.set_yticks([])
        if self.label:
            self.ax.set_xlabel("Length (m)")
            self.ax.set_ylabel("Width (m)")

    def scatter(self, x, y, **kwargs):
        return self.ax.scatter(x, y, **kwargs)

    def heatmap(self, x, y, **kwargs):
        return self.ax.hexbin(x, y, **kwargs)
