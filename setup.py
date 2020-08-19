from setuptools import setup

setup(name="ssget",
      version="0.92",
      description="A Python interface to the SparseSuite Matrix Collection",
      author="Sudarshan Raghunathan",
      author_email="rdarshan@gmail.com",
      url="http://www.github.com/drdarshan/ssget",
      packages=["ssget"],
      entry_points={
        "console_scripts": [
            "ssget = ssget.query:cli",
        ],
      },
      install_requires=['tqdm']
)
