import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import pickle

connections = {
    'head': [
        (0, 3), (3, 2), (1, 3), (0, 1),
        (0, 2)
    ],
    'arms': [(4, 6), (4, 5)],
    'body': [(3, 4), (4, 7)],
    'legs': [(7, 10), (7, 8), (7, 9)]
}

# Create a custom colormap from light red to dark red
colors = [(1, 0.8, 0.8), (0.8, 0.2, 0.2), (0.5, 0, 0)]  # Light red, medium red, and dark red
n_bins = 100  # Number of bins for the color map
cmap_name = 'custom_red'
cm_custom_red = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)



def plot_syllables(syllable_dict: dict):
    num_syllables = len(syllable_dict.keys())

    # get parameters for plotting
    rows = (num_syllables + 4) // 5 # 5 subplots for each row
    fig, axs = plt.subplots(rows, 5, figsize=(20, 4*rows), squeeze=False)

    for idx, (ax, (syllable, entries)) in enumerate(zip(axs.flat, syllable_dict.items())):

        data = entries[0]  # First entry for the syllable
        colors = cm_custom_red(np.linspace(0, 1, data.shape[0]))

        # Plot full skeletons for the first, 10th, and last frames
        important_frames = [0, 9, data.shape[0] - 1]
        labels = ['Start Movement', 'Half of Movement', 'End of Movement']

        for frame_index, label in zip(important_frames, labels):
            frame = data[frame_index]
            color = colors[frame_index]

            # Plot the points
            ax.scatter(frame[:, 0], frame[:, 1], color=color, alpha=0.7, s=50, label=label if idx == 0 else "")

            # Annotate the points with their indices
            for i, (x, y) in enumerate(frame):
                ax.text(x, y, str(i), fontsize=12, ha='right', color=color)

            # Plot the skeleton connections
            for part, conns in connections.items():
                for connection in conns:
                    point1 = frame[connection[0]]
                    point2 = frame[connection[1]]
                    ax.plot([point1[0], point2[0]], [point1[1], point2[1]], color=color, alpha=0.7)

        # Draw trajectories for each point
        for i in range(data.shape[1]):
            ax.plot(data[:, i, 0], data[:, i, 1], 'k--', alpha=0.3,
                    linewidth=0.5)  # Thinner, dimmer dashed lines for trajectories

        ax.set_title(f'{syllable}')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')

        # Add a single legend
    handles, labels = axs[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper right')

    # Adjust layout
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    plt.suptitle('Mouse Skeleton Movement for Each Syllable', y=1.02)
    plt.gca().set_aspect('equal')
    plt.show()
