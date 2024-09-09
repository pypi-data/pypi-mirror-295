from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="raster_to_vector",
    version="0.0.1",
    author="chuboy",
    author_email="billju666@gmail.com",
    description="convert GIS WMTS tile image to polygon and point using computer vision",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/billju/raster_to_vector",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        "rapidocr-onnxruntime",
        "scikit-image",
        "shapely",
    ],
)
# pip install setuptools wheel twine
# python setup.py sdist bdist_wheel
# twine upload dist/*