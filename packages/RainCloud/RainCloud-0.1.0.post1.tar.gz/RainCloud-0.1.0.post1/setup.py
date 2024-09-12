from setuptools import setup, find_packages

setup(
    name='RainCloud',
    version='0.1.0.post1',
    author='Yosri Ben Halima',
    author_email='yosri.benhalima@ept.ucar.tn',
    description='A package for creating raincloud plots',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Yosri-Ben-Halima/RaincloudPlot',
    packages=find_packages(),
    install_requires=[
        'matplotlib',
        'seaborn',
        'ptitprince',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
