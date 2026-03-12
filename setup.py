from setuptools import setup, find_packages

setup(
    name="EnglishCenterManager",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "PyQt6",
        "pyodbc",
    ],
    entry_points={
        "console_scripts": [
            "english_center_manager=main:main",
        ],
    },
)