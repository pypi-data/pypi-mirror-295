from setuptools import setup, find_packages

setup(
    name="sharehousepy",
    version="0.1.1",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "snowflake-connector-python",
        "python-dotenv",
        "tqdm",
        "yaspin",
        "shapely",
        "python-geohash",
        ""
    ],
    author="Worthy Rae",
    author_email="worthyr@anomalysix.com",
    description="A python library to create and execute sharehouse queries",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/sharehousepy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    include_package_data=True,
    package_data={
        "": ["data/*.csv"],
    },
)