# config.py

# Input limits
INPUT_LIMITS = {
    "initial_velocity": {
        "minimum": 0,
        "maximum": 200,
        "parameter": "Initial Velocity",
        "unit": "m/s",
    },
    "radius": {
        "minimum": 0.01,
        "maximum": 0.15,
        "parameter": "Radius",
        "unit": "m",
    },
    "elevation_angle": {
        "minimum": 0,
        "maximum": 90,
        "parameter": "Elevation Angle",
        "unit": "°",
    },
    "azimuth_angle": {
        "minimum": -90,
        "maximum": 90,
        "parameter": "Azimuth Angle",
        "unit": "°",
    },
    "drag_coefficient": {
        "minimum": 0,
        "maximum": 2,
        "parameter": "Drag Coefficient",
        "unit": "",
    },
    "lift_coefficient": {
        "minimum": 0,
        "maximum": 2,
        "parameter": "Lift Coefficient",
        "unit": "",
    },
    "air_density": {
        "minimum": 0,
        "maximum": 2,
        "parameter": "Air Density",
        "unit": "kg/m³",
    },
    "spin_rate": {
        "minimum": -5000,
        "maximum": 5000,
        "parameter": "Spin Rate",
        "unit": "rpm",
    },
    "top_spin": {
        "minimum": 0,
        "maximum": 1,
        "parameter": "Top Spin",
        "unit": "",
    },
    "side_spin": {
        "minimum": 0,
        "maximum": 1,
        "parameter": "Side Spin",
        "unit": "",
    },
    "time_step": {
        "minimum": 0.001,
        "maximum": 1,
        "parameter": "Time Step",
        "unit": "s",
    },
    "duration": {
        "minimum": 5,
        "maximum": 30,
        "parameter": "Duration",
        "unit": "s",
    },
}

INPUT_PARAMETERS = {
    "Initial Parameters": {
        "Initial Velocity(m/s)": "initial_velocity",
        "Elevation Angle(°)": "elevation_angle",
        "Azimuth Angle(°)": "azimuth_angle",
        "Radius(m)": "radius",
    },
    "Environment Variables": {
        "Drag Coefficient": "drag_coefficient",
        "Lift Coefficient": "lift_coefficient",
        "Air Density(kg/m³)": "air_density",
    },
    "Spin Parameters": {
        "Spin Rate(rpm)": "spin_rate",
        "Top Spin": "top_spin",
        "Side Spin": "side_spin",
    },
    "Simulation Settings": {
        "Time Step(s)": "time_step",
        "Duration(s)": "duration",
    },
}
PLOT_CONFIG = [
    # Trajectory group
    [
        {
            "title": "Trajectory Plot",
            "x_label": "X(m)",
            "y_label": "Z(m)",
            "z_label": "Y(m)",
        }
    ],
    # Velocity group
    [
        {
            "title": "V${_x}$(m/s) v/s Time(s)",
            "x_label": "Time(s)",
            "y_label": "V${_x}$(m/s)",
            "z_label": "",
        },
        {
            "title": "V${_y}$(m/s) v/s Time(s)",
            "x_label": "Time(s)",
            "y_label": "V${_y}$(m/s)",
            "z_label": "",
        },
        {
            "title": "V${_z}$(m/s) v/s Time(s)",
            "x_label": "Time(s)",
            "y_label": "V${_z}$(m/s)",
            "z_label": "",
        },
    ],
    # Acceleration group
    [
        {
            "title": "A${_x}$(m/s²) v/s Time(s)",
            "x_label": "Time(s)",
            "y_label": "A${_x}$(m/s²)",
            "z_label": "",
        },
        {
            "title": "A${_y}$(m/s²) v/s Time(s)",
            "x_label": "Time(s)",
            "y_label": "A${_y}$(m/s²)",
            "z_label": "",
        },
        {
            "title": "A${_z}$(m/s²) v/s Time(s)",
            "x_label": "Time(s)",
            "y_label": "A${_z}$(m/s²)",
            "z_label": "",
        },
    ],
    # Force group
    [
        {
            "title": "F${_x}$(N) v/s Time(s)",
            "x_label": "Time(s)",
            "y_label": "F${_x}$(N)",
            "z_label": "",
        },
        {
            "title": "F${_y}$(N) v/s Time(s)",
            "x_label": "Time(s)",
            "y_label": "F${_y}$(N)",
            "z_label": "",
        },
        {
            "title": "F${_z}$(N) v/s Time(s)",
            "x_label": "Time(s)",
            "y_label": "F${_z}$(N)",
            "z_label": "",
        },
    ],
    # Animation group
    [
        {
            "title": "Animation Plot",
            "x_label": "X-Axis",
            "y_label": "Z-Axis",
            "z_label": "Y-Axis",
        }
    ],
]
LINE_COLORS = {
    "trajectory": "#2563EB",  # blue
    "velocity": "#16A34A",  # green
    "acceleration": "#F59E0B",  # amber
    "force": "#DC2626",  # red
    "animation": "#7C3AED",  # violet
}
PLOT_TEXT_COLORS = {
    "title": "#0F172A",  # very dark navy instead of black
    "label": "#1E3A8A",  # dark blue for a subtle theme accent
    "ticks": "#4F46E5",  # mid-blue for tick labels
    "grid": "#CBD5E1",  # light blue-gray grid
}

PLOT_FONT_SIZES = {
    "title": 14,
    "label": 11,
    "ticks": 10,
}
PLOT_MARGIN_MIN = 0.98
PLOT_MARGIN_MAX = 1.1

SAVE_PLOT_NAMES = {
    "trajectory_plot": "trajectory_figure",
    "velocity_plot": "velocity_figure",
    "acceleration_plot": "acceleration_figure",
    "force_plot": "force_figure",
    "animation_plot": "animation_figure",
}
data_map = {
    # Time
    "times": "time",
    # Position
    "x_positions": "position",
    "y_positions": "position",
    "z_positions": "position",
    # Velocity
    "x_velocity": "velocity",
    "y_velocity": "velocity",
    "z_velocity": "velocity",
    # Acceleration
    "x_acceleration": "acceleration",
    "y_acceleration": "acceleration",
    "z_acceleration": "acceleration",
    # Forces
    "x_magnus_force": "magnus_force",
    "y_magnus_force": "magnus_force",
    "z_magnus_force": "magnus_force",
    "x_drag_force": "drag_force",
    "y_drag_force": "drag_force",
    "z_drag_force": "drag_force",
    "x_total_force": "total_force",
    "y_total_force": "total_force",
    "z_total_force": "total_force",
}
