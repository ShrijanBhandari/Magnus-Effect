import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from config import (
    PLOT_CONFIG,
    LINE_COLORS,
    PLOT_TEXT_COLORS,
    PLOT_FONT_SIZES,
    PLOT_MARGIN_MIN,
    PLOT_MARGIN_MAX,
)


def create_canvas(self):
    self.canvas = {
        "trajectory_canvas": ("trajectory_figure", "trajectory_axes", 1, 1),
        "velocity_canvas": ("velocity_figure", "velocity_axes", 1, 3),
        "acceleration_canvas": ("acceleration_figure", "acceleration_axes", 1, 3),
        "force_canvas": ("force_figure", "force_axes", 1, 3),
        "animation_canvas": ("animation_figure", "animation_axes", 1, 1),
    }
    plt.style.use("seaborn-v0_8-whitegrid")
    for canvas_name, (
        figure_name,
        axes_name,
        row,
        column,
    ) in self.canvas.items():
        if column == 1:
            figure, axes = plt.subplots(
                subplot_kw={"projection": "3d"}, constrained_layout=True
            )
        else:
            figure, axes = plt.subplots(
                row, column, figsize=(20, 10), constrained_layout=True
            )
        setattr(self, figure_name, figure)
        setattr(self, axes_name, axes)
        canvas = FigureCanvas(getattr(self, figure_name))
        setattr(self, canvas_name, canvas)


def reset_canvas(self):
    for canvas_name, value in self.canvas.items():
        axes_name = value[1]
        axes = getattr(self, axes_name)
        if not isinstance(axes, (list, np.ndarray)):
            axes = [axes]
        for ax in axes:
            for line in ax.get_lines():
                line.remove()
            ax.figure.canvas.draw()


def design_canvas(self):
    create_canvas(self)

    for (_, axes_name, _, column), plot_group in zip(self.canvas.values(), PLOT_CONFIG):
        axes = getattr(self, axes_name)
        if not isinstance(axes, (list, np.ndarray)):
            axes = [axes]
        for ax, plot_info in zip(axes, plot_group):
            if column == 1:
                ax.set_zlabel(
                    plot_info["z_label"],
                    color=PLOT_TEXT_COLORS["label"],
                    fontsize=PLOT_FONT_SIZES["label"],
                )
            ax.set_title(
                plot_info["title"],
                color=PLOT_TEXT_COLORS["title"],
                fontsize=PLOT_FONT_SIZES["title"],
            )
            ax.set_xlabel(
                plot_info["x_label"],
                color=PLOT_TEXT_COLORS["label"],
                fontsize=PLOT_FONT_SIZES["label"],
            )
            ax.set_ylabel(
                plot_info["y_label"],
                color=PLOT_TEXT_COLORS["label"],
                fontsize=PLOT_FONT_SIZES["label"],
            )
            ax.tick_params(
                axis="both",
                colors=PLOT_TEXT_COLORS["ticks"],
                labelsize=PLOT_FONT_SIZES["ticks"],
            )
            ax.grid(
                True,
                color=PLOT_TEXT_COLORS["grid"],
                linewidth=0.8,
            )


def plot_calculated_data(self):
    t = self.calculated_data["t"]

    self.canvas_values = [
        # Trajectory (3D)
        [
            (
                self.calculated_data["x"],
                self.calculated_data["z"],
                self.calculated_data["y"],
            )
        ],
        # Velocity vs Time (2D)
        [
            (t, self.calculated_data["vx"], ""),
            (t, self.calculated_data["vy"], ""),
            (t, self.calculated_data["vz"], ""),
        ],
        # Acceleration vs Time (2D)
        [
            (t, self.calculated_data["ax"], ""),
            (t, self.calculated_data["ay"], ""),
            (t, self.calculated_data["az"], ""),
        ],
        # Force vs Time (2D)
        [
            (t, self.calculated_data["fx"], ""),
            (t, self.calculated_data["fy"], ""),
            (t, self.calculated_data["fz"], ""),
        ],
        # Animation (3D)
        [
            (
                self.calculated_data["x"],
                self.calculated_data["z"],
                self.calculated_data["y"],
            )
        ],
    ]
    for (canvas_name, (_, axes_name, _, column)), canvas_value, line_color in zip(
        self.canvas.items(), self.canvas_values, LINE_COLORS.values()
    ):
        axes = getattr(self, axes_name)
        if not isinstance(axes, (list, np.ndarray)):
            axes = [axes]
        for ax, (x, y, z) in zip(axes, canvas_value):
            ax.set_xlim(min(x) * PLOT_MARGIN_MIN, max(x) * PLOT_MARGIN_MAX)
            ax.set_ylim(-10, 10)
            if column == 1:
                # ax.view_init(elev=90, azim=-90)  # top-down view
                # ax.set_box_aspect([1, 1, 1])
                ax.set_zlim(min(z) * PLOT_MARGIN_MIN, max(z) * PLOT_MARGIN_MAX)
                if canvas_name == "animation_canvas":
                    create_animation(self)
                    continue
                ax.plot(x, y, z, linewidth=2.2, color=line_color)
            else:
                ax.plot(x, y, linewidth=2.2, color=line_color)
        getattr(self, canvas_name).draw()


def update(self, frame, line, frame_skip):
    idx = frame_skip * frame
    line.set_data(self.calculated_data["x"][:idx], self.calculated_data["z"][:idx])
    line.set_3d_properties(self.calculated_data["y"][:idx])
    getattr(self, "animation_canvas").draw()
    return (line,)


def create_animation(self):
    frame_skip = 20

    frames = len(self.calculated_data["t"]) // frame_skip
    (animation_line,) = self.animation_axes.plot(
        [], [], [], color=LINE_COLORS["animation"], linewidth=2.2
    )
    self.animation = FuncAnimation(
        self.animation_figure,
        lambda f: update(self, f, animation_line, frame_skip),
        frames=frames,
        repeat=True,
        interval=20,
    )
