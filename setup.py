import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="iceaddr",
    version="0.5.2",  # Also update __init__.py
    author="Sveinbjorn Thordarson",
    author_email="sveinbjorn@sveinbjorn.org",
    license="BSD",
    url="https://github.com/sveinbjornt/iceaddr",
    description="Look up information about Icelandic street addresses, postcodes, landmarks, locations and placenames",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    extras_require={
        "dev": [
            "pytest",
            "humanize",
            "fiona",
        ]
    },
    packages=["iceaddr"],
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: Icelandic",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Topic :: Text Processing :: Linguistic",
    ],
    include_package_data=True,
    zip_safe=False,
)
