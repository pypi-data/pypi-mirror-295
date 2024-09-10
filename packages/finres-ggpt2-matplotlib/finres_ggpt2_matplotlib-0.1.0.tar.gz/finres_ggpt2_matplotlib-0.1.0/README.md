# Matplotlib Poppins Theme (Inspired by ggplot)

This package provides a custom theme for **Matplotlib**, inspired by the visual style of **ggplot**, using the **Poppins** font for a clean and modern look. 

## Features

- Custom Matplotlib theme with the Poppins font.
- Configurable options for title size, label size, boldness, and grid display.
- Inspired by ggplot2's elegant styling.

## Installation

You can install this package via pip:

```bash
pip install matplotlib-poppins-theme
```

## Usage
```python

import matplotlib_poppins_theme

# Apply the custom Poppins theme
matplotlib_poppins_theme.set_poppins_theme()

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

