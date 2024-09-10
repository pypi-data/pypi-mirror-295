from setuptools import setup, find_packages

setup(
    name='moseqpreprocess',  # Your package name
    version='0.1',  # Version of the package
    packages=find_packages(),  # Automatically finds sub-packages (like moseqprep)
    author='Thomas Wyndham Bush',
    author_email='thomaswyndham.bush@unitn.it',
    description='A package to filter and plot syllables',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # Indicates the type of long description
    url='',  # Replace with your project’s URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify your required Python version
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib'
    ],  # Add any external packages that your project depends on
)
