from setuptools import find_packages, setup

setup(
  name="nb_sdk_test_v1",
  version="0.1.12",
  packages=find_packages(),
  install_requires=[
    # List your package dependencies here
  ],
  author='Neural Bridge',
  description="test",
  license="Apache License 2.0",
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
  ],
  python_requires=">=3.9",
)
