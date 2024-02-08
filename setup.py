from setuptools import setup, find_packages

setup(
    name='compute_anomaly',
    version='0.1.0',
    url="https://github.com/athulrs177/compute_anomaly.git",
    author="Athul Rasheeda Satheesh",
    author_email="athulrs177@gmail.com",
    packages=["compute_anomaly"],
    install_requires=[
        'numpy',
        'xarray',
	    ],
)
