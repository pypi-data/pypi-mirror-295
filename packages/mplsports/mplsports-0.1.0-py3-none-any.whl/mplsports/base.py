from abc import ABC, abstractmethod
import matplotlib.pyplot as plt


class BasePitch(ABC):
    def __init__(
        self, figsize=(10, 7), dpi=100, field_color=None, line_color=None, **kwargs
    ):
        self.figsize = figsize
        self.dpi = dpi
        self.field_color = field_color
        self.line_color = line_color
        self.ax = None
        self.fig = None

    @abstractmethod
    def _draw_field(self):
        """Draw the basic field/court outline and markings."""
        pass

    @abstractmethod
    def _set_field_dimensions(self):
        """Set the dimensions of the field/court."""
        pass

    def draw(self, ax=None):
        if ax is None:
            fig, self.ax = plt.subplots(figsize=self.figsize)
        else:
            self.ax = ax
        self._draw_field()
        self._set_field_dimensions()
        self.ax.set_aspect("equal")  # Ensure the aspect ratio is equal
        return self.ax.figure, self.ax

    @abstractmethod
    def scatter(self, x, y, **kwargs):
        """Plot scatter points on the field/court."""
        pass

    @abstractmethod
    def heatmap(self, x, y, **kwargs):
        """Plot a heatmap on the field/court."""
        pass
