from setuptools import setup, find_packages

with open("readme.md", "r") as f:
    description = f.read()

setup(
    name='vzn',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'matplotlib',
        'seaborn',
        'plotly'
    ],
    description='A module for data visualization.',
    author='Alan Fernandes',
    author_email='alanferns19@gmail.com',
    url='https://github.com/AlanFernandes8/vzn',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    long_description=description,
    long_description_content_type="text/markdown",
)