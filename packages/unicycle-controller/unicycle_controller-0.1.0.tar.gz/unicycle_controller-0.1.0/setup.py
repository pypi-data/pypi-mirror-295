from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="unicycle_controller",
    version="0.1.0",
    author="Puja Chaudhury",
    author_email="catplotlib@gmail.com",
    description="A package for unicycle control and reachability analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/catplotlib/verified_control",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "jax",
        "jaxlib",
        "jax-verify",
        "optax",
        "matplotlib",
        "numpy"
    ],
)