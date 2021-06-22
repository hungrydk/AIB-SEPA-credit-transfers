import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aib",
    version="2.2",
    author="Hungry.dk",
    author_email="tech@hungry.dk",
    description="Python package containing the hungry AIB Document class.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hungrydk/AIB-SEPA-credit-transfers",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
    install_requires=[
        'lxml'
    ]
)
