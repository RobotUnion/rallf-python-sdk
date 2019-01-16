import setuptools

setuptools.setup(
  name="rallf",
  version="0.4.1",
  author="Lluis Santos",
  author_email="lluis@rallf.com",
  license="MIT",
  description="rallf.com Software Development Kit (SDK)",
  long_description=open("README.md", "r").read(),
  long_description_content_type="text/markdown",
  url="https://github.com/robotunion/rallf-python-sdk",
  packages=setuptools.find_packages(),
  scripts=['bin/rallf-py'],
  classifiers=[
    "Development Status :: 2 - Pre-Alpha",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Intended Audience :: Developers",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
    "Topic :: Scientific/Engineering :: Artificial Life",
    "Topic :: Scientific/Engineering :: Image Recognition",
    "Topic :: Home Automation",
    "Topic :: Internet",
    "Topic :: Internet :: WWW/HTTP :: Browsers",
    "Topic :: Software Development",
    "Topic :: Software Development :: Build Tools",
    "Topic :: Software Development :: Libraries",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Software Development :: Quality Assurance",
    "Topic :: Software Development :: Testing",
    "Topic :: Software Development :: Testing :: Mocking",
    "Topic :: Software Development :: Testing :: Traffic Generation"
  ],
  install_requires=[pkg.strip() for pkg in open("requirements.txt").readlines() if len(pkg) > 1]
)
