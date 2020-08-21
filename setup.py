from setuptools import setup

setup(name="ssget",
      version="1.0",
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
      python_requires='>3.5.2',
      install_requires=['requests>2.22', 'tqdm>4.48']
)
