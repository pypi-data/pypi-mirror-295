from finres_ggpt2_matplotlib.theme import set_poppins_theme

# Apply the custom Poppins theme
set_poppins_theme()

# Now create your plots
import matplotlib.pyplot as plt
x = [1, 2, 3, 4, 5]
y = [10, 15, 13, 17, 18]
plt.plot(x, y)
plt.title("Sample Poppins Plot")
plt.show()