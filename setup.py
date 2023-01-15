import os.path
from setuptools import setup

setup(
    name = "wbui",
    packages = ["wbui", "wbui.default_theme"],
    py_modules = ["__main__"],
    include_package_data=True
)
