"""
Komodo AI CLI
"""

from setuptools import find_packages, setup

from komo.version import __version__

with open("requirements.txt", "r") as f:
    dependencies = f.readlines()

setup(
    name="komo",
    version=__version__,
    url="https://github.com/komodoai/komo",
    license="BSD",
    author="Komodo AI",
    author_email="anish@komodo.io",
    description="Komodo AI CLI",
    long_description=__doc__,
    packages=find_packages(exclude=["tests", "komoproj.yaml"], include=["*"]),
    include_package_data=True,
    zip_safe=False,
    platforms="any",
    python_requires=">=3.8.0",
    install_requires=dependencies,
    entry_points={
        "console_scripts": [
            "komo = komo.cli.cli:cli",
        ],
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        "Development Status :: 4 - Beta",
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
