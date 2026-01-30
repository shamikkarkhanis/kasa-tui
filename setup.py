from setuptools import setup

setup(
    name="kasatui",
    version="0.1.0",
    py_modules=["kasa_tui"],
    install_requires=[
        "python-kasa",
    ],
    entry_points={
        "console_scripts": [
            "ktui=kasa_tui:main",
        ],
    },
)
