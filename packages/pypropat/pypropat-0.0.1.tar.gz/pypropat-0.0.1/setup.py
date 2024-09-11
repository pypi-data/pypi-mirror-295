from setuptools import setup, find_packages
 
__version__ = "0.0.1"
 
with open('README.md', encoding='utf-8') as f:
    readme = f.read()
 
if __name__ == "__main__":
    setup(
        name='pypropat',
        version=__version__,
        long_description=readme,
        long_description_content_type='text/markdown',
        description='Python package for a test',
        author='Oh Min Sik,Kim Gwan Young,Joo Sang Hyun ',
        author_email='michael1015999@gmail.com',
        url='https://github.com/MichaelBentlyOh/pypropat',
        install_requires=['distlib', 'idna'],
        packages=find_packages(exclude=[]),
        keywords=['orbit', 'space','spacecraft'],
        python_requires='>=3.7',
    )