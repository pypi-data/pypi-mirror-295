from setuptools import setup, find_packages


VERSION = "1.2.0"
DESCRIPTION = (
    "Scrape Rotten Tomatoes's website for basic information on movies, without the "
    "use of their hard-to-attain official REST API."
)


def read_me():
    with open("README.md", "r", encoding="utf-8") as f:
        return f.read()


# Set it up
setup(
    name="rottentomatoes-python",
    version=VERSION,
    author="Prerit Das",
    author_email="<preritdas@gmail.com>",
    description=DESCRIPTION,
    long_description=read_me(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["requests", "beautifulsoup4"],
    keywords=["python", "movies", "rottentomatoes"],
    url="https://github.com/preritdas/rottentomatoes-python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
