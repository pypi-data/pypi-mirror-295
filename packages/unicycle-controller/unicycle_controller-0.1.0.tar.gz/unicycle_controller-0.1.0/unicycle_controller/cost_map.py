import jax.numpy as jnp

def create_cost_map(grid_size, danger_zones, goal_zone):
    cost_map = jnp.ones((grid_size, grid_size))
    
    # Set high cost for danger zones
    for zone in danger_zones:
        cost_map = cost_map.at[zone].set(10)
    
    # Set low cost for goal zone
    cost_map = cost_map.at[goal_zone].set(0)
    
    return cost_map