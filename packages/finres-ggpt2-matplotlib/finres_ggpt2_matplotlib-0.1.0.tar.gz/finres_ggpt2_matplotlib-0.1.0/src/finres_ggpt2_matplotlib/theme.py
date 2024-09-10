import matplotlib.pyplot as plt
from matplotlib import font_manager
import pkg_resources
import os

def set_poppins_theme(title_size=14, label_size=12, bold_title=True, bold_labels=True, show_grid=False):
    """
    Applies a custom Matplotlib theme using the Poppins font with customizable size, boldness, and grid.

    Parameters:
    title_size (int): Font size for the plot title.
    label_size (int): Font size for the axis labels.
    bold_title (bool): Whether to make the title bold.
    bold_labels (bool): Whether to make the axis labels bold.
    show_grid (bool): Whether to display the grid on the plot.
    """

    # Get the absolute paths to the Poppins font inside the package
    regular_font_path = pkg_resources.resource_filename('finres_ggpt2_matplotlib', 'fonts/Poppins-Regular.ttf')
    bold_font_path = pkg_resources.resource_filename('finres_ggpt2_matplotlib', 'fonts/Poppins-Bold.ttf')

    print(f"Regular font path: {regular_font_path}")
    print(f"Bold font path: {bold_font_path}")

    # Check if the files actually exist at these paths
    if not os.path.exists(regular_font_path):
        print(f"Regular font not found at {regular_font_path}")
    if not os.path.exists(bold_font_path):
        print(f"Bold font not found at {bold_font_path}")


    # Add the Poppins fonts to matplotlib's font manager
    font_manager.fontManager.addfont(regular_font_path)
    font_manager.fontManager.addfont(bold_font_path)

    # Set the custom theme settings
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['Poppins'],
        'text.color': 'black',
        'axes.labelcolor': 'black',
        'xtick.color': 'black',
        'ytick.color': 'black',

        # Background and grid settings
        'axes.facecolor': 'white',
        'figure.facecolor': 'white',
        'axes.grid': show_grid,  # Show or hide grid based on the argument
        'grid.color': 'gray',  # Optional: Grid line color
        'grid.linestyle': '--',  # Optional: Grid line style
        
        # Title and axis label settings with bold or regular font
        'axes.titleweight': 'bold' if bold_title else 'normal',
        'axes.titlesize': title_size,
        'axes.labelsize': label_size,
        'axes.labelweight': 'bold' if bold_labels else 'normal',

        # Custom font paths based on boldness
        'font.weight': 'bold' if bold_labels else 'normal',

        # Set title font to bold if specified
        'axes.titleweight': 'bold' if bold_title else 'normal',
    })

    print(f"Poppins theme applied with title size {title_size}, label size {label_size}, "
          f"title bold: {bold_title}, labels bold: {bold_labels}, grid: {show_grid}.")
