import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

version = {}
with open("sdpchainpy/version.py") as fp:
    exec(fp.read(), version)

setuptools.setup(
    name="sdpchainpy",
    version=version['__version__'],
    author="Wayne Crawford",
    author_email="crawford@ipgp.fr",
    description="SDPCHAIN provenance system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WayneCrawford/sdpchainpy",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
          'progress>=1.5',
      ],
    entry_points={
         'console_scripts': [
             'sdpcat=sdpchainpy:sdpcat',
             'sdpstep=sdpchainpy:sdpstep',
         ]
    },
    python_requires='>=3.8',
    classifiers=(
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics"
    ),
    keywords='provencance, data, metadata'
)
