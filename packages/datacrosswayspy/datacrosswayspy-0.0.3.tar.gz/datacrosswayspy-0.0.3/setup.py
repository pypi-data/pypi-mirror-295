import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="datacrosswayspy",
    version="0.0.3",
    author="Alexander Lachmann",
    author_email="alexander.lachmann@mssm.edu",
    description="Datacrossways package to access API propgramatically.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maayanlab/datacrosswayspy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_data={
        "datacrosswayspy": ["data/*"]
    },
    include_package_data=True,
    install_requires=[
        'pandas>=1.1.5',
        'numpy',
        'tqdm'
    ],
    python_requires='>=3.6',
)
