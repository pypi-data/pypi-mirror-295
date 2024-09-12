"""setup.py: setuptools control.

# Create the distribution
python3 setup.py sdist

# Upload to PyPi
twine upload ./dist/path-to-tar.gz

"""


import re
from setuptools import setup


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('quantumdiceware/quantumdiceware.py').read(),
    re.M
    ).group(1)


with open("README.rst", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(
    name = "quantumdiceware",
    packages = ["quantumdiceware"],
    python_requires=">=3.10",
    entry_points = {
        "console_scripts": ['qdg = quantumdiceware.quantumdiceware:main']
        },
    version = version,
    install_requires=[
            'python-dotenv',
            'argparse',
            'tqdm',
            'requests',
        ],
    package_data={'quantumdiceware': ['diceware_word_list.txt']},
    description = "Generates Diceware passphrases from quantum random data.",
    long_description_content_type="text/x-rst",
    long_description = long_descr,
    author = "Justin M. Sloan",
    author_email = "justin@justinsloan.com",
    url = "http://github.com/justinsloan/qdg",
    )
