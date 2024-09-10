# -*- coding:utf-8 -*-
from setuptools import setup, find_packages
__version__ = '0.0.2.1'



setup(
    name="PlayDrissionPage",
    version=__version__,
    author="xx299x",
    author_email="xx299x@gmail.com",
    description="Playwright and DrissionPage",
    long_description="",
    long_description_content_type="text/markdown",
    license="BSD",
    keywords="Playwright, DrissionPage",
    url="https://gitee.com/xx299x/PlayDrissionPage",
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'DrissionPage',
        'playwright',
        'requests',
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'dp = DrissionPage._functions.cli:main',
        ],
    },
)
