use pyo3::pyclass;

use crate::parameter::MagnusParameter;
use crate::vector3::Vec3;

const GRAVITY:f64 = 9.81;

#[derive(Clone,Copy,Debug)]
pub struct PresentState{
    pub(crate) position : Vec3,
    pub(crate) velocity: Vec3
}

impl PresentState{
    fn new(position:Vec3, velocity:Vec3) -> Self{
        Self{
            position,
            velocity
        }
    }
}

#[derive(Clone,Copy,Debug)]
struct DerivativeState{
     velocity: Vec3,
     acceleration: Vec3
}

impl DerivativeState{
    fn new(velocity: Vec3, acceleration:Vec3) -> Self{
        DerivativeState{
            velocity,
            acceleration
        }
    }
}

#[pyclass]
#[derive(Clone, Copy)]
pub struct ForceData {
    #[pyo3(get)]
    pub magnus: Vec3,
    #[pyo3(get)]
    pub drag: Vec3,
    #[pyo3(get)]
    pub gravity: Vec3,
    #[pyo3(get)]
    pub total: Vec3,
}

#[derive(Clone, Copy, Debug)]
pub struct TrajectoryPoint {
    pub time: f64,
    pub position: Vec3,
    pub velocity: Vec3,
    pub acceleration: Vec3,
    pub forces: Forces,
}

#[derive(Clone, Copy, Debug)]
pub struct Forces {
    pub magnus: Vec3,
    pub drag: Vec3,
    pub gravity: Vec3,
    pub total: Vec3,
}

impl Forces {
    pub fn new(magnus: Vec3, drag: Vec3, gravity: Vec3) -> Self {
        let total = magnus + drag + gravity;
        Self { magnus, drag, gravity, total }
    }
}

pub struct RK4Integrator{
    params: MagnusParameter,
    mass: f64,
    spin_vector: Vec3
}

impl RK4Integrator{
    pub fn new(params:MagnusParameter, mass:f64, spin_vector:Vec3) -> Self{
        Self{
            params,
            mass,
            spin_vector
        }
    }

    fn calculate_forces_and_acceleration(&self, velocity: Vec3) -> (Forces, Vec3) {
        let speed = velocity.magnitude();
        
        if speed < 1e-10 {
            let gravity = Vec3::new(0.0, -self.mass * GRAVITY, 0.0);
            let forces = Forces::new(Vec3::new(0.0, 0.0, 0.0), Vec3::new(0.0, 0.0, 0.0), gravity);
            return (forces, Vec3::new(0.0, -GRAVITY, 0.0));
        }

        let magnus_force = self.params.lift_coefficient * (self.spin_vector.cross(&velocity));
        let drag_force = -self.params.drag_coefficient * speed * velocity;
        let grav_force = Vec3::new(0.0, -self.mass * GRAVITY, 0.0);
        
        let forces = Forces::new(magnus_force, drag_force, grav_force);
        let acceleration = forces.total * (1.0 / self.mass);
        
        (forces, acceleration)
    }

    fn slope_now(&self, state:&PresentState) -> DerivativeState{
        let (_,acceleration) = self.calculate_forces_and_acceleration(state.velocity);
        DerivativeState::new(state.velocity, acceleration)
    }

    fn slope_future(&self, present_state:&PresentState,derivative_state:&DerivativeState, dt: f64) -> DerivativeState{
        //Updating position and velocity after each slope obtained
       let updated_present_state = PresentState{
        position: present_state.position + derivative_state.velocity*dt,
        velocity: present_state.velocity + derivative_state.acceleration*dt,
       };
       self.slope_now(&updated_present_state)
    }

    fn advance_single_step(&self, current_state:&PresentState,dt:f64) -> PresentState{

         let k1 = self.slope_now(&current_state);
         let k2 = self.slope_future(&current_state, &k1, dt*0.5);
         let k3 = self.slope_future(&current_state,&k2, dt*0.5);
         let k4 = self.slope_future(&current_state,&k3, dt);

         let position_change = (k1.velocity + 2.0*(k2.velocity+k3.velocity) + k4.velocity) * (dt/6.0);
         let velocity_change = (k1.acceleration + 2.0*(k2.acceleration+k3.acceleration) + k4.acceleration) * (dt/6.0);
         PresentState{
            position : current_state.position+ position_change,
            velocity : current_state.velocity + velocity_change
         }
      
    }

        pub fn simulate_points(&self, duration: f64, dt: f64) -> Vec<TrajectoryPoint> {
        let num_steps = (duration / dt).ceil() as usize;
        let mut trajectory:Vec<TrajectoryPoint> = Vec::with_capacity(num_steps + 1);
        
        // Initial state


        let vx = self.params.initial_velocity 
            * self.params.elevation_angle.cos() 
            * self.params.azimuth_angle.cos();
        let vy = self.params.initial_velocity * self.params.elevation_angle.sin();
        let vz = self.params.initial_velocity 
            * self.params.elevation_angle.cos() 
            * self.params.azimuth_angle.sin();
        
        let mut state = PresentState::new(
            Vec3::new(0.0, 0.0, 0.0),
            Vec3::new(vx, vy, vz),
        );
        let (forces,acceleration) = self.calculate_forces_and_acceleration(state.velocity);
        
            trajectory.push(TrajectoryPoint {
            time: 0.0,
            position: state.position,
            velocity: state.velocity,
            acceleration,
            forces,
        });
        
   for i in 0..num_steps {
        state = self.advance_single_step(&state, dt);
        let (forces, acceleration) = self.calculate_forces_and_acceleration(state.velocity);

        // Stop simulation if projectile hits the ground
        if state.position.y <= 0.0 && i > 0 {
            // Clamp y to 0 for the last point
            state.position.y = 0.0;
            trajectory.push(TrajectoryPoint {
                time: (i + 1) as f64 * dt,
                position: state.position,
                velocity: state.velocity,
                acceleration,
                forces,
            });
            break;
        }

        trajectory.push(TrajectoryPoint {
            time: (i + 1) as f64 * dt,
            position: state.position,
            velocity: state.velocity,
            acceleration,
            forces,
        });
    }
        
        trajectory
    }
}

