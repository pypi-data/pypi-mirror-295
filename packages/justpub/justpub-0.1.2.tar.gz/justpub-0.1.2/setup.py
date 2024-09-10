
import setuptools


setuptools.setup(
    name="justpub",
    version="0.1.2",
    author="buggist",
    author_email="316114933@qq.com",
    description="Publish your python module to pypi with merely one command. ",
    long_description=open('README.md', "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Buggist/Just-Pub",
    packages=setuptools.find_packages(),
    install_requires=['setuptools', 'twine', 'wheel'],
    entry_points={
        'console_scripts': [
            'justpub=justpub:publish',
        ],
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)


