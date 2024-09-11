from setuptools import setup, find_packages

from lynq import SYSVER

setup(
    name="lynq",
    version=str(SYSVER),
    author="Elekk (elemenom)",
    author_email="pixilreal@gmail.com",
    description="Hosting local servers easily, smooth as butter.",
    long_description=(README:=open("README.md")).read(),
    long_description_content_type="text/markdown",
    url="https://github.com/elemenom/lynq",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
    license="GPLv3",
    include_package_data=True,
    install_requires=["simple-term-menu"]
)
README.close()