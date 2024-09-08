from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="k8s-resource-monitor",
    version="0.1.0",
    author="Shramish Kafle",
    author_email="shramish4@gmail.com",
    description="A CLI tool for monitoring Kubernetes resources and autoscaling",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shramish2057/k8s_resource_monitor.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "click",
        "rich",
        "kubernetes",
        "matplotlib",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "k8s-monitor=k8s_monitor.cli:cli",
        ],
    },
)
