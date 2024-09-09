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


def publish(package_name, api_token):
    global setup

    print("package_name: ", package_name)
    print("api_token: ", api_token)
    print("========")

    file_name = "%s.py" % package_name
    
    # 构建 pypi 所需的库本体结构
    print("Building package structure ...(1/6)")
    if os.path.isfile(file_name):
        os.makedirs(package_name)
        with open("%s/__init__.py" % package_name, "w+", encoding="utf-8") as file:
            file.writelines("from .%s import * \n" % package_name)
        shutil.copy("%s.py" % package_name, "%s/%s.py" % (package_name, package_name))

    os.system("pause")

    # 构建 pypi 所需的 README.md
    print("Building README.md ...(2/6)")
    if not os.path.exists("README.md"):
        with open("README.md", "w+", encoding="utf-8") as file:
            file.writelines("# %s\n" % package_name)

    os.system("pause")

    # 构建 pypi 所需的 setup.cfg
    print("Building setup.cfg ...(3/6)")
    if not os.path.exists("setup.cfg"):
        with open("setup.cfg", "w+", encoding="utf-8") as file:
            file.writelines("[metadata]\ndesciption-file = README.md\n")

    os.system("pause")

    # 构建 pypi 所需的 setup.py
    print("Building setup.py ...(4/6)")
    if not os.path.exists("setup.py"):
        with open("setup.py", "w+", encoding="utf-8") as file:
            file.writelines(setup.replace("<package-name>", package_name))

    os.system("pause")

    # 执行构建脚本
    print("Executing pypi build ...(5/6)")
    os.system("python setup.py sdist bdist_wheel")

    os.system("pause")

    # 执行发布脚本
    print("Publishing package to pypi ...(6/6)")
    os.system("twine upload dist/* --username __token__ --password %s" % api_token)

    os.system("pause")

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
