import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import jax.numpy as jnp
import jax

def plot_multistep_samples_and_bounds(initial_state_range, step_fn, num_steps, cost_map, bounds_list=None, title="Reachable Sets with Cost Map"):
    xt = np.random.uniform(low=initial_state_range[:, 0], high=initial_state_range[:, 1], size=(1000, 5))
    states = [xt]

    for _ in range(num_steps):
        xt1 = jax.vmap(step_fn)(xt)
        states.append(xt1)
        xt = xt1

    plt.figure(figsize=(12, 8))
    
    # Create a base cost map with all cells set to 1 (low cost)
    base_cost_map = np.ones_like(cost_map)
    
    # Plot the base cost map
    plt.imshow(base_cost_map, cmap='YlOrRd', origin='lower', extent=[0, cost_map.shape[1], 0, cost_map.shape[0]], vmin=0, vmax=10)
    
    # Plot individual obstacles
    for i in range(cost_map.shape[0]):
        for j in range(cost_map.shape[1]):
            if cost_map[i, j] == 10:  # Assuming 10 is the cost for obstacles
                plt.gca().add_patch(Rectangle((j, i), 1, 1, fill=True, facecolor='darkred', edgecolor='none'))

    plt.colorbar(label='Cost')

    for state in states:
        plt.plot(state[:, 0], state[:, 1], 'o', markersize=2)

    if bounds_list is not None:
        for bounds in bounds_list:
            lower = bounds.lower
            upper = bounds.upper
            rect = Rectangle((lower[0], lower[1]), upper[0] - lower[0], upper[1] - lower[1], fill=False, edgecolor='black', linewidth=1)
            plt.gca().add_patch(rect)

    goal_zone = np.unravel_index(np.argmin(cost_map), cost_map.shape)
    plt.text(goal_zone[1], goal_zone[0], 'G', ha='center', va='center', color='black', fontweight='bold')

    plt.title(title)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.show()

def plot_loss_history(loss_history):
    plt.figure(figsize=(10, 5))
    plt.plot(loss_history, label='Training Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.title('Training Loss Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()