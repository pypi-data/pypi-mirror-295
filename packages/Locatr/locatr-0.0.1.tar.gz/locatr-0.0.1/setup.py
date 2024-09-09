from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Locatr A simple offline Reverse Geocoder Library'
LONG_DESCRIPTION = '''
Our reverse geocoding library is a robust Python tool designed to translate latitude and longitude coordinates into detailed addresses, entirely offline. It processes geographical coordinates, such as latitude and longitude, and returns a full address corresponding to the location, including country, state, city. The library is optimized for performance and accuracy, leveraging pre-downloaded datasets of geographical locations, eliminating the need for online queries or API calls.

This library is especially useful for applications where internet connectivity is limited or unavailable, or where privacy concerns require offline processing. It supports large-scale reverse geocoding operations by efficiently handling massive datasets, making it ideal for geospatial analysis, mobile applications, and data processing pipelines that require rapid location lookup without external dependencies.

With built-in data compression and storage optimizations, your reverse geocoding library minimizes disk space while maintaining high accuracy, offering developers a reliable solution for offline geocoding tasks.'''

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="Locatr",
    version=VERSION,
    author="SOORAJ TS",
    author_email="sjts007@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['reverse geocoding', 'geolocation', 'offline', 'python'],
    classifiers=[
        "Development Status :: 4 - Beta",  # Indicating the package is more stable than Alpha
        "Intended Audience :: Developers",  # Broader audience targeting developers
        "Topic :: Software Development :: Libraries :: Python Modules",  # Relevant to Python modules
        "License :: OSI Approved :: MIT License",  # Update based on your license type
        "Programming Language :: Python :: 3",  # General support for Python 3
        "Operating System :: OS Independent",  # If your package works across multiple platforms
    ]
)
