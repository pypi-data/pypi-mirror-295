# mplsports/tennis.py

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from .base import BasePitch


class TennisPitch(BasePitch):
    def __init__(self, court_color="#4a7732", line_color="black", **kwargs):
        super().__init__(**kwargs)
        self.court_color = court_color
        self.line_color = line_color
        self.court_length = 23.77  # in meters
        self.court_width = 10.97  # in meters for doubles

    def _draw_field(self):
        # Set court background color
        self.ax.set_facecolor(self.court_color)

        # Draw outer rectangle (doubles court)
        self.ax.add_patch(
            Rectangle(
                (0, 0),
                self.court_length,
                self.court_width,
                fill=False,
                ec=self.line_color,
            )
        )

        # Draw singles court
        singles_width = 8.23
        self.ax.add_patch(
            Rectangle(
                (0, (self.court_width - singles_width) / 2),
                self.court_length,
                singles_width,
                fill=False,
                ec=self.line_color,
            )
        )

        # Draw service lines
        service_line = 6.40
        self.ax.plot(
            [service_line, service_line],
            [
                (self.court_width - singles_width) / 2,
                (self.court_width + singles_width) / 2,
            ],
            color=self.line_color,
        )
        self.ax.plot(
            [self.court_length - service_line, self.court_length - service_line],
            [
                (self.court_width - singles_width) / 2,
                (self.court_width + singles_width) / 2,
            ],
            color=self.line_color,
        )

        # Draw center service line
        self.ax.plot(
            [service_line, service_line],
            [self.court_width / 2 - 0.1, self.court_width / 2 + 0.1],
            color=self.line_color,
        )
        self.ax.plot(
            [self.court_length - service_line, self.court_length - service_line],
            [self.court_width / 2 - 0.1, self.court_width / 2 + 0.1],
            color=self.line_color,
        )

        # Draw net
        self.ax.plot(
            [self.court_length / 2, self.court_length / 2],
            [0, self.court_width],
            color=self.line_color,
        )

    def _set_field_dimensions(self):
        self.ax.set_xlim(-1, self.court_length + 1)
        self.ax.set_ylim(-1, self.court_width + 1)

    def scatter(self, x, y, **kwargs):
        return self.ax.scatter(x, y, **kwargs)

    def heatmap(self, x, y, **kwargs):
        return self.ax.hexbin(x, y, **kwargs)
