from setuptools import setup, find_packages

setup(
    name="mplsports",
    version="0.1.0",
    description="Add your description here",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/mplsports",  # Update with your repository URL
    packages=find_packages(),
    install_requires=[
        "matplotlib>=3.7.5",
    ],
    python_requires=">=3.8",
)
