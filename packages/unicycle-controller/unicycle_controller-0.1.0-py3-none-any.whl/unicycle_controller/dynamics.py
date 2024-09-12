import jax.numpy as jnp

class UnicycleModel:
    def __init__(self, delta_t=0.1):
        self.delta_t = delta_t

    def dynamics_step(self, xs, ut):
        x, y, theta, vold, omegaold = xs
        v, omega = ut

        theta_new = theta + omega * self.delta_t
        x_new = x + v * jnp.cos(theta) * self.delta_t
        y_new = y + v * jnp.sin(theta) * self.delta_t

        return jnp.array([x_new, y_new, theta_new, v, omega])