from typing import List
import os, pathlib
from setuptools import setup, find_packages


def strip_comments(string: str) -> str:
    """Remove comments string

    Args:
        string (str): some string

    Returns:
        str: striped string
    """
    return string.split('#', 1)[0].strip()

def get_dependencies(*req: str) -> List[str]:
    """Get dependencies from requirements.txt

    Returns:
        List[str]: list of dependencies strings
    """
    return list(filter(
        None,
        [strip_comments(l) for l in open(
            os.path.join(os.getcwd(), *req)
        ).readlines()]
    ))

here = pathlib.Path(__file__).parent.resolve()
NAME = 'kektris'
AUTHOR = 'Konstantin Klepikov'
EMAIL = 'oformleno@gmail.com'
DESCRIPTION = '4-quarter tetris created by Pyxel'
LONG_DESCRIPTION = (here / "README.md").read_text(encoding="utf-8")
SOURCE_URL = 'https://github.com/KonstantinKlepikov/kektris'

setup(
    name=NAME,
    version='0.0.1',
    install_requires=get_dependencies('requirements.txt'),
    extras_require={
        "dev": get_dependencies('requirements-dev.txt'),
    },
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    url=SOURCE_URL,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="game",
    license='MIT',
    python_requires='>=3.10',
    packages=find_packages(exclude=('tests*',)),
    package_dir={'': 'src'},
)
