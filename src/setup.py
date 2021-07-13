from setuptools import find_packages, setup

setup(
    name="mcollector",
    version="0.1.0",
    description="Measurements Collector",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["SQLAlchemy==1.4.20"],
    extras_require={"test": ["pytest==6.2.4", "pytest-asyncio==0.15.1"]},
)
