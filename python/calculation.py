import magnus_simulation as ms

import numpy as np


def run_magnus_simulation(magnus_data):
    print(magnus_data)
    # Create a Vec3 for spin vector
    spin_vector = ms.Vec3(
        0.0,
        magnus_data["side_spin"],
        magnus_data["top_spin"],
    )
    K_D = (
        (1 / 2)
        * (np.pi * magnus_data["radius"] ** 2)
        * magnus_data["air_density"]
        * magnus_data["drag_coefficient"]
    )
    K_L = (
        (1 / 2)
        * (np.pi * magnus_data["radius"] ** 2)
        * magnus_data["air_density"]
        * magnus_data["lift_coefficient"]
    )
    # print(f"K_D={K_D}\nK_L={K_L}")
    # Create Magnus parameters

    params = ms.MagnusParameter(
        initial_velocity=magnus_data["initial_velocity"],
        elevation_angle=np.radians(magnus_data["elevation_angle"]),
        azimuth_angle=np.radians(magnus_data["azimuth_angle"]),
        drag_coefficient=K_D,
        lift_coefficient=K_L,
        spin_rate=magnus_data["spin_rate"],
        is_top_spin=False,
        air_density=magnus_data["air_density"],
        time_step=magnus_data["time_step"],
        duration=magnus_data["duration"],
    )

    # Mass of the projectile
    MASS = 0.43
    GRAVITY = 9.81

    magnus_force, drag_force, grav_force = params.initial_forces(spin_vector, MASS)
    trajectory = ms.simulate_trajectory(params, MASS, spin_vector)

    # Extract position data for plotting
    times = [point.time for point in trajectory]
    x_positions = [point.position.x for point in trajectory]
    y_positions = [point.position.y for point in trajectory]
    z_positions = [point.position.z for point in trajectory]
    x_velocity = [point.velocity.x for point in trajectory]
    y_velocity = [point.velocity.y for point in trajectory]
    z_velocity = [point.velocity.z for point in trajectory]
    x_acceleration = [point.acceleration.x for point in trajectory]
    y_acceleration = [point.acceleration.y for point in trajectory]
    z_acceleration = [point.acceleration.z for point in trajectory]

    magnus_force_magnitude = [
        np.linalg.norm(
            [point.forces.magnus.x, point.forces.magnus.y, point.forces.magnus.z]
        )
        for point in trajectory
    ]

    drag_force_magnitude = [
        np.linalg.norm([point.forces.drag.x, point.forces.drag.y, point.forces.drag.z])
        for point in trajectory
    ]
    gravity_force = [MASS * GRAVITY for _ in magnus_force_magnitude]
    print(min(z_positions))
    print(max(z_positions))
    return {
        "t": times,
        "x": x_positions,
        "y": y_positions,
        "z": z_positions,
        "vx": x_velocity,
        "vy": y_velocity,
        "vz": z_velocity,
        "ax": x_acceleration,
        "ay": y_acceleration,
        "az": z_acceleration,
        "fx": drag_force_magnitude,
        "fy": gravity_force,
        "fz": magnus_force_magnitude,
    }
