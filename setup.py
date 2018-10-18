import setuptools

with open("README.md", "r") as fh:
long_description = fh.read()

setuptools.setup(
  name="rallf",
  version="0.0.1",
  author="Lluis Santos",
  author_email="author@example.com",
  description="A small example package",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/robotunion/rallf-py-sdk",
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
)
