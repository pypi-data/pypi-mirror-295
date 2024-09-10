# Matplotlib Poppins Theme (Inspired by ggplot)

This package provides a custom theme for **Matplotlib**, inspired by the visual style of **ggplot**, using the **Poppins** font for a clean and modern look. 

## Features

- Custom Matplotlib theme with the Poppins font.
- Configurable options for title size, label size, boldness, and grid display.
- Inspired by ggplot2's elegant styling.

## Installation

You can install this package via pip:

```bash
pip install finres_ggpt2_matplotlib
```

## Usage
```python
import finres_ggpt2_matplotlib

# Apply the custom Poppins theme
finres_ggpt2_matplotlib.set_poppins_theme()

# Now create your plots
import matplotlib.pyplot as plt
x = [1, 2, 3, 4, 5]
y = [10, 15, 13, 17, 18]
plt.plot(x, y)
plt.title("Sample Poppins Plot")
plt.show()

```

### Customization Options

You can customize the theme by passing different options to set_poppins_theme():

```python
# Apply the Poppins theme with custom options
matplotlib_poppins_theme.set_poppins_theme(
    title_size=18,        # Custom title size
    label_size=14,        # Custom label size
    bold_title=True,      # Bold titles
    bold_labels=False,    # Non-bold axis labels
    show_grid=True        # Show grid lines
)




import matplotlib.pyplot as plt
import numpy as np

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

```
with the theme
![Faceted Plot](./Figure_1.png)

![Faceted Plot](./Figure_1.png)


### Autre example
```python
# Example plot using the custom theme
theme.set_finres_ggpt_theme(vc_fontname="Poppins", 
                            vc_cols="black", 
                            vc_colbg_plot="white", 
                            vc_colbg="#EFEFEF", 
                            title_size=18, 
                            label_size=12, 
                            tick_size=12)

# Sample plot
fig, ax = plt.subplots()

# Data for plotting
ax.plot([0, 1, 2], [0, 1, 4], label="Example Data")
ax.set_title("Example Plot Title")
ax.set_xlabel("X Axis Label")
ax.set_ylabel("Y Axis Label")

# Place the legend outside the plot (right center)
ax.legend(title="Legend Title", loc="center left", bbox_to_anchor=(1, 0.5), frameon=True)

# Adjust layout to make room for the legend
plt.subplots_adjust(right=0.75)

# Show plot
plt.show()
```

### Parameters:
- `title_size`: Sets the font size for the plot title (default is 14).
- `label_size`: Sets the font size for the axis labels (default is 12).
- `bold_title`: Boolean to specify if the title should be bold (default is `True`).
- `bold_labels`: Boolean to specify if the axis labels should be bold (default is `True`).
- `show_grid`: Boolean to specify if the grid should be shown (default is `False`).

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue on GitHub.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

