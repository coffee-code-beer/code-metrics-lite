from setuptools import setup

setup(
    name="code-metrics-lite",
    version="1.0.0",
    py_modules=["analyzer"],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "code-metrics=analyzer:main",
        ],
    },
    author="Your Organization",
    description="A lightweight, zero-dependency Python utility for instant codebase statistics.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/coffee-code-beer/code-metrics",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
