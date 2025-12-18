#![allow(dead_code)]
#![allow(unused_variables)]

use pyo3::prelude::*;

pub mod vector3;
pub mod parameter;
pub mod integrator;
use parameter::MagnusParameter;
use vector3::Vec3;
use integrator::{RK4Integrator};

use crate::integrator::ForceData;

#[pymodule]
fn magnus_simulation(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<MagnusParameter>()?;
    m.add_class::<Vec3>()?;
    m.add_class::<DetailedTrajectoryPoint>()?;
    m.add_function(wrap_pyfunction!(simulate_trajectory, m)?)?;
    Ok(())
}

#[pyclass]
#[derive(Clone)]
pub struct DetailedTrajectoryPoint {
    #[pyo3(get)]
    pub time: f64,
    #[pyo3(get)]
    pub position: Vec3,
    #[pyo3(get)]
    pub velocity: Vec3,
    #[pyo3(get)]
    pub acceleration: Vec3,
    #[pyo3(get)]
    pub forces: ForceData
}

#[pyfunction]
fn simulate_trajectory(
    params: MagnusParameter,
    mass: f64,
    spin_vector: Vec3,
) -> PyResult<Vec<DetailedTrajectoryPoint>> {
    let dt = params.time_step;
    let duration = params.duration;
    
    let integrator = RK4Integrator::new(params, mass, spin_vector);
    let trajectory = integrator.simulate_points(duration, dt);
    
    let results: Vec<DetailedTrajectoryPoint> = trajectory
        .iter()
        .map(|point| DetailedTrajectoryPoint {
            time: point.time,
            position: point.position,
            velocity: point.velocity,
            acceleration: point.acceleration,
            forces: {
                ForceData { magnus: point.forces.magnus,
                     drag: point.forces.drag,
                      gravity:point.forces.gravity,
                       total: point.forces.total }
            }
        })
        .collect();
    
    Ok(results)
}