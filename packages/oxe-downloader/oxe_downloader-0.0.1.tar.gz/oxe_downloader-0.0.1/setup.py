from setuptools import setup, find_packages

setup(
    name="oxe_downloader",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "typer",
        "google-cloud-storage",
        "tqdm",
        "typing-extensions",
    ],
    entry_points={
        "console_scripts": [
            "oxe_download=oxe_downloader:app",
        ],
    },
    py_modules=["oxe_downloader"],
    python_requires=">=3.6",
    author="Misha Lvovsky",
    author_email="m.lvovsky66@gmail.com",
    description="A tool to download open-x-embodiment datasets from Google Cloud Storage",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mishmish66/oxe_downloader",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    contributors=["Original Author: Xiang Li"],
)
