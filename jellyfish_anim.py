import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 1. Set up the ocean environment
fig, ax = plt.subplots(figsize=(6, 8))
fig.patch.set_facecolor('#050b14')  # Deep ocean background
ax.set_facecolor('#050b14')
ax.set_xlim(-4, 4)
ax.set_ylim(-8, 4)
ax.axis('off')  # Hide the grid and axes

# 2. Initialize the jellyfish structures
# The bell is a single line, tentacles are a list of lines
bell_line, = ax.plot([], [], color='#00ffff', lw=4, alpha=0.8)
num_tentacles = 7
tentacles = [ax.plot([], [], color='#00ffff', lw=1.5, alpha=0.5)[0] for _ in range(num_tentacles)]

def init():
    bell_line.set_data([], [])
    for t in tentacles:
        t.set_data([], [])
    return [bell_line] + tentacles

def animate(frame):
    t = frame * 0.1  # Global time variable
    
    # --- ANIMATE THE BELL ---
    # Pulse multiplier: creates the contraction and expansion swimming motion
    pulse = 1.0 + 0.15 * np.sin(2 * t)
    
    # Calculate half-ellipse coordinates for the bell
    theta = np.linspace(0, np.pi, 100)
    bell_x = 2 * pulse * np.cos(theta)
    bell_y = 1.5 * pulse * np.sin(theta)
    bell_line.set_data(bell_x, bell_y)
    
    # --- ANIMATE THE TENTACLES ---
    # Distribute the start points of tentacles evenly across the bottom of the bell
    bases_x = np.linspace(-1.8 * pulse, 1.8 * pulse, num_tentacles)
    
    for i, tentacle in enumerate(tentacles):
        y_vals = np.linspace(0, -7, 100)
        
        # Offset each tentacle's phase so they don't move in perfect sync
        phase_offset = i * 0.4
        
        # Amplitude increases as y goes deeper, creating a trailing whip effect
        amplitude = 0.05 + 0.08 * np.abs(y_vals)
        
        # x = start_pos + wave_motion
        x_vals = bases_x[i] + amplitude * np.sin(2.5 * y_vals - 3 * t + phase_offset)
        tentacle.set_data(x_vals, y_vals)
        
    return [bell_line] + tentacles

# 3. Render the animation
print("Calculating fluid dynamics and rendering frames...")
ani = animation.FuncAnimation(
    fig, animate, frames=120, init_func=init, blit=True, interval=50
)

# 4. Save to a file that can be previewed in the Codespace
output_file = 'jellyfish.gif'
ani.save(output_file, writer='pillow', fps=24)
print(f"Success! Open {output_file} in your file explorer to see the result.")