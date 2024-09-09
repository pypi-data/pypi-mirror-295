from setuptools import setup, find_packages

setup(
    name="pyjoker",  # The name of your package
    version="0.1.0",  # Initial version
    description="A Python package for categorized one-liner jokes.",  # Short description
    long_description=open('README.md').read(),  # Pulls from your README
    long_description_content_type="text/markdown",  # Markdown format for the README
    author="Ashain Perera",  
    author_email="ashainperera95@gmail.com",  
    url="https://github.com/ashainp",  
    packages=find_packages(),  # Automatically find and include all packages
    include_package_data=True,  # Ensure non-Python files like CSV are included
    package_data={"pyjoker": ["jokes.csv"]},  # Specify that jokes.csv should be included
    install_requires=["pandas"],  # Package dependencies
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # <-- Reference the MIT license here
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Minimum Python version required
)
