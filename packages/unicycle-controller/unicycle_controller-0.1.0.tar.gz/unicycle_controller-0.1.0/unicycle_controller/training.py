import jax
import jax.numpy as jnp
import optax
import functools
from .visualization import plot_multistep_samples_and_bounds, plot_loss_history
from jax_verify import IntervalBound
import jax_verify

def compute_multistep_reachable_set(initial_state_range, step_fn, params, num_steps):
    initial_state_bounds = IntervalBound(initial_state_range[:, 0], initial_state_range[:, 1])
    state_bounds = initial_state_bounds
    state_ranges = []

    for _ in range(num_steps):
        next_state_bounds = jax_verify.backward_crown_bound_propagation(functools.partial(step_fn, params=params), state_bounds)
        state_ranges.append(next_state_bounds)
        state_bounds = next_state_bounds

    return state_ranges

def loss_multi_step_reachable_set_volume(reachable_sets):
    volumes = [jnp.prod(set_.upper[:2] - set_.lower[:2]) for set_ in reachable_sets]
    return jnp.sum(jnp.array(volumes))

def loss_reach_avoid(controller_params, initial_state_bounds, cost_map, num_steps, step_fn, goal_zone, danger_zones):
    reachable_set = compute_multistep_reachable_set(
        initial_state_bounds,
        functools.partial(step_fn),
        controller_params,
        num_steps
    )

    loss_value = 0.0
    volume_loss = loss_multi_step_reachable_set_volume(reachable_set)

    goal_center = jnp.array([goal_zone[1], goal_zone[0]])
    danger_centers = jnp.array(danger_zones)

    for state_bounds in reachable_set:
        state_center = (state_bounds.upper + state_bounds.lower) / 2
        distance_to_goal = jnp.linalg.norm(state_center[:2] - goal_center)

        overlap_area_danger = 0.0
        for danger_center in danger_centers:
            overlap_lower = jnp.maximum(state_bounds.lower[:2], danger_center - 0.5)
            overlap_upper = jnp.minimum(state_bounds.upper[:2], danger_center + 0.5)
            overlap_width = jnp.maximum(overlap_upper - overlap_lower, 0)
            overlap_area_danger += jnp.prod(overlap_width)

        overlap_lower_goal = jnp.maximum(state_bounds.lower[:2], goal_center - 0.5)
        overlap_upper_goal = jnp.minimum(state_bounds.upper[:2], goal_center + 0.5)
        overlap_width_goal = jnp.maximum(overlap_upper_goal - overlap_lower_goal, 0)
        overlap_area_goal = jnp.prod(overlap_width_goal)

        step_loss = 10.0 * distance_to_goal + 15.0 * overlap_area_danger - 25.0 * overlap_area_goal
        loss_value += step_loss

    return loss_value + volume_loss

def train_controller(controller, dynamics_model, initial_state_range, cost_map, num_epochs, num_steps, goal_zone, danger_zones, learning_rate=0.0001, patience=100, threshold=1e-7):
    optimizer = optax.adam(learning_rate)
    opt_state = optimizer.init(controller.params)
    best_loss = float('inf')
    best_params = controller.params
    epochs_without_improvement = 0
    loss_history = []

    def step_fn(state, params):
        control = controller(state, params)
        return dynamics_model.dynamics_step(state, control)

    @jax.jit
    def train_step(params, opt_state):
        loss_value, grads = jax.value_and_grad(loss_reach_avoid)(
            params, initial_state_range, cost_map, num_steps, step_fn, goal_zone, jnp.array(danger_zones)
        )
        updates, opt_state = optimizer.update(grads, opt_state)
        params = optax.apply_updates(params, updates)
        return params, opt_state, loss_value

    for epoch in range(num_epochs):
        controller.params, opt_state, loss_value = train_step(controller.params, opt_state)
        loss_history.append(loss_value)

        if epoch % 100 == 0:
            print(f"Epoch {epoch}, Loss: {loss_value}")

        if loss_value < best_loss:
            best_loss = loss_value
            best_params = controller.params
            epochs_without_improvement = 0
        else:
            epochs_without_improvement += 1

        if epochs_without_improvement >= patience:
            if best_loss - loss_value < threshold:
                print(f"Loss plateaued. Stopping training at epoch {epoch}.")
                break

    controller.params = best_params
    
    # Plot final state
    output_ranges = compute_multistep_reachable_set(
        initial_state_range,
        lambda state, params: dynamics_model.dynamics_step(state, controller(state, params)),
        controller.params,
        num_steps
    )
    plot_multistep_samples_and_bounds(
        initial_state_range,
        lambda x: dynamics_model.dynamics_step(x, controller(x, controller.params)),
        num_steps,
        cost_map,
        bounds_list=output_ranges,
        title="Final Reachable Sets with Cost Map"
    )
    
    # Plot loss history
    plot_loss_history(loss_history)
    return controller, loss_history