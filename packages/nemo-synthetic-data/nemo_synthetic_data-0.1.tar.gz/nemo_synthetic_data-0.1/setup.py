from setuptools import setup, find_packages

setup(
    name="nemo_synthetic_data",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "argparse",
        "tqdm",
        "requests",
        "jsonlines",
    ],
    entry_points={
        "console_scripts": [
            "generate-data = nemo_synthetic_data.main:main",
        ],
    },
    author="Rohith Bojja",
    author_email="rohithbojja03@gmail.com",
    description="A package for generating synthetic conversational datasets",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/rohithbojja/nemo_synthetic_data",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
