import pathlib

from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="ssgetpy",
    version="1.0",
    description="A Python interface to the SparseSuite Matrix Collection",
    author="Sudarshan Raghunathan",
    author_email="darshan@alum.mit.edu",
    url="http://www.github.com/drdarshan/ssgetpy",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=["ssgetpy"],
    entry_points={"console_scripts": ["ssgetpy = ssgetpy.query:cli",],},
    python_requires=">3.5.2",
    install_requires=["requests>=2.22", "tqdm>=4.48"],
)
