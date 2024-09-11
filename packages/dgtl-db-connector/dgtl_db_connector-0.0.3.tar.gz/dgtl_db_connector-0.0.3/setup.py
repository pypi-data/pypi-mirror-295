from pathlib import Path

from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="dgtl_db_connector",
    version="0.0.3",
    description="AWS DynamoDB python wrapper with backward compatibility",
    author="Olivier Witteman",
    license="MIT",
    packages=["dgtl_db_connector"],
    install_requires=["boto3",
                      "pandas"],
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
    ]
)

