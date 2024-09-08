from setuptools import setup, find_packages
import SBDL

NAME = "sbdletldemo"
DESCRIPTION = "Package of SBDL app"
LONG_DESCRIPTION = ""

ENTRY_POINTS = """
[console_scripts]
run-sbdl=SBDL.run_sbdl:from_databricks
run-sbdl2=SBDL.scripts.run_databricks:on_databricks
"""

with open("README.md") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name=NAME,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=SBDL.__author__,
    version=SBDL.__version__,
    author_email="akash967049@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points=ENTRY_POINTS,
    keywords=['python', 'etl', 'boiler', 'local', 'databricks']
)