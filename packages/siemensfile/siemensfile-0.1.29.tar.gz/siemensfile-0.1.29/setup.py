from setuptools import setup, find_packages

setup(
    name="siemensfile",
    version="0.1.29",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "mri-nufft",
        "pydicom"
    ],
    author="Fernando Jose Ramirez",
    author_email="fernando.ramirez.sarmiento@gmail.com",
    description="Paquete para leer archivos .dat de Siemens y realizar reconstrucciones de imágenes.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/cenarius1985/SIEMENSFile",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
