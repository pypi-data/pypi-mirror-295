"""
require:

    setuptools
    twine
"""

import argparse
import os
import shutil


# in <author_email> there is a email-format check.
# in <url> there is a url-format check.
setup = """
import setuptools


setuptools.setup(
    name="<package-name>",
    version="0.1.0",
    author="shut up and just publish!",
    author_email="fill@this.later",
    description="None",
    long_description=open('README.md', "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://fill.this/latter",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)


"""


def publish(package_name=None, api_token=None):
    global setup
    if not package_name and not api_token:
        parser = argparse.ArgumentParser(description="Automatic config and publish package to pypi.")
        parser.add_argument('package_name', type=str, help='package_name')
        parser.add_argument('api_token', type=str, help='api_token')
        args = parser.parse_args()

        package_name = args.package_name
        api_token    = args.api_token

    file_name = "%s.py" % package_name
    
    # 1 - Building package structure that pypi requires.
    print("\nBuilding package structure ...(1/6)")
    if os.path.isdir(file_name):
        pass
    elif os.path.isfile(file_name):
        os.makedirs(package_name)
        try:
            with open("%s/__init__.py" % package_name, "w+", encoding="utf-8") as file:
                file.writelines("from .%s import * \n" % package_name)
            shutil.copy("%s.py" % package_name, "%s/%s.py" % (package_name, package_name))
        except Exception as e:
            shutil.rmtree(package_name)
            raise(e)
    else:
        raise Exception("Module '%s' dose not exist!" % package_name)

    # os.system("pause")

    # 2 - Building README.md that pypi requires.
    print("\nBuilding README.md ...(2/6)")
    if not os.path.exists("README.md"):
        with open("README.md", "w+", encoding="utf-8") as file:
            file.writelines("# %s\n" % package_name)

    # os.system("pause")

    # 3 - Building setup.cfg that pypi requires.
    print("\nBuilding setup.cfg ...(3/6)")
    if not os.path.exists("setup.cfg"):
        with open("setup.cfg", "w+", encoding="utf-8") as file:
            file.writelines("[metadata]\ndesciption-file = README.md\n")

    # os.system("pause")

    # 4 -Building setup.py that pypi requires.
    print("\nBuilding setup.py ...(4/6)")
    if not os.path.exists("setup.py"):
        with open("setup.py", "w+", encoding="utf-8") as file:
            file.writelines(setup.replace("<package-name>", package_name))

    # os.system("pause")

    # 5 - Executing pypi build
    print("\nExecuting pypi build ...(5/6)")
    os.system("python setup.py sdist bdist_wheel")

    # os.system("pause")

    # 6 - Publishing package to pypi
    print("\nPublishing package to pypi ...(6/6)")
    os.system("twine upload dist/* --username __token__ --password %s" % api_token)

    # os.system("pause")

    print("================================")
    print("        Publish finish!!       ")
    print("================================")
    
    os.system("pause")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automatic config and publish package to pypi.")
    parser.add_argument('package_name', type=str, help='package_name')
    parser.add_argument('api_token', type=str, help='api_token')
    args = parser.parse_args()
    publish(args.package_name, args.api_token)
