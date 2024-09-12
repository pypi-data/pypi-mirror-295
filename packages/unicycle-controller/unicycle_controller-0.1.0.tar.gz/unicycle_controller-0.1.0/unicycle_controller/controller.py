import jax
import jax.numpy as jnp
import functools

class UnicycleController:
    def __init__(self, layer_sizes, v_max=7, omega_max=jnp.pi):
        self.layer_sizes = layer_sizes
        self.v_max = v_max
        self.omega_max = omega_max
        self.params = self.init_network_params(layer_sizes, jax.random.PRNGKey(0))

    def init_network_params(self, layer_sizes, rng_key):
        params = []
        for i in range(1, len(layer_sizes)):
            in_dim, out_dim = layer_sizes[i-1], layer_sizes[i]
            key, rng_key = jax.random.split(rng_key)
            bound = jnp.sqrt(6.0 / (in_dim + out_dim))
            weights = jax.random.uniform(key, (in_dim, out_dim), minval=-bound, maxval=bound)
            biases = jnp.zeros(out_dim)
            params.append((weights, biases))
        return params

    def __call__(self, inputs, params=None):
        if params is None:
            params = self.params
        return self.relu_nn(params, inputs)

    @functools.partial(jax.jit, static_argnums=(0,))
    def relu_nn(self, params, inputs):
        for W, b in params[:-1]:
            outputs = jnp.dot(inputs, W) + b
            inputs = jnp.maximum(outputs, 0)
        Wout, bout = params[-1]
        outputs = jnp.dot(inputs, Wout) + bout

        v = jnp.clip(outputs[0], -self.v_max, self.v_max)
        omega = jnp.clip(outputs[1], -self.omega_max, self.omega_max)

        return jnp.array([v, omega])