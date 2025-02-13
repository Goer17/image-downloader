from setuptools import setup, find_packages

def read_requirements():
    with open("requirements.txt", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="image-downloader",
    version="0.1.0",
    author="Yuanyang Lee",
    author_email="yuanyanglee398@gmail.com",
    description="Image Downloader is a lightweight Python script that allows you to download images from the internet based on your search queries.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/goer17/image-downloader",
    packages=find_packages(),
    install_requires=read_requirements(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
