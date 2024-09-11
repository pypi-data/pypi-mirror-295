from setuptools import setup, find_packages

setup(
    name="doku_python_library", 
    version="1.1.5", 
    description="DOKU Python Library for Payment Integration", 
    url="https://github.com/PTNUSASATUINTIARTHA-DOKU/doku-python-library", 
    author="DOKU", 
    author_email="technology@doku.com", 
    license="MIT", 
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ], 
    packages= find_packages(),
    install_requires=["requests", "urllib3", "pyjwt", "pytz", "pycparser", "idna", "cryptography", "charset-normalizer", "cffi", "certifi"], 
    keywords="snap doku payment",
    python_requires=">=3.6"
) 