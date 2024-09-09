from setuptools import setup, find_packages
# Read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.txt").read_text()

setup(
    name='games_g',  # Name of your package
    version='1.1',  # Version number
    description='Console Based Guess the Number and Snake and Ladder Game.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ghanshyam Vaja',
    author_email='ghanshyamvaja11@gmail.com',  # Your contact email
    license='MIT',  # License type, choose according to your project
    packages=find_packages(),  # Automatically find and include packages
    classifiers=[
        'Development Status :: 5 - Production/Stable',  # Stability of the package
        'License :: OSI Approved :: MIT License',  # License info
        'Programming Language :: Python :: 3.10',  # Python version supported
    ],
    keywords='gmaes_g, g games',  # Keywords for searching on PyPI
    install_requires=['pyttsx3>=2.90',
        'pyaudio>=1.0'],  # Add any package dependencies here
    python_requires='>=3.6',  # Python version requirement
    include_package_data=True,  # Include additional files (e.g., README)
    zip_safe=False
)
