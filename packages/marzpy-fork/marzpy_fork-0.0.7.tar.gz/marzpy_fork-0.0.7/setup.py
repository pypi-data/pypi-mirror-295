from setuptools import setup, find_packages

with open("README.md", "r") as file:
    readme = file.read()

setup(
    name="marzpy-fork", 
    version="0.0.7",
    author="Mewhrzad",
    description="A fork of the original Marzpy library to manage Marzban panel",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/vsskx/marzpy",
    keywords=["marzpy", "Marzban", "Gozargah", "Marzban python", "Marzban API"],
    packages=find_packages(),
    install_requires=["aiohttp"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
