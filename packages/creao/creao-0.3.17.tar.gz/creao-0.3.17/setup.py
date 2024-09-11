from setuptools import setup, find_packages

setup(
    name="creao",
    version="0.3.17",
    packages=find_packages(),
    install_requires=[
        "networkx==3.3",
        "openai==1.40.6",
        "datasets==2.21.0",
    ],
    include_package_data=True,
    description="A description of your project",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://creao@dev.azure.com/creao/creao/_git/creao",
    author="creaoai",
    author_email="dev@creao.ai",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
