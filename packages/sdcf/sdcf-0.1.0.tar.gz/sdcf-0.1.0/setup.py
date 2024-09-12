from setuptools import setup, find_packages

setup(
    name="sdcf",
    version="0.1.0",
    author="Shankar Dutt",
    author_email="shankar.dutt@anu.edu.au",
    description="Shankar Dutt's Carbon Fibre Strength Testing Platform",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "sdcf=sdcf.cli:main",
        ],
    },
    install_requires=[
        "streamlit",
        "numpy",
        "pandas",
        "matplotlib",
        "plotly",
        "scipy",
        "pdfkit"
    ],
    python_requires=">=3.6",
)