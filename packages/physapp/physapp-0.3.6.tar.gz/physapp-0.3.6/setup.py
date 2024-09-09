import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="physapp", 
    version="0.3.6",
    author="David THERINCOURT",
    author_email="dtherincourt@gmail.com",
    description="Librairie Python pour la physique appliquée",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/david-therincourt/physapp",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
    python_requires='>=3.10',
    install_requires=[
        "numpy >= 1.26.0",
        "matplotlib >= 3.8.0",
        "scipy >= 1.11.0"
        ]
)
