from setuptools import setup, find_packages

setup(
    name='Cleanlyze',
    version='0.1',
    packages=find_packages(),
    install_requires=[
    'pandas',          # For data manipulation
    'numpy',           # For numerical operations
    'scikit-learn',    # For scaling, transformation, encoding, etc.
    'matplotlib',      # For plotting (optional, used for visualizations)
    'seaborn',         # For advanced visualization (optional)
    'scipy'            # For advanced statistical methods (optional)
],
    description='A simple library for data processing tasks.',
    author='PgNetwork',
    author_email='cleanlyze@gmail.com',
    readme = "README.md",
    Homepage = "https://github.com/PgNetwork01/cleanlyze"
)
