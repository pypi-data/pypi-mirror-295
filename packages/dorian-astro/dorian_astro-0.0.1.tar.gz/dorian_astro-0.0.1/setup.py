from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="dorian-astro",
    version="0.0.1",
    description="Code to generate full-sky ray-traced weak gravitational lensing maps from cosmological simulations.",
    package_dir={"dorian": "dorian"},
    packages=['dorian'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.mpcdf.mpg.de/fferlito/dorian",
    author="Fulvio Ferlito",
    author_email="fulvioferlito@gmail.com",
    license="GPLv3",
    install_requires=[
          'numpy',
          'scipy',
          'healpy',
          'h5py',
          'ducc0',
      ],
    python_requires=">=3.8",
)