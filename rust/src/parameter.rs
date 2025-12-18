use pyo3::prelude::*;
use pyo3::{pymethods};
use crate::vector3::Vec3; 

const GRAVITY:f64 = 9.81;
#[pyclass]
#[derive(Debug, Copy,Clone)]
pub struct MagnusParameter{
    pub(crate) initial_velocity:f64,
    pub(crate) azimuth_angle: f64,
    pub(crate) elevation_angle: f64,
    pub(crate) spin_rate: f64,
    pub(crate) is_top_spin:bool,
    pub(crate) drag_coefficient:f64,
    pub(crate) lift_coefficient:f64,
    pub(crate) air_density: f64,
    pub(crate)time_step: f64,
    pub(crate) duration: f64
}





#[pymethods]
impl MagnusParameter{   
    #[new]
    fn new(
    initial_velocity:f64,
    elevation_angle: f64,
    azimuth_angle: f64,
    drag_coefficient:f64,
    lift_coefficient:f64,
    spin_rate: f64,
    is_top_spin:bool,
    air_density: f64,
    time_step: f64,
    duration: f64) -> PyResult<Self>{

        Ok(Self {
            initial_velocity,
            elevation_angle,
            azimuth_angle,
            drag_coefficient,
            lift_coefficient,
            spin_rate,
            is_top_spin,
            air_density,
            time_step,
            duration
        })
    }

      fn initial_forces(&self, spin_vector:Vec3, mass:f64) -> (Vec3, Vec3,Vec3){
        let vx:f64 = self.initial_velocity*self.elevation_angle.cos()*self.azimuth_angle.cos();
        let vy:f64 = self.initial_velocity*self.elevation_angle.sin();
        let vz:f64 = self.initial_velocity*self.elevation_angle.cos()*self.azimuth_angle.sin();
        
        let v = Vec3::new(vx,vy,vz);
        let mag_v = v.magnitude();

        let magnus_force = self.lift_coefficient*(spin_vector.cross(&v));
        let drag_force = -self.drag_coefficient* mag_v*v;

        let gravitational_force = Vec3::new(0.0,-mass*GRAVITY,0.0);

        (magnus_force, drag_force, gravitational_force)

    }
  }
