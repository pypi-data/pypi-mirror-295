from finres_ggpt2_matplotlib.theme import set_poppins_theme

# Apply the custom Poppins theme
set_poppins_theme()


set_poppins_theme(
    title_size=18,        # Custom title size
    label_size=14,        # Custom label size
    bold_title=True,      # Bold titles
    bold_labels=False,    # Non-bold axis labels
    show_grid=True        # Show grid lines
)
# Now create your plots
import matplotlib.pyplot as plt
x = [1, 2, 3, 4, 5]
y = [10, 15, 13, 17, 18]
plt.plot(x, y)
plt.title("Sample Poppins Plot")
plt.show()


import matplotlib.pyplot as plt
import numpy as np


plt.rcdefaults()

categories = ['Category A', 'Category B', 'Category C', 'Category D']
x = np.linspace(0, 10, 100)  # Shared x-axis for all plots
data = {category: np.sin(x + i) for i, category in enumerate(categories)}  # Different sine waves for each category

# Create a figure and axes for the faceted plot (2 rows, 2 columns)
fig, axes = plt.subplots(2, 2, figsize=(10, 8))  # Create a 2x2 grid of subplots
axes = axes.flatten()  # Flatten axes for easy iteration

# Iterate through each axis and plot the corresponding data
for ax, (category, y) in zip(axes, data.items()):
    ax.plot(x, y, label=category, color=np.random.rand(3,))
    ax.set_title(f"Facet: {category}", fontsize=12, weight='bold')  # Set the title for each facet
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.legend()

# Adjust layout for better spacing
plt.tight_layout()

# Show the faceted plot
plt.show()
