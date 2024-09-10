from setuptools import setup, find_packages

# Reading the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="finres_ggpt2_matplotlib",  # Your package name
    version="0.1.0",  # Version number of your package
    author="Your Name",  # Your name
    author_email="vhiny.mombo@finres.dev",  # Your email
    description="A custom Matplotlib theme using the Poppins font styled like ggplot.",  # Short description
    long_description=long_description,  # Detailed description from README.md
    long_description_content_type="text/markdown",  # Content type for the long description
    url="https://github.com/yourusername/finres_ggpt2_matplotlib",  # Your project’s URL
    packages=find_packages(where="src"),  # Automatically find packages in the "src" folder
    package_dir={"": "src"},  # Define the base directory for packages
    include_package_data=True,  # Include non-Python files (like fonts) specified in package_data
    package_data={
        'finres_ggpt2_matplotlib': ['fonts/*.ttf'],  # Include the font files from the fonts directory
    },
    classifiers=[
        "Programming Language :: Python :: 3",  # Your package is compatible with Python 3
        "License :: OSI Approved :: MIT License",  # Your package license (MIT)
        "Operating System :: OS Independent",  # The package works on any OS
        "Framework :: Matplotlib",  # Specifies the package works with Matplotlib
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ],
    python_requires='>=3.6',  # Specify the minimum Python version
    install_requires=[
        "matplotlib>=3.1.0",  # Install Matplotlib as a dependency
    ],
    extras_require={  # Optional: Define extra dependencies
        "dev": ["pytest>=6.0", "twine", "wheel"],  # Development requirements (for testing and publishing)
    },
    entry_points={  # Optional: Add entry points for command-line scripts
        'console_scripts': [
            'apply_poppins_theme = finres_ggpt2_matplotlib.theme:set_poppins_theme',
        ],
    },
    keywords="matplotlib theme poppins ggplot",  # Keywords for PyPI
    project_urls={  # Optional: Additional URLs
        "Bug Tracker": "https://github.com/yourusername/finres_ggpt2_matplotlib/issues",
        "Documentation": "https://github.com/yourusername/finres_ggpt2_matplotlib/wiki",
        "Source Code": "https://github.com/yourusername/finres_ggpt2_matplotlib",
    },
)
