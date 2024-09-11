from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ttb-cli",
    version="0.4",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    py_modules=['cli', 'src'],
    entry_points={
        'console_scripts': [
            'ttb = cli:cli',
            'tammtoolbox = cli:cli',
        ],
    },
    install_requires= [
        'polars==1.5.0',
        'Requests==2.32.3',
        'pyppeteer~=2.0.0',
        'argparse~=1.4.0',
        'click==8.1.7',
        'PyYAML==6.0.2',
        'tqdm~=4.66.5'
    ],
    include_package_data=True,
)