import os
from setuptools import setup, find_packages

# Define the current working directory
cwd = os.path.abspath(os.path.dirname(__file__))

setup(
    name="crystalpy_barno",
    version="1.1.11",
    description="Python integration with crystal report",
    long_description=open(os.path.join(cwd, "README.md")).read(),
    long_description_content_type="text/markdown",
    author="barno1994",
    author_email="barno.baptu@gmail.com",
    maintainer="barno.baptu",
    maintainer_email="barno.baptu@gmail.com",
    url="https://github.com/barno1994/crystalpy_barno",
    project_urls={
        "Homepage": "https://github.com/barno1994/crystalpy_barno",
        "Issues": "https://github.com/barno1994/crystalpy_barno/issues",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords=["crystal report", "python integration"],
    python_requires=">=3.6",
    license="MIT",
    packages=find_packages(),  # Finds all packages inside the 'crystalpy_barno' directory
    package_dir={'': '.'},  # Root package directory mapped to current directory
    include_package_data=True,  # Include data files specified in MANIFEST.in
    package_data={
        'crystalpy_barno.ReportsClasses': [
            'CR/*.dll',
            'Helpers/*.py',
            'Sales/*.py',
            'Stock/*.py',
        ],
    },
    install_requires=[],  # Add required dependencies here if any
    extras_require={
        "dev": [
            "cffi==1.17.0",
            "clr-loader==0.2.6",
            "pycparser==2.22",
            "pythonnet==3.0.3",
        ],
    },
    zip_safe=False,
)