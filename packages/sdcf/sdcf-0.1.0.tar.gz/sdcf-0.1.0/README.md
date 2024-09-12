# SDCF (Shankar Dutt's Carbon Fibre Strength Testing Platform)

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Data Requirements](#data-requirements)
- [Analysis Methods](#analysis-methods)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

SDCF (Shankar Dutt's Carbon Fibre Strength Testing Platform) is an integrated analysis tool specifically designed for carbon fibre strength testing. Developed by Shankar Dutt, this application provides a user-friendly interface for analyzing and visualizing strain data from ARAMIS optical measurements and stress-strain data from Instron mechanical testing machines, with a focus on carbon fibre composites.

This tool is designed to assist researchers, engineers, and material scientists in the field of composite materials, particularly those working with carbon fibre reinforced polymers (CFRP). It streamlines the process of analyzing complex experimental data from carbon fibre strength tests, enabling more efficient and accurate assessments of material properties.

## Features

- Import and process ARAMIS optical strain measurement data for carbon fibre composites
- Import and analyze Instron mechanical testing data specific to carbon fibre strength tests
- Calculate and visualize various strain parameters (longitudinal, transverse, Poisson's ratio) in carbon fibre samples
- Perform stress-strain analysis with multiple fitting methods optimized for carbon fibre composites
- Generate 2D and 3D strain distribution plots to visualize stress concentrations in carbon fibre layers
- Calculate and visualize advanced strain metrics (strain rate, strain energy) relevant to carbon fibre behavior
- Generate comprehensive HTML reports of carbon fibre strength test results
- Support for multiple strain calculation methods (Engineering, True, Green-Lagrange, etc.) applicable to composite materials
- Batch processing capabilities in "GOD Mode" for high-throughput carbon fibre testing

## Installation

To install SDCF, follow these steps:

1. Ensure you have Python 3.6 or later installed on your system.
2. Install SDCF using pip:

   ```
   pip install sdcf
   ```

   Alternatively, you can install from source:

   ```
   git clone https://github.com/shankardutt/sdcf.git
   cd sdcf
   pip install -e .
   ```

3. SDCF should now be installed and ready to use.

## Usage

To run the Shankar Dutt's Carbon Fibre Strength Testing Platform, simply use the following command:
```
SDCF
```
This will launch the Streamlit-based user interface in your default web browser.

### Basic Workflow:

1. Enter the folder path containing your ARAMIS data files from carbon fibre tests.
2. Select the series you want to analyze.
3. Adjust analysis parameters in the sidebar as needed for your specific carbon fibre sample.
4. Upload your Instron data file (CSV format) from the corresponding strength test.
5. Explore the various plots and analysis results specific to carbon fibre behavior.
6. Generate an HTML report of your carbon fibre strength test analysis if desired.

### GOD Mode:

For batch processing of multiple carbon fibre test datasets, enable GOD Mode in the application. This allows you to:

1. Select multiple ARAMIS data folders for processing different carbon fibre samples or test conditions.
2. Automatically match ARAMIS data with corresponding Instron files for each test.
3. Generate a summary CSV and a comprehensive HTML report for all processed carbon fibre datasets.

## Data Requirements

### ARAMIS Data:
- ARAMIS data should be in text file format (.txt)
- Files should follow the naming convention: `{series_name}-Stage-{stage}-{substage}.txt`
- Each file should contain strain data for a single time step of the carbon fibre test

### Instron Data:
- Instron data should be in CSV format
- The CSV should contain columns for Time, Extension, and Load from the carbon fibre strength test

## Analysis Methods

SDCF offers various strain calculation methods suitable for carbon fibre composites:

1. **Engineering Strain**: ε = (L - L₀) / L₀
2. **True Strain**: ε = ln(L / L₀)
3. **Green-Lagrange Strain**: ε = 0.5 * ((L / L₀)² - 1)
4. **Average Strain**: Calculates average strain across the gauge area of the carbon fibre sample
5. **Maximum Strain**: Identifies point of maximum deformation in the carbon fibre

The application performs stress-strain analysis tailored to carbon fibre behavior, calculates Young's modulus using both linear and polynomial fitting methods, and computes advanced metrics such as strain rate and strain energy, which are crucial for understanding the performance of carbon fibre composites under different loading conditions.

## Contributing

Contributions to SDCF are welcome! If you have suggestions for improvements or new features specific to carbon fibre testing, please feel free to submit pull requests or create issues. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Shankar Dutt - shankar.dutt@anu.edu.au

Project Link: https://github.com/yourusername/sdcf

---

For more detailed information on using specific features for carbon fibre strength testing or troubleshooting, please refer to the [documentation](docs/index.md) or open an issue on the GitHub repository.