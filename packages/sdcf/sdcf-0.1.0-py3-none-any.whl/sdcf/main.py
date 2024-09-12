import streamlit as st
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import re
import warnings
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from plotly.subplots import make_subplots
from scipy.optimize import curve_fit
from scipy.interpolate import griddata
import pdfkit
import io
from plotly.io import to_image
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import base64
import time
import argparse
import sys


god_mode_enable = False
god_mode = False

def calculate_strain_rate(strain_data, time_data):
    """
    Calculate strain rate using central difference method for better accuracy.
    """
    strain_rate = np.gradient(strain_data, time_data)
    return strain_rate

def calculate_strain_energy(strain_data, stress_data):
    """
    Calculate strain energy as the area under the stress-strain curve.
    Handles potential mismatches in the lengths of stress and strain data.
    """
    # Ensure stress_data and strain_data have the same length
    min_length = min(len(strain_data), len(stress_data))
    strain_data = strain_data[:min_length]
    stress_data = stress_data[:min_length]
    
    # Calculate strain energy
    strain_energy = np.cumsum(0.5 * (stress_data[1:] + stress_data[:-1]) * np.diff(strain_data))
    return np.insert(strain_energy, 0, 0) 

def process_single_dataset(aramis_folder, instron_file, series_name, params, strain_method, save_path, max_retries=3):
    for attempt in range(max_retries):
        try:
            # Analyze ARAMIS data
            aramis_results = load_and_analyze_data(aramis_folder, series_name, 4, 9999, params, strain_method)
            
            if aramis_results is None:
                return None
            
            # Load and analyze Instron data
            instron_data = load_instron_data(instron_file)
            
            # Set default sample dimensions
            width, thickness, length = 20.0, 0.32, 100.0
            
            # Perform stress analysis
            stress_analysis_results = perform_stress_analysis(
                aramis_results['StrainOnG'],
                np.arange(len(aramis_results['StrainOnG'])),
                instron_data,
                width,
                thickness,
                length,
                data_source="both",
                align_method="max"
            )
            
            # Generate HTML report
            html_report_path = generate_pdf_report(
                aramis_results,
                stress_analysis_results,
                aramis_results['last_stage_data'],
                params,
                'ey',
                series_name,
                width,
                thickness,
                length,
                instron_data,
                save_path,
                god_mode=True
            )
            
            return {
                'series_name': series_name,
                'aramis_results': aramis_results,
                'stress_analysis_results': stress_analysis_results,
                'html_report_path': html_report_path
            }
        except Exception as e:
            if attempt < max_retries - 1:
                st.warning(f"Error processing {series_name}, retrying... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(1)  # Wait a bit before retrying
            else:
                st.error(f"Failed to process {series_name} after {max_retries} attempts. Error: {str(e)}")
                return None

def find_matching_instron_file(aramis_folder, instron_folder):
    aramis_name = os.path.basename(aramis_folder)
    matching_file = None
    
    for file in os.listdir(instron_folder):
        if file.startswith(aramis_name) and file.endswith('.is_tens_RawData'):
            matching_file = os.path.join(instron_folder, file, 'Specimen_RawData_1.csv')
            break
    
    return matching_file

def process_all_datasets(aramis_main_folder, instron_main_folder):
    all_results = []
    aramis_folders = [f for f in os.listdir(aramis_main_folder) if os.path.isdir(os.path.join(aramis_main_folder, f, 'Results'))]
    
    progress_bar = st.progress(0)
    for i, aramis_folder in enumerate(aramis_folders):
        full_aramis_path = os.path.join(aramis_main_folder, aramis_folder, 'Results')
        instron_file = find_matching_instron_file(aramis_folder, instron_main_folder)
        
        if instron_file:
            result = process_single_dataset(full_aramis_path, instron_file, aramis_folder)
            if result:
                all_results.append(result)
                st.success(f"Processed {aramis_folder}")
        else:
            st.warning(f"No matching Instron file found for {aramis_folder}")
        
        # Update progress
        progress_bar.progress((i + 1) / len(aramis_folders))
    
    return all_results

def create_summary_csv(all_results, output_path):
    summary_data = []
    
    for result in all_results:
        aramis = result['aramis_results']
        stress = result['stress_analysis_results']
        
        # Calculate standard errors
        gauge_strain_error = np.std(aramis['StrainOnG']) / np.sqrt(len(aramis['StrainOnG']))
        transverse_strain_error = np.std(aramis['StrainGtrans']) / np.sqrt(len(aramis['StrainGtrans']))
        poisson_error = np.std(aramis['Poisson']) / np.sqrt(len(aramis['Poisson']))
        
        # For Young's modulus and max stress, we'll estimate a percentage error
        young_modulus_error_percentage = 5  # Assuming 5% error, adjust as needed
        max_stress_error_percentage = 3  # Assuming 3% error, adjust as needed
        
        summary_data.append({
            'Series Name': result['series_name'],
            'Final Gauge Strain (%)': aramis['StrainOnG'][-1]*100,
            'Final Gauge Strain Error (%)': gauge_strain_error*100,
            'Final Transverse Strain (%)': aramis['StrainGtrans'][-1]*100,
            'Final Transverse Strain Error (%)': transverse_strain_error*100,
            'Final Poisson\'s Ratio': aramis['Poisson'][-1],
            'Final Poisson\'s Ratio Error': poisson_error,
            'Young\'s Modulus (ARAMIS) (MPa)': stress['E1_aramis_linear'],
            'Young\'s Modulus (ARAMIS) Error (MPa)': stress['E1_aramis_linear'] * young_modulus_error_percentage / 100,
            'Young\'s Modulus (Instron) (MPa)': stress['E1_instron_linear'],
            'Young\'s Modulus (Instron) Error (MPa)': stress['E1_instron_linear'] * young_modulus_error_percentage / 100,
            'Max Stress (ARAMIS) (MPa)': stress['max_stress_aramis'],
            'Max Stress (ARAMIS) Error (MPa)': stress['max_stress_aramis'] * max_stress_error_percentage / 100,
            'Max Stress (Instron) (MPa)': stress['max_stress_instron'],
            'Max Stress (Instron) Error (MPa)': stress['max_stress_instron'] * max_stress_error_percentage / 100,
            'HTML Report Path': result.get('html_report_path', 'Not available')
        })
    
    df = pd.DataFrame(summary_data)
    df.to_csv(output_path, index=False)
    st.success(f"Summary CSV with separate error columns created: {output_path}")

def find_max_indices(instron_data, aramis_strain):
    max_load_index = instron_data['Load'].idxmax()
    max_strain_index = np.argmax(aramis_strain)
    return max_load_index, max_strain_index

def get_save_location():
    # List of common directories
    common_dirs = {
        "Desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
        "Documents": os.path.join(os.path.expanduser("~"), "Documents"),
        "Downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
        "Custom": "custom"
    }

    # Create a dropdown for selecting the save location
    selected_dir = st.selectbox(
        "Choose where to save the report:",
        options=list(common_dirs.keys())
    )

    if selected_dir == "Custom":
        # If custom is selected, show a text input for the path
        custom_path = st.text_input("Enter the custom save path:")
        save_path = custom_path if custom_path else os.path.expanduser("~")
    else:
        save_path = common_dirs[selected_dir]

    return save_path

def synchronize_data(instron_data, aramis_results, align_method='max'):
    aramis_time = np.arange(len(aramis_results['StrainOnG']))
    
    if align_method == 'max':
        max_load_index = instron_data['Load'].idxmax()
        max_strain_index = np.argmax(aramis_results['StrainOnG'])
        
        # Align both datasets to have their maximum at t=0
        instron_time = instron_data['Time'] - instron_data['Time'].iloc[max_load_index]
        aramis_time = aramis_time - max_strain_index
        
        # Determine the overlapping time range
        start_time = max(instron_time.min(), aramis_time.min())
        end_time = min(instron_time.max(), aramis_time.max())
        
        # Filter both datasets to the overlapping range
        valid_instron = instron_data[(instron_time >= start_time) & (instron_time <= end_time)].copy()
        valid_aramis = {
            'time': aramis_time[(aramis_time >= start_time) & (aramis_time <= end_time)],
            'strain': np.array(aramis_results['StrainOnG'])[(aramis_time >= start_time) & (aramis_time <= end_time)]
        }
        
        # Reset time to start from 0
        valid_instron['Time'] = valid_instron['Time'] - valid_instron['Time'].iloc[0]
        valid_aramis['time'] = valid_aramis['time'] - valid_aramis['time'][0]
        
    else:  # 'start' alignment method
        # Find the overlapping time range
        max_time = min(instron_data['Time'].max(), aramis_time.max())
        
        # Filter both datasets to the overlapping range
        valid_instron = instron_data[instron_data['Time'] <= max_time].copy()
        valid_aramis = {
            'time': aramis_time[aramis_time <= max_time],
            'strain': np.array(aramis_results['StrainOnG'])[aramis_time <= max_time]
        }
        
        # Adjust time for ARAMIS data to match Instron time
        valid_aramis['time'] = np.interp(valid_aramis['time'], 
                                         [valid_aramis['time'][0], valid_aramis['time'][-1]], 
                                         [valid_instron['Time'].iloc[0], valid_instron['Time'].iloc[-1]])

    return valid_instron, valid_aramis

def calculate_instron_strain(instron_data, initial_length):
    return instron_data['Extension'] / initial_length


def create_analysis_plots(results):
    # Gauge Strain vs Time
    fig_gauge = go.Figure()
    fig_gauge.add_trace(go.Scatter(
        y=np.array(results['StrainOnG']) * 100,
        mode='lines+markers',
        line=dict(color='blue', width=2),
        marker=dict(color='blue', size=5)
    ))
    fig_gauge.update_layout(
        title='Gauge Strain vs Time',
        xaxis_title='Time (s)',
        yaxis_title='Gauge Strain (%)',
        width=800,
        height=400,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    # Poisson's Ratio vs Time
    fig_poisson = go.Figure()
    fig_poisson.add_trace(go.Scatter(
        y=results['Poisson'],
        mode='lines+markers',
        line=dict(color='red', width=2),
        marker=dict(color='red', size=5)
    ))
    fig_poisson.update_layout(
        title='Poisson\'s Ratio vs Time',
        xaxis_title='Time (s)',
        yaxis_title='Poisson\'s Ratio',
        yaxis=dict(range=[-1, 1]),
        width=800,
        height=400,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    return fig_gauge, fig_poisson

def create_strain_plot(results):
    time = np.arange(len(results['StrainOnG']))
    
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        subplot_titles=("Longitudinal Strain", "Transverse Strain"))
    
    fig.add_trace(
        go.Scatter(x=time, y=results['StrainOnG'], mode='lines', name='Longitudinal Strain',
                   line=dict(color='blue', width=2)),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=time, y=results['StrainGtrans'], mode='lines', name='Transverse Strain',
                   line=dict(color='red', width=2)),
        row=2, col=1
    )
    
    fig.update_layout(height=600, width=800, title_text="Longitudinal and Transverse Strain over Time",
                      plot_bgcolor='white', paper_bgcolor='white')
    fig.update_xaxes(title_text="Time (s)", row=2, col=1)
    fig.update_yaxes(title_text="Strain", row=1, col=1)
    fig.update_yaxes(title_text="Strain", row=2, col=1)
    
    return fig

def create_instron_plot(instron_data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=instron_data['Extension'], y=instron_data['Load'], 
                             mode='lines', name='Instron Data',
                             line=dict(color='green', width=2)))
    fig.update_layout(title='Instron Data: Load vs Extension (Truncated at Peak Load)', 
                      xaxis_title='Extension (mm)', 
                      yaxis_title='Load (N)',
                      plot_bgcolor='white',
                      paper_bgcolor='white')
    return fig

def create_strain_rate_plot(strain_data, time_data):
    strain_rate = calculate_strain_rate(strain_data, time_data)
    fig = go.Figure(go.Scatter(x=time_data, y=strain_rate, mode='lines', 
                               name='Strain Rate',
                               line=dict(color='purple', width=2)))
    fig.update_layout(title="Strain Rate vs Time",
                      xaxis_title="Time (s)",
                      yaxis_title="Strain Rate (1/s)",
                      plot_bgcolor='white',
                      paper_bgcolor='white')
    return fig

def create_strain_energy_plot(strain_data, stress_data, time_data):
    strain_energy = calculate_strain_energy(strain_data, stress_data)
    
    # Ensure time_data matches the length of strain_energy
    time_data = time_data[:len(strain_energy)]
    
    fig = go.Figure(go.Scatter(x=time_data, y=strain_energy, mode='lines', 
                               name='Strain Energy',
                               line=dict(color='orange', width=2)))
    fig.update_layout(title="Cumulative Strain Energy vs Time",
                      xaxis_title="Time (s)",
                      yaxis_title="Strain Energy (J/m³)",
                      plot_bgcolor='white',
                      paper_bgcolor='white')
    return fig


def generate_pdf_report(aramis_results, stress_analysis_results, file_data, params, selected_parameter, selected_series, width, thickness, length, instron_data, save_path, god_mode=False):
    # Start the HTML string
    html_str = f"""
    <html>
    <head>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            padding: 20px;
        }}
        h1, h2, h3 {{
            color: #333;
        }}
        .plot-container {{
            width: 100%;
            height: 600px;
        }}
        .page-break {{
            page-break-after: always;
        }}
    </style>
    </head>
    <body>
        <h1>ARAMIS and Instron Analysis Report: {selected_series}</h1>
        <h2>Author: Shankar Dutt</h2>
        <p>Email: shankar.dutt@anu.edu.au</p>
        
        <h2>Sample Dimensions</h2>
        <p>Width: {width} mm</p>
        <p>Thickness: {thickness} mm</p>
        <p>Length: {length} mm</p>
        
        <h2>ARAMIS Results</h2>
        <p>Final Gauge Strain: {aramis_results['StrainOnG'][-1]*100:.2f}%</p>
        <p>Final Transverse Strain: {aramis_results['StrainGtrans'][-1]*100:.2f}%</p>
        <p>Final Poisson's Ratio: {aramis_results['Poisson'][-1]:.3f}</p>
    """

    # Gauge Strain vs Time
    fig_gauge, fig_poisson = create_analysis_plots(aramis_results)
    html_str += f"""
        <h3>Gauge Strain vs Time</h3>
        <div class="plot-container" id="gauge-strain-plot"></div>
        <script>
            var gaugeStrainData = {fig_gauge.to_json()};
            Plotly.newPlot('gauge-strain-plot', gaugeStrainData.data, gaugeStrainData.layout);
        </script>
    """

    # Poisson's ratio vs Time
    html_str += f"""
        <h3>Poisson's Ratio vs Time</h3>
        <div class="plot-container" id="poisson-ratio-plot"></div>
        <script>
            var poissonRatioData = {fig_poisson.to_json()};
            Plotly.newPlot('poisson-ratio-plot', poissonRatioData.data, poissonRatioData.layout);
        </script>
    """

    # Longitudinal and Transverse Strain over Time
    strain_plot = create_strain_plot(aramis_results)
    html_str += f"""
        <div class="page-break"></div>
        <h3>Longitudinal and Transverse Strain over Time</h3>
        <div class="plot-container" id="strain-plot"></div>
        <script>
            var strainPlotData = {strain_plot.to_json()};
            Plotly.newPlot('strain-plot', strainPlotData.data, strainPlotData.layout);
        </script>
    """

    # Exclude strain distribution plot for GOD mode
    if not god_mode:
        fig_strain_distribution = create_strain_distribution_plot(file_data, params, selected_parameter)
        html_str += f"""
            <h3>Strain Distribution Plot</h3>
            <div class="plot-container" id="strain-distribution-plot"></div>
            <script>
                var strainDistributionData = {fig_strain_distribution.to_json()};
                Plotly.newPlot('strain-distribution-plot', strainDistributionData.data, strainDistributionData.layout);
            </script>
        """

    # Stress-Strain Curve (ARAMIS data only)
    fig_stress_strain = go.Figure()
    fig_stress_strain.add_trace(go.Scatter(x=stress_analysis_results['aramis_strain'], 
                                           y=stress_analysis_results['aramis_stress'], 
                                           mode='lines', 
                                           name='ARAMIS Stress-Strain',
                                           line=dict(color='blue', width=2)))
    fig_stress_strain.update_layout(title='Stress-Strain Curve (ARAMIS)', 
                                    xaxis_title='Strain', 
                                    yaxis_title='Stress (MPa)',
                                    plot_bgcolor='white',
                                    paper_bgcolor='white')
    
    html_str += f"""
        <div class="page-break"></div>
        <h2>Stress-Strain Curve (ARAMIS)</h2>
        <div class="plot-container" id="stress-strain-plot"></div>
        <script>
            var stressStrainData = {fig_stress_strain.to_json()};
            Plotly.newPlot('stress-strain-plot', stressStrainData.data, stressStrainData.layout);
        </script>
    """

    # Instron Data Plot
    fig_instron = create_instron_plot(instron_data)
    html_str += f"""
        <h3>Instron Data: Load vs Extension</h3>
        <div class="plot-container" id="instron-plot"></div>
        <script>
            var instronData = {fig_instron.to_json()};
            Plotly.newPlot('instron-plot', instronData.data, instronData.layout);
        </script>
    """

    # ARAMIS Data Analysis
    html_str += f"""
        <div class="page-break"></div>
        <h2>ARAMIS Data Analysis</h2>
        <p>Young's Modulus (Linear Fit): {stress_analysis_results['E1_aramis_linear']:.2f} MPa</p>
        <p>Young's Modulus (Polynomial Fit): {stress_analysis_results['E1_aramis_poly']:.2f} MPa</p>
        <p>Maximum Stress: {stress_analysis_results['max_stress_aramis']:.2f} MPa</p>
    """

    # Instron Data Analysis
    html_str += f"""
        <h2>Instron Data Analysis</h2>
        <p>Young's Modulus (Linear Fit): {stress_analysis_results['E1_instron_linear']:.2f} MPa</p>
        <p>Young's Modulus (Polynomial Fit): {stress_analysis_results['E1_instron_poly']:.2f} MPa</p>
        <p>Maximum Stress: {stress_analysis_results['max_stress_instron']:.2f} MPa</p>
        <p>Stiffness: {stress_analysis_results['stiffness']:.2f} N/mm</p>
    """

    # Advanced Strain Analysis
    strain_data = np.array(aramis_results['StrainOnG'])
    time_data = np.arange(len(strain_data))
    stress_data = stress_analysis_results['aramis_stress']

    # Strain Rate Plot
    fig_strain_rate = create_strain_rate_plot(strain_data, time_data)
    html_str += f"""
        <div class="page-break"></div>
        <h2>Advanced Strain Analysis</h2>
        <h3>Strain Rate vs Time</h3>
        <div class="plot-container" id="strain-rate-plot"></div>
        <script>
            var strainRateData = {fig_strain_rate.to_json()};
            Plotly.newPlot('strain-rate-plot', strainRateData.data, strainRateData.layout);
        </script>
    """

    # Strain Energy Plot
    fig_strain_energy = create_strain_energy_plot(strain_data, stress_data, time_data)
    html_str += f"""
        <h3>Cumulative Strain Energy vs Time</h3>
        <div class="plot-container" id="strain-energy-plot"></div>
        <script>
            var strainEnergyData = {fig_strain_energy.to_json()};
            Plotly.newPlot('strain-energy-plot', strainEnergyData.data, strainEnergyData.layout);
        </script>
    """

    # Complete the HTML
    html_str += """
    </body>
    </html>
    """

    # Save HTML to a file
    html_file_name = f"{selected_series}_report.html"
    html_full_path = os.path.join(save_path, html_file_name)
    with open(html_full_path, "w") as html_file:
        html_file.write(html_str)

    st.success(f"HTML Report has been generated and saved to: {html_full_path}")
    return html_full_path

def generate_god_mode_report(all_results, save_path):
    html_str = """
    <html>
    <head>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
        }
        h1, h2, h3 {
            color: #333;
        }
        .plot-container {
            width: 100%;
            height: 600px;
        }
        .page-break {
            page-break-after: always;
        }
    </style>
    </head>
    <body>
        <h1>ARAMIS and Instron Analysis Report - GOD Mode</h1>
        <h2>Author: Shankar Dutt</h2>
        <p>Email: shankar.dutt@anu.edu.au</p>
    """

    for result in all_results:
        html_str += f"""
        <div class="page-break"></div>
        <h2>Analysis for {result['series_name']}</h2>
        """

        aramis_results = result['aramis_results']
        stress_analysis_results = result['stress_analysis_results']

        html_str += f"""
        <h3>ARAMIS Results</h3>
        <p>Final Gauge Strain: {aramis_results['StrainOnG'][-1]*100:.2f}%</p>
        <p>Final Transverse Strain: {aramis_results['StrainGtrans'][-1]*100:.2f}%</p>
        <p>Final Poisson's Ratio: {aramis_results['Poisson'][-1]:.3f}</p>
        """

        # Gauge Strain vs Time
        fig_gauge, fig_poisson = create_analysis_plots(aramis_results)
        html_str += f"""
        <h3>Gauge Strain vs Time</h3>
        <div class="plot-container" id="gauge-strain-plot-{result['series_name']}"></div>
        <script>
            var gaugeStrainData = {fig_gauge.to_json()};
            Plotly.newPlot('gauge-strain-plot-{result['series_name']}', gaugeStrainData.data, gaugeStrainData.layout);
        </script>

        <h3>Poisson's Ratio vs Time</h3>
        <div class="plot-container" id="poisson-ratio-plot-{result['series_name']}"></div>
        <script>
            var poissonRatioData = {fig_poisson.to_json()};
            Plotly.newPlot('poisson-ratio-plot-{result['series_name']}', poissonRatioData.data, poissonRatioData.layout);
        </script>
        """

        # Longitudinal and Transverse Strain over Time
        strain_plot = create_strain_plot(aramis_results)
        html_str += f"""
        <h3>Longitudinal and Transverse Strain over Time</h3>
        <div class="plot-container" id="strain-plot-{result['series_name']}"></div>
        <script>
            var strainPlotData = {strain_plot.to_json()};
            Plotly.newPlot('strain-plot-{result['series_name']}', strainPlotData.data, strainPlotData.layout);
        </script>
        """

        # Stress-Strain Curve
        fig_stress_strain = create_stress_strain_plot(stress_analysis_results)
        html_str += f"""
        <h3>Stress-Strain Curve</h3>
        <div class="plot-container" id="stress-strain-plot-{result['series_name']}"></div>
        <script>
            var stressStrainData = {fig_stress_strain.to_json()};
            Plotly.newPlot('stress-strain-plot-{result['series_name']}', stressStrainData.data, stressStrainData.layout);
        </script>
        """

        # ARAMIS Data Analysis
        html_str += f"""
        <h3>ARAMIS Data Analysis</h3>
        <p>Young's Modulus (Linear Fit): {stress_analysis_results['E1_aramis_linear']:.2f} MPa</p>
        <p>Young's Modulus (Polynomial Fit): {stress_analysis_results['E1_aramis_poly']:.2f} MPa</p>
        <p>Maximum Stress: {stress_analysis_results['max_stress_aramis']:.2f} MPa</p>
        """

        # Instron Data Analysis
        html_str += f"""
        <h3>Instron Data Analysis</h3>
        <p>Young's Modulus (Linear Fit): {stress_analysis_results['E1_instron_linear']:.2f} MPa</p>
        <p>Young's Modulus (Polynomial Fit): {stress_analysis_results['E1_instron_poly']:.2f} MPa</p>
        <p>Maximum Stress: {stress_analysis_results['max_stress_instron']:.2f} MPa</p>
        <p>Stiffness: {stress_analysis_results['stiffness']:.2f} N/mm</p>
        """

        # Advanced Strain Analysis
        strain_data = np.array(aramis_results['StrainOnG'])
        time_data = np.arange(len(strain_data))
        stress_data = stress_analysis_results['aramis_stress']

        # Strain Rate Plot
        fig_strain_rate = create_strain_rate_plot(strain_data, time_data)
        html_str += f"""
        <h3>Strain Rate vs Time</h3>
        <div class="plot-container" id="strain-rate-plot-{result['series_name']}"></div>
        <script>
            var strainRateData = {fig_strain_rate.to_json()};
            Plotly.newPlot('strain-rate-plot-{result['series_name']}', strainRateData.data, strainRateData.layout);
        </script>
        """

        # Strain Energy Plot
        fig_strain_energy = create_strain_energy_plot(strain_data, stress_data, time_data)
        html_str += f"""
        <h3>Cumulative Strain Energy vs Time</h3>
        <div class="plot-container" id="strain-energy-plot-{result['series_name']}"></div>
        <script>
            var strainEnergyData = {fig_strain_energy.to_json()};
            Plotly.newPlot('strain-energy-plot-{result['series_name']}', strainEnergyData.data, strainEnergyData.layout);
        </script>
        """

    # Complete the HTML
    html_str += """
    </body>
    </html>
    """

    # Save HTML to a file
    html_file_name = "god_mode_report.html"
    html_full_path = os.path.join(save_path, html_file_name)
    with open(html_full_path, "w") as html_file:
        html_file.write(html_str)

    return html_full_path


def truncate_at_peak_load(instron_data):
    peak_index = instron_data['Load'].idxmax()
    return instron_data.iloc[:peak_index+1]

def load_instron_data(file):
    df = pd.read_csv(file, skiprows=1)
    time_column = df.columns[0]
    extension_column = df.columns[1]
    load_column = df.columns[2]
    df = df.rename(columns={time_column: 'Time', extension_column: 'Extension', load_column: 'Load'})
    df = truncate_at_peak_load(df)
    return df

def calculate_stress(load, width, thickness):
    return load / (width * thickness)

# def calculate_instron_strain(extension, initial_length):
#     return extension / initial_length

def calculate_aramis_strain(D, params, method='engineering'):
    valid_indices = ~np.isnan(D['xi']) & ~np.isnan(D['yi']) & ~np.isnan(D['x']) & ~np.isnan(D['y'])
    
    if method == 'engineering':
        distances1 = np.sqrt((params['ytop'] - D['yi'][valid_indices])**2 + (params['xtop'] - D['xi'][valid_indices])**2)
        index1 = np.argmin(distances1)
        distances2 = np.sqrt((params['ybot'] - D['yi'][valid_indices])**2 + (params['xbot'] - D['xi'][valid_indices])**2)
        index2 = np.argmin(distances2)
        
        lengthinitial = np.sqrt((D['yi'][valid_indices][index1] - D['yi'][valid_indices][index2])**2 + 
                                (D['xi'][valid_indices][index1] - D['xi'][valid_indices][index2])**2)
        lengthnew = np.sqrt((D['y'][valid_indices][index1] - D['y'][valid_indices][index2])**2 + 
                            (D['x'][valid_indices][index1] - D['x'][valid_indices][index2])**2)
        
        return (lengthnew - lengthinitial) / lengthinitial
    
    elif method == 'average':
        initial_lengths = np.sqrt((D['yi'][valid_indices] - params['ybot'])**2 + (D['xi'][valid_indices] - params['xbot'])**2)
        new_lengths = np.sqrt((D['y'][valid_indices] - params['ybot'])**2 + (D['x'][valid_indices] - params['xbot'])**2)
        strains = (new_lengths - initial_lengths) / initial_lengths
        return np.mean(strains)
    
    elif method == 'maximum':
        initial_lengths = np.sqrt((D['yi'][valid_indices] - params['ybot'])**2 + (D['xi'][valid_indices] - params['xbot'])**2)
        new_lengths = np.sqrt((D['y'][valid_indices] - params['ybot'])**2 + (D['x'][valid_indices] - params['xbot'])**2)
        strains = (new_lengths - initial_lengths) / initial_lengths
        return np.max(strains)
    
    elif method == 'true':
        distances1 = np.sqrt((params['ytop'] - D['yi'][valid_indices])**2 + (params['xtop'] - D['xi'][valid_indices])**2)
        index1 = np.argmin(distances1)
        distances2 = np.sqrt((params['ybot'] - D['yi'][valid_indices])**2 + (params['xbot'] - D['xi'][valid_indices])**2)
        index2 = np.argmin(distances2)
        
        lengthinitial = np.sqrt((D['yi'][valid_indices][index1] - D['yi'][valid_indices][index2])**2 + 
                                (D['xi'][valid_indices][index1] - D['xi'][valid_indices][index2])**2)
        lengthnew = np.sqrt((D['y'][valid_indices][index1] - D['y'][valid_indices][index2])**2 + 
                            (D['x'][valid_indices][index1] - D['x'][valid_indices][index2])**2)
        
        return np.log(lengthnew / lengthinitial)
    
    elif method == 'green-lagrange':
        distances1 = np.sqrt((params['ytop'] - D['yi'][valid_indices])**2 + (params['xtop'] - D['xi'][valid_indices])**2)
        index1 = np.argmin(distances1)
        distances2 = np.sqrt((params['ybot'] - D['yi'][valid_indices])**2 + (params['xbot'] - D['xi'][valid_indices])**2)
        index2 = np.argmin(distances2)
        
        lengthinitial = np.sqrt((D['yi'][valid_indices][index1] - D['yi'][valid_indices][index2])**2 + 
                                (D['xi'][valid_indices][index1] - D['xi'][valid_indices][index2])**2)
        lengthnew = np.sqrt((D['y'][valid_indices][index1] - D['y'][valid_indices][index2])**2 + 
                            (D['x'][valid_indices][index1] - D['x'][valid_indices][index2])**2)
        
        return 0.5 * ((lengthnew / lengthinitial)**2 - 1)
    
    else:
        raise ValueError(f"Unknown strain calculation method: {method}")

def linear_fit(x, a, b):
    return a * x + b

def polynomial_fit(x, a, b, c):
    return a * x**2 + b * x + c



def perform_stress_analysis(aramis_strain, aramis_time, instron_data, width, thickness, length, data_source="both", align_method='max'):
    try:
        # Synchronize data
        synced_instron, synced_aramis = synchronize_data(instron_data, {'StrainOnG': aramis_strain}, align_method)
        
        # Calculate Instron strain
        synced_instron.loc[:,'Strain'] = calculate_instron_strain(synced_instron, length)
        
        # Calculate stress for both datasets
        instron_stress = calculate_stress(synced_instron['Load'], width, thickness)
        aramis_stress = np.interp(synced_aramis['time'], synced_instron['Time'], instron_stress)
        

        # Ensure data is 1D and has the same length
        synced_aramis_strain = synced_aramis['strain']
        synced_instron_strain = synced_instron['Strain'].values
        
        # Convert to numpy arrays if they're not already
        if isinstance(synced_aramis_strain, pd.Series):
            synced_aramis_strain = synced_aramis_strain.values
        if isinstance(aramis_stress, pd.Series):
            aramis_stress = aramis_stress.values
        if isinstance(instron_stress, pd.Series):
            instron_stress = instron_stress.values
        
        # Flatten arrays
        synced_aramis_strain = synced_aramis_strain.flatten()
        aramis_stress = aramis_stress.flatten()
        synced_instron_strain = synced_instron_strain.flatten()
        instron_stress = instron_stress.flatten()
        
        # Ensure no NaN or inf values
        valid_aramis = np.isfinite(synced_aramis_strain) & np.isfinite(aramis_stress)
        valid_instron = np.isfinite(synced_instron_strain) & np.isfinite(instron_stress)
        
        synced_aramis_strain = synced_aramis_strain[valid_aramis]
        aramis_stress = aramis_stress[valid_aramis]
        synced_instron_strain = synced_instron_strain[valid_instron]
        instron_stress = instron_stress[valid_instron]
        
        if data_source == "aramis":
            selected_strain = synced_aramis_strain
            selected_stress = aramis_stress
        elif data_source == "instron":
            selected_strain = synced_instron_strain
            selected_stress = instron_stress
        else:  # both
            selected_strain = synced_aramis_strain
            selected_stress = aramis_stress
        
        # Perform linear and polynomial fits for both datasets
        popt_linear_aramis, _ = curve_fit(linear_fit, synced_aramis_strain, aramis_stress)
        popt_poly_aramis, _ = curve_fit(polynomial_fit, synced_aramis_strain, aramis_stress)
        popt_linear_instron, _ = curve_fit(linear_fit, synced_instron_strain, instron_stress)
        popt_poly_instron, _ = curve_fit(polynomial_fit, synced_instron_strain, instron_stress)
        
        # Calculate stiffness (slope of the linear portion of the stress-strain curve)
        stiffness = np.gradient(selected_stress, selected_strain)[0]  # Approximate initial slope
        
        return {
            'aramis_strain': synced_aramis_strain,
            'aramis_stress': aramis_stress,
            'aramis_time': synced_aramis['time'],
            'instron_strain': synced_instron_strain,
            'instron_stress': instron_stress,
            'instron_time': synced_instron['Time'],
            'E1_aramis_linear': popt_linear_aramis[0],
            'E1_aramis_poly': popt_poly_aramis[1],  # First derivative at strain = 0
            'E1_instron_linear': popt_linear_instron[0],
            'E1_instron_poly': popt_poly_instron[1],  # First derivative at strain = 0
            'stiffness': stiffness,
            'max_stress_aramis': np.max(aramis_stress),
            'max_stress_instron': np.max(instron_stress),
            'popt_linear_aramis': popt_linear_aramis,
            'popt_poly_aramis': popt_poly_aramis,
            'popt_linear_instron': popt_linear_instron,
            'popt_poly_instron': popt_poly_instron
        }
    except Exception as e:
        st.error(f"Error during stress analysis: {str(e)}")
        st.write("Debug information:")
        st.write(f"ARAMIS strain shape: {synced_aramis_strain.shape if 'synced_aramis_strain' in locals() else 'Not available'}")
        st.write(f"ARAMIS stress shape: {aramis_stress.shape if 'aramis_stress' in locals() else 'Not available'}")
        st.write(f"Instron strain shape: {synced_instron_strain.shape if 'synced_instron_strain' in locals() else 'Not available'}")
        st.write(f"Instron stress shape: {instron_stress.shape if 'instron_stress' in locals() else 'Not available'}")
        return None
    
def fileprep(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Extract header information
    header = lines[:12]
    ad_channels = {}
    for line in header:
        if line.startswith('#     AD-'):
            parts = line.split()
            ad_channels[parts[1].strip(':')] = float(parts[2])

    # Process data lines
    data = []
    max_fields = 0
    for line in lines[12:]:
        line = line.strip()
        if line:
            # Split the line and convert to float, ignoring any non-numeric values
            values = [float(val) for val in line.split() if val.replace('.', '', 1).replace('-', '', 1).isdigit()]
            if values:
                data.append(values)
                max_fields = max(max_fields, len(values))

    # Check if data is empty
    if not data:
        #st.warning(f"No valid data found in file: {filename}")
        return None

    # Pad shorter rows with NaN
    padded_data = [row + [np.nan] * (max_fields - len(row)) for row in data]

    # Convert data to numpy array
    data_array = np.array(padded_data)

    # Determine the number of columns
    num_columns = data_array.shape[1] if data_array.ndim > 1 else 0

    # Assign column names based on the number of columns
    column_names = ['Index_x', 'Index_y', 
                    'Coordinate-undef_x', 'Coordinate-undef_y', 'Coordinate-undef_z',
                    'Coord-def_x', 'Coord-def_y', 'Coord-def_z',
                    'Displ_x', 'Displ_y', 'Displ_z']
    if num_columns > 11:
        column_names.extend(['Strain_x', 'Strain_y', 'Strain_xy', 'Strain_Major', 'Strain_Minor', 'Strain_Thickness'])
    if num_columns > 17:
        column_names.extend(['AD-0', 'AD-1'])
    # Add generic column names for any additional columns
    column_names.extend([f'Column_{i}' for i in range(len(column_names), num_columns)])

    # Create DataFrame
    df = pd.DataFrame(data_array, columns=column_names[:num_columns])

    return {
        'xi': df['Coordinate-undef_x'] if 'Coordinate-undef_x' in df else None,
        'yi': df['Coordinate-undef_y'] if 'Coordinate-undef_y' in df else None,
        'zi': df['Coordinate-undef_z'] if 'Coordinate-undef_z' in df else None,
        'x': df['Coord-def_x'] if 'Coord-def_x' in df else None,
        'y': df['Coord-def_y'] if 'Coord-def_y' in df else None,
        'z': df['Coord-def_z'] if 'Coord-def_z' in df else None,
        'dx': df['Displ_x'] if 'Displ_x' in df else None,
        'dy': df['Displ_y'] if 'Displ_y' in df else None,
        'dz': df['Displ_z'] if 'Displ_z' in df else None,
        'ix': df['Index_x'] if 'Index_x' in df else None,
        'iy': df['Index_y'] if 'Index_y' in df else None,
        'ad_channels': ad_channels,
        'ex': df['Strain_x'] if 'Strain_x' in df else None,
        'ey': df['Strain_y'] if 'Strain_y' in df else None,
        'exy': df['Strain_xy'] if 'Strain_xy' in df else None,
        'ema': df['Strain_Major'] if 'Strain_Major' in df else None,
        'emi': df['Strain_Minor'] if 'Strain_Minor' in df else None,
    }


def analyze_files(folder_path):
    files = os.listdir(folder_path)
    series_pattern = r'(.+)-Stage-(\d+)-(\d+)\.txt'
    series_dict = {}
    
    for file in files:
        match = re.match(series_pattern, file)
        if match:
            series_name, stage, substage = match.groups()
            stage = int(stage)
            substage = int(substage)
            if series_name not in series_dict:
                series_dict[series_name] = []
            series_dict[series_name].append((stage, substage, file))
        else:
            st.write(f"Debug: File '{file}' did not match the expected pattern")
    
    # Sort the files within each series
    for series, stages in series_dict.items():
        series_dict[series] = sorted(stages, key=lambda x: (x[0], x[1]))
        st.write(f"Series '{series}' has {len(stages)} stages")

    return series_dict

def perform_analysis(folder_path, selected_series, start_substage, end_substage, params, strain_method):
    StrainOnG, StrainGtrans, Poisson = [], [], []
    last_valid_D = None
    errors = []
    unloadable_files = []
    last_loadable_file = None

    for substage in range(start_substage, end_substage + 1):
        filename = os.path.join(folder_path, f"{selected_series}-Stage-0-{substage}.txt")
        if not os.path.exists(filename):
            unloadable_files.append(filename)
            continue

        D = fileprep(filename)
        if D is None:
            unloadable_files.append(filename)
            continue

        last_valid_D = D
        last_loadable_file = filename

        try:
            # Calculate longitudinal strain
            strainstep = calculate_aramis_strain(D, params, method=strain_method)

            # Calculate transverse strain
            transverse_params = params.copy()
            transverse_params['ytop'], transverse_params['ybot'] = params['yleft'], params['yright']
            transverse_params['xtop'], transverse_params['xbot'] = params['xleft'], params['xright']
            straintrans = calculate_aramis_strain(D, transverse_params, method=strain_method)

            StrainOnG.append(strainstep)
            StrainGtrans.append(straintrans)

        except Exception as e:
            errors.append(f"Error processing substage {substage}: {str(e)}")

    if errors:
        st.warning("Some errors occurred during processing:")
        for error in errors:
            st.warning(error)

    if unloadable_files:
        # st.warning(f"The following files could not be loaded: {', '.join(unloadable_files)}")
        if last_loadable_file:
            st.warning(f"Complete failure might have occurred just before {last_loadable_file}")

    if not StrainOnG:
        st.error("No valid data files were processed.")
        return None

    Poisson = -np.array(StrainGtrans) / np.array(StrainOnG)
    Poisson = np.where(np.isfinite(Poisson), Poisson, np.nan)  # Replace inf and -inf with NaN

    return {
        'StrainOnG': StrainOnG,
        'StrainGtrans': StrainGtrans,
        'Poisson': Poisson,
        'last_stage_data': last_valid_D,
        'plot_params': params
    }

@st.cache_data
def load_and_analyze_data(folder_path, selected_series, start_substage, end_substage, params, strain_method):
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', category=RuntimeWarning)
        results = perform_analysis(folder_path, selected_series, start_substage, end_substage, params, strain_method)
    return results


def create_stress_strain_plot(stress_analysis_results, data_source="both"):
    fig = go.Figure()
    
    if data_source in ["aramis", "both"]:
        # ARAMIS Data and Fits
        fig.add_trace(go.Scatter(x=stress_analysis_results['aramis_strain'], y=stress_analysis_results['aramis_stress'], mode='markers', name='ARAMIS Data'))
        
        # Calculate and add ARAMIS linear fit
        aramis_strain_range = np.linspace(min(stress_analysis_results['aramis_strain']), max(stress_analysis_results['aramis_strain']), 100)
        aramis_linear_fit = stress_analysis_results['popt_linear_aramis'][0] * aramis_strain_range + stress_analysis_results['popt_linear_aramis'][1]
        fig.add_trace(go.Scatter(x=aramis_strain_range, y=aramis_linear_fit, mode='lines', name='ARAMIS Linear Fit'))
        
        # Calculate and add ARAMIS polynomial fit
        aramis_poly_fit = stress_analysis_results['popt_poly_aramis'][0] * aramis_strain_range**2 + stress_analysis_results['popt_poly_aramis'][1] * aramis_strain_range + stress_analysis_results['popt_poly_aramis'][2]
        fig.add_trace(go.Scatter(x=aramis_strain_range, y=aramis_poly_fit, mode='lines', name='ARAMIS Polynomial Fit'))
    
    if data_source in ["instron", "both"]:
        # Instron Data and Fits
        fig.add_trace(go.Scatter(x=stress_analysis_results['instron_strain'], y=stress_analysis_results['instron_stress'], mode='markers', name='Instron Data'))
        
        # Calculate and add Instron linear fit
        instron_strain_range = np.linspace(min(stress_analysis_results['instron_strain']), max(stress_analysis_results['instron_strain']), 100)
        instron_linear_fit = stress_analysis_results['popt_linear_instron'][0] * instron_strain_range + stress_analysis_results['popt_linear_instron'][1]
        fig.add_trace(go.Scatter(x=instron_strain_range, y=instron_linear_fit, mode='lines', name='Instron Linear Fit'))
        
        # Calculate and add Instron polynomial fit
        instron_poly_fit = stress_analysis_results['popt_poly_instron'][0] * instron_strain_range**2 + stress_analysis_results['popt_poly_instron'][1] * instron_strain_range + stress_analysis_results['popt_poly_instron'][2]
        fig.add_trace(go.Scatter(x=instron_strain_range, y=instron_poly_fit, mode='lines', name='Instron Polynomial Fit'))
    
    fig.update_layout(title='Stress-Strain Curve', xaxis_title='Strain', yaxis_title='Stress (MPa)')
    return fig


def create_instron_plot(instron_data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=instron_data['Extension'], y=instron_data['Load'], mode='lines', name='Instron Data'))
    fig.update_layout(title='Instron Data: Load vs Extension (Truncated at Peak Load)', 
                      xaxis_title='Extension (mm)', 
                      yaxis_title='Load (N)')
    return fig


def create_strain_plot(results):
    # Create a time array based on the length of StrainOnG
    time = np.arange(len(results['StrainOnG']))
    
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        subplot_titles=("Longitudinal Strain", "Transverse Strain"))
    
    fig.add_trace(
        go.Scatter(x=time, y=results['StrainOnG'], mode='lines', name='Longitudinal Strain'),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=time, y=results['StrainGtrans'], mode='lines', name='Transverse Strain'),
        row=2, col=1
    )
    
    fig.update_layout(height=600, width=800, title_text="Longitudinal and Transverse Strain over Time")
    fig.update_xaxes(title_text="Time (s)", row=2, col=1)
    fig.update_yaxes(title_text="Strain", row=1, col=1)
    fig.update_yaxes(title_text="Strain", row=2, col=1)
    
    return fig

def create_strain_distribution_plot(data, params, selected_parameter, contrast_min=-2.0, contrast_max=2.0):
    fig = go.Figure()
    if data[selected_parameter] is not None:
        fig.add_trace(go.Scatter(
            x=data['xi'],
            y=data['yi'],
            mode='markers',
            marker=dict(
                size=5,
                color=data[selected_parameter],
                colorscale='Jet',
                showscale=True,
                cmin=contrast_min,
                cmax=contrast_max
            )
        ))
    else:
        fig.add_trace(go.Scatter(
            x=data['xi'],
            y=data['yi'],
            mode='markers',
            marker=dict(size=5)
        ))
    
    p = params
    fig.add_trace(go.Scatter(
        x=[p['xtop'], p['xbot']],
        y=[p['ytop'], p['ybot']],
        mode='lines+markers',
        line=dict(color='red', width=2),
        marker=dict(symbol='x', size=10, color='red'),
        showlegend=False
    ))
    fig.add_trace(go.Scatter(
        x=[p['xleft'], p['xright']],
        y=[p['yleft'], p['yright']],
        mode='lines+markers',
        line=dict(color='red', width=2),
        marker=dict(symbol='x', size=10, color='red'),
        showlegend=False
    ))
    
    fig.update_layout(
        title=f'{selected_parameter} Distribution',
        xaxis_title='x (mm)',
        yaxis_title='y (mm)',
        yaxis=dict(scaleanchor="x", scaleratio=1),
        width=800,
        height=600
    )
    return fig


def create_3d_strain_plot(file_data_list, params, selected_parameter):
    fig = go.Figure()

    for i, file_data in enumerate(file_data_list):
        if file_data is not None and selected_parameter in file_data and file_data[selected_parameter] is not None:
            xi = file_data['xi'].values
            yi = file_data['yi'].values
            z_data = file_data[selected_parameter].values
            
            grid_x, grid_y = np.meshgrid(np.linspace(np.min(xi), np.max(xi), 100),
                                         np.linspace(np.min(yi), np.max(yi), 100))

            grid_z = griddata((xi, yi), z_data, (grid_x, grid_y), method='linear')

            fig.add_trace(go.Surface(
                x=grid_x,
                y=grid_y,
                z=grid_z,
                surfacecolor=grid_z,
                colorscale='Jet',
                opacity=0.7,
                showscale=(i == 0),
                name=f'Time {i}'
            ))

    fig.update_layout(
        title=f'3D {selected_parameter} Distribution Over Time',
        scene=dict(
            xaxis_title='x (mm)',
            yaxis_title='y (mm)',
            zaxis_title=selected_parameter,
            aspectratio=dict(x=1, y=1, z=0.5)
        ),
        width=800,
        height=600
    )

    sliders = [dict(
        active=0,
        currentvalue={"prefix": "Time: "},
        pad={"t": 50},
        steps=[dict(
            method='update',
            args=[{'visible': [j == i for j in range(len(file_data_list))]}],
            label=str(i)
        ) for i in range(len(file_data_list))]
    )]

    fig.update_layout(sliders=sliders)

    return fig

def create_alignment_plot(stress_analysis_results):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=stress_analysis_results['aramis_time'], 
                             y=stress_analysis_results['aramis_strain'], 
                             mode='lines', 
                             name='ARAMIS Strain'))
    
    fig.add_trace(go.Scatter(x=stress_analysis_results['instron_time'], 
                             y=stress_analysis_results['instron_strain'], 
                             mode='lines', 
                             name='Instron Strain'))
    
    fig.update_layout(title='Aligned Strain Data',
                      xaxis_title='Time',
                      yaxis_title='Strain',
                      legend_title='Data Source')
    
    return fig

def create_analysis_plots(results):
    # Gauge Strain vs Time
    fig_gauge = go.Figure()
    fig_gauge.add_trace(go.Scatter(
        y=np.array(results['StrainOnG']) * 100,
        mode='lines+markers'
    ))
    fig_gauge.update_layout(
        title='Gauge Strain vs Time',
        xaxis_title='Time (s)',
        yaxis_title='Gauge Strain (%)',
        width=800,
        height=400
    )

    # Poisson's Ratio vs Time
    fig_poisson = go.Figure()
    fig_poisson.add_trace(go.Scatter(
        y=results['Poisson'],
        mode='lines+markers'
    ))
    fig_poisson.update_layout(
        title='Poisson\'s Ratio vs Time',
        xaxis_title='Time (s)',
        yaxis_title='Poisson\'s Ratio',
        yaxis=dict(range=[-1, 1]),
        width=800,
        height=400
    )

    return fig_gauge, fig_poisson

def create_results_dataframe(results, analysis_options):
    df = pd.DataFrame({
        'StrainOnG': results['StrainOnG'],
        'StrainGtrans': results['StrainGtrans'],
        'Poisson': results['Poisson']
    })
    
    if "Strain Rate" in analysis_options:
        df['StrainRate'] = np.pad(np.diff(results['StrainOnG']) / np.diff(np.arange(len(results['StrainOnG']))), (1, 0), 'constant')
    
    if "Strain Energy" in analysis_options:
        df['StrainEnergy'] = np.cumsum(np.array(results['StrainOnG']) ** 2)
    
    return df



def create_strain_rate_plot(strain_data, time_data):
    strain_rate = calculate_strain_rate(strain_data, time_data)
    fig = go.Figure(go.Scatter(x=time_data, y=strain_rate, mode='lines', name='Strain Rate'))
    fig.update_layout(title="Strain Rate vs Time",
                      xaxis_title="Time (s)",
                      yaxis_title="Strain Rate (1/s)")
    return fig

def create_strain_energy_plot(strain_data, stress_data, time_data):
    strain_energy = calculate_strain_energy(strain_data, stress_data)
    
    # Ensure time_data matches the length of strain_energy
    time_data = time_data[:len(strain_energy)]
    
    fig = go.Figure(go.Scatter(x=time_data, y=strain_energy, mode='lines', name='Strain Energy'))
    fig.update_layout(title="Cumulative Strain Energy vs Time",
                      xaxis_title="Time (s)",
                      yaxis_title="Strain Energy (J/m³)")
    return fig


def display_strain_analysis(aramis_results, stress_analysis_results):
    st.subheader("Advanced Strain Analysis")

    strain_data = np.array(aramis_results['StrainOnG'])
    time_data = np.arange(len(strain_data))
    stress_data = stress_analysis_results['aramis_stress']

    # Ensure all data arrays have the same length
    min_length = min(len(strain_data), len(stress_data), len(time_data))
    strain_data = strain_data[:min_length]
    stress_data = stress_data[:min_length]
    time_data = time_data[:min_length]

    # Strain Rate Analysis
    with st.expander("Strain Rate Analysis"):
        st.markdown("""
        **Strain Rate** is the rate of change of strain with respect to time. It is calculated as:

        Strain Rate = dε/dt

        where ε is strain and t is time.

        **Significance**:
        - Indicates how fast the material is deforming
        - Many materials exhibit different behaviors at different strain rates
        - Critical for understanding material behavior in dynamic loading conditions
        - Important in designing for impact, crash, or high-speed manufacturing processes
        """)
        fig_strain_rate = create_strain_rate_plot(strain_data, time_data)
        st.plotly_chart(fig_strain_rate)

    # Strain Energy Analysis
    with st.expander("Strain Energy Analysis"):
        st.markdown("""
        **Strain Energy** is the energy stored in a material as a result of deformation. It is calculated as the area under the stress-strain curve:

        Strain Energy = ∫ σ dε

        where σ is stress and ε is strain.

        **Significance**:
        - Represents the material's capacity to absorb and release energy elastically
        - Indicative of the material's toughness and resilience
        - Important in applications requiring energy absorption (e.g., protective equipment, crash structures)
        - Used in various failure theories and structural analyses
        """)
        fig_strain_energy = create_strain_energy_plot(strain_data, stress_data, time_data)
        st.plotly_chart(fig_strain_energy)

def analyze_poisson_ratio(aramis_results):
    poisson_values = aramis_results['Poisson']
    total_values = len(poisson_values)
    
    st.write("Poisson's Ratio Analysis")
    
    # Slider for selecting the number of last values to analyze
    num_values = st.slider("Select number of last values to analyze", 
                           min_value=1, 
                           max_value=total_values, 
                           value=min(50, total_values), 
                           step=1)
    
    # Calculate mean and standard deviation
    selected_values = poisson_values[-num_values:]
    mean_poisson = np.mean(selected_values)
    std_poisson = np.std(selected_values)
    
    st.write(f"Mean Poisson's Ratio (last {num_values} values): {mean_poisson:.3f}")
    st.write(f"Standard Deviation of Poisson's Ratio (last {num_values} values): {std_poisson:.3f}")
    
    # Create a plot of Poisson's ratio over time
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=poisson_values, mode='lines', name="Poisson's Ratio"))
    fig.add_trace(go.Scatter(y=[mean_poisson]*len(poisson_values), mode='lines', 
                             name=f"Mean (last {num_values} values)", line=dict(dash='dash')))
    fig.update_layout(title="Poisson's Ratio Over Time",
                      xaxis_title="Time Step",
                      yaxis_title="Poisson's Ratio",
                      yaxis=dict(range=[-0.1, 1]),
                      width=800,
                      height=600)
    st.plotly_chart(fig)

def run_app():
    st.title("Integrated ARAMIS and Instron Analysis")
    st.subheader("Shankar Dutt")
    st.text("shankar.dutt@anu.edu.au")
    # Initialize session state variables
    if 'contrast_min' not in st.session_state:
        st.session_state.contrast_min = -2.0
    if 'contrast_max' not in st.session_state:
        st.session_state.contrast_max = 2.0
    
    god_mode = st.checkbox("Enable GOD Mode")

    if god_mode:
        aramis_main_folder = st.text_input("Enter the main folder path containing ARAMIS data folders:")
        instron_main_folder = st.text_input("Enter the main folder path containing Instron data files:")
        
        if aramis_main_folder and instron_main_folder and os.path.isdir(aramis_main_folder) and os.path.isdir(instron_main_folder):
            aramis_folders = [f for f in os.listdir(aramis_main_folder) if os.path.isdir(os.path.join(aramis_main_folder, f, 'Results'))]
            selected_folders = st.multiselect("Select folders to process:", aramis_folders, default=aramis_folders)
            
            # Add parameter inputs for GOD mode
            st.sidebar.header("Analysis Parameters")
            with st.sidebar.expander("Position Parameters"):
                a = st.number_input("a", value=-2)
                b = st.number_input("b", value=0)
                ytop = st.number_input("ytop", value=15+b)
                ybot = st.number_input("ybot", value=-15+b)
                xtop = st.number_input("xtop", value=0+a)
                xbot = st.number_input("xbot", value=0+a)
                yleft = st.number_input("yleft", value=0+b)
                yright = st.number_input("yright", value=0+b)
                xleft = st.number_input("xleft", value=-3.5+a)
                xright = st.number_input("xright", value=3.5+a)
            
            params = {
                'ytop': ytop, 'ybot': ybot, 'xtop': xtop, 'xbot': xbot,
                'yleft': yleft, 'yright': yright, 'xleft': xleft, 'xright': xright
            }
            
            strain_method = st.sidebar.selectbox("Select strain calculation method:", 
                            ['Engineering', 'Average', 'Maximum', 'True', 'Green-Lagrange'])
            
            save_path = get_save_location()
            
            if st.button("Process Selected Datasets"):
                all_results = []
                for folder in selected_folders:
                    result = process_single_dataset(
                        os.path.join(aramis_main_folder, folder, 'Results'), 
                        find_matching_instron_file(folder, instron_main_folder), 
                        folder,
                        params=params,
                        strain_method=strain_method.lower(),
                        save_path=save_path
                    )
                    if result:
                        all_results.append(result)
                
                # Generate summary CSV
                csv_path = os.path.join(save_path, "summary_results.csv")
                create_summary_csv(all_results, csv_path)
                st.success(f"Summary CSV created: {csv_path}")
                
                # Generate single HTML report
                html_path = generate_god_mode_report(all_results, save_path)
                st.success(f"HTML Report created: {html_path}")
        else:
            st.warning("Please enter valid folder paths for both ARAMIS and Instron data.")
    else:
        folder_path = st.text_input("Enter the folder path containing ARAMIS data files:")
        if folder_path and os.path.isdir(folder_path):
            st.success(f"Folder selected: {folder_path}")
            
            series_dict = analyze_files(folder_path)
            
            if not series_dict:
                st.warning("No valid series found in the selected folder.")
            else:
                
                selected_series = st.selectbox("Select a series to analyze:", list(series_dict.keys()))
                
                stages = series_dict[selected_series]
                
                if not stages:
                    st.warning(f"No valid stages found for the selected series: {selected_series}")
                else:
                    substages = [substage for _, substage, _ in stages]
                    min_substage, max_substage = min(substages), max(substages)
                    
                    # Updated to start from substage 4
                    start_substage, end_substage = st.slider("Select time range (s)", 0, max_substage, (4, max_substage))
                    
                    st.sidebar.header("Analysis Parameters")
                    
                    with st.sidebar.expander("Position Parameters"):
                        a = st.number_input("a", value=-2)
                        b = st.number_input("b", value=0)
                        ytop = st.number_input("ytop", value=15+b)
                        ybot = st.number_input("ybot", value=-15+b)
                        xtop = st.number_input("xtop", value=0+a)
                        xbot = st.number_input("xbot", value=0+a)
                        yleft = st.number_input("yleft", value=0+b)
                        yright = st.number_input("yright", value=0+b)
                        xleft = st.number_input("xleft", value=-3.5+a)
                        xright = st.number_input("xright", value=3.5+a)
                    
                    params = {
                        'ytop': ytop, 'ybot': ybot, 'xtop': xtop, 'xbot': xbot,
                        'yleft': yleft, 'yright': yright, 'xleft': xleft, 'xright': xright
                    }

                    strain_method = st.sidebar.selectbox("Select strain calculation method:", 
                                ['Engineering', 'Average', 'Maximum', 'True', 'Green-Lagrange'])
                    # Add expander with ARAMIS strain calculation explanation
                    with st.sidebar.expander("ARAMIS Strain Calculation Methods"):
                        st.markdown("""
                        # ARAMIS Strain Calculation Methods

                        1. **Engineering Strain**:
                        - ε = (L - L₀) / L₀
                        - Simplest method, good for small deformations
                        - Assumes uniform deformation

                        2. **Average Strain**:
                        - Calculates average strain across gauge area
                        - Useful for non-uniform deformations

                        3. **Maximum Strain**:
                        - Identifies point of maximum deformation
                        - Important for failure analysis

                        4. **True Strain**:
                        - ε = ln(L / L₀)
                        - Accurate for large deformations
                        - Accounts for continuous length change

                        5. **Green-Lagrange Strain**:
                        - ε = 0.5 * ((L / L₀)² - 1)
                        - Accounts for stretching and rotation
                        - Suitable for large, complex deformations

                        Choose the method that best suits your material and test conditions.
                        """)
                    # Load and analyze ARAMIS data
                    aramis_results = load_and_analyze_data(folder_path, selected_series, start_substage, end_substage, params, strain_method.lower())
                    
                    if aramis_results is not None:
                        
                        
                        # File selection for strain distribution plot (sorted)
                        files = [file for _, _, file in stages if file.startswith(selected_series) and file.endswith('.txt')]
                        selected_file = st.selectbox("Select file for strain distribution plot:", files)
                        
                        # Parameter selection
                        available_parameters = ['ex', 'ey', 'exy', 'ema', 'emi']
                        selected_parameter = st.selectbox("Select parameter for visualization:", available_parameters, index=1)  # Default to 'ey'
                        
                        # Dynamic contrast control with adjustable range
                        with st.sidebar.expander("Contrast Control"):
                            contrast_range = st.slider("Contrast Range", -10.0, 10.0, (-2.0, 2.0), 0.01)
                            contrast_min = st.slider("Contrast Min", contrast_range[0], contrast_range[1], contrast_range[0], 0.01)
                            contrast_max = st.slider("Contrast Max", contrast_range[0], contrast_range[1], contrast_range[1], 0.01)
                        
                        

                        # Update session state
                        st.session_state.contrast_min = contrast_min
                        st.session_state.contrast_max = contrast_max
                        
                        if selected_file:
                            file_data = fileprep(os.path.join(folder_path, selected_file))
                            fig1 = create_strain_distribution_plot(file_data, params, selected_parameter)
                            st.plotly_chart(fig1)
                        
                        # 3D plotting
                        show_3d = st.checkbox("Show 3D Strain Distribution")
                        if show_3d:
                            file_data_list = [fileprep(os.path.join(folder_path, file)) for file in files]
                            fig_3d = create_3d_strain_plot(file_data_list, params, selected_parameter)
                            st.plotly_chart(fig_3d)
                        
                        fig_gauge, fig_poisson = create_analysis_plots(aramis_results)
                        st.plotly_chart(fig_gauge)
                        #st.plotly_chart(fig_poisson)

                        st.write("ARAMIS Analysis Results:")
                        st.write(f"Time period analyzed: {len(aramis_results['StrainOnG'])} seconds")
                        st.write(f"Final Gauge Strain: {aramis_results['StrainOnG'][-1]*100:.2f}%")
                        st.write(f"Final Transverse Strain: {aramis_results['StrainGtrans'][-1]*100:.2f}%")
                        st.write(f"Final Poisson's Ratio: {aramis_results['Poisson'][-1]:.3f}")

                        analyze_poisson_ratio(aramis_results)
                        
                        
                        strain_plot = create_strain_plot(aramis_results)
                        st.plotly_chart(strain_plot)

                        # Instron data analysis
                        st.sidebar.subheader("Instron Data Analysis")
                        instron_file = st.sidebar.file_uploader("Upload Instron data file (CSV)", type="csv")
                        stress_analysis_results = None
                        
                        if instron_file is not None:

                            align_method = st.sidebar.selectbox("Select alignment method:", ["max", "start"], index=0)

                            data_source = st.sidebar.selectbox("Select data source for stress-strain analysis:", ["aramis", "instron", "both"])

                            instron_data = load_instron_data(instron_file)
                            
                            with st.sidebar.expander("Sample Dimensions"):
                                width = st.number_input("Sample width (mm)", value=20.0, step=0.01)
                                thickness = st.number_input("Sample thickness (mm)", value=0.32, step=0.01)
                                length = st.number_input("Sample length (mm)", value=100.0, step=0.01)
                            
                            # Plot Instron data
                            fig_instron = create_instron_plot(instron_data)
                            st.plotly_chart(fig_instron)
                            

                            # Perform stress analysis
                            aramis_time = np.arange(len(aramis_results['StrainOnG']))

                            stress_analysis_results=perform_stress_analysis(
                                aramis_results['StrainOnG'], 
                                aramis_time, 
                                instron_data, 
                                width, 
                                thickness, 
                                length,
                                data_source=data_source,
                                align_method=align_method
                            )

                            if data_source == 'aramis':

                                st.write("ARAMIS Data Analysis:")
                                st.write(f"Young's Modulus (Linear Fit): {stress_analysis_results['E1_aramis_linear']:.2f} MPa")
                                st.write(f"Young's Modulus (Polynomial Fit): {stress_analysis_results['E1_aramis_poly']:.2f} MPa")
                                st.write(f"Maximum Stress: {stress_analysis_results['max_stress_aramis']:.2f} MPa")

                            elif data_source == 'instron':
                                    

                                st.write("\nInstron Data Analysis:")
                                st.write(f"Young's Modulus (Linear Fit): {stress_analysis_results['E1_instron_linear']:.2f} MPa")
                                st.write(f"Young's Modulus (Polynomial Fit): {stress_analysis_results['E1_instron_poly']:.2f} MPa")
                                st.write(f"Maximum Stress: {stress_analysis_results['max_stress_instron']:.2f} MPa")

                            else:
                                st.write("ARAMIS Data Analysis:")
                                st.write(f"Young's Modulus (Linear Fit): {stress_analysis_results['E1_aramis_linear']:.2f} MPa")
                                st.write(f"Young's Modulus (Polynomial Fit): {stress_analysis_results['E1_aramis_poly']:.2f} MPa")
                                st.write(f"Maximum Stress: {stress_analysis_results['max_stress_aramis']:.2f} MPa")

                                st.write("\nInstron Data Analysis:")
                                st.write(f"Young's Modulus (Linear Fit): {stress_analysis_results['E1_instron_linear']:.2f} MPa")
                                st.write(f"Young's Modulus (Polynomial Fit): {stress_analysis_results['E1_instron_poly']:.2f} MPa")
                                st.write(f"Maximum Stress: {stress_analysis_results['max_stress_instron']:.2f} MPa")

                            #st.write(f"Stiffness: {stress_analysis_results['stiffness']/1000:.2f} kN/mm ")

                            fig_stress_strain = create_stress_strain_plot(stress_analysis_results, data_source=data_source)
                            st.plotly_chart(fig_stress_strain)


                        # if stress_analysis_results is not None:
                        #     alignment_plot = create_alignment_plot(stress_analysis_results)
                        #     st.plotly_chart(alignment_plot)

                        if stress_analysis_results is not None:
                            display_strain_analysis(aramis_results, stress_analysis_results)

                            # Get the save location using the new function
                            save_path = get_save_location()
                            if st.button("Generate HTML Report"):
                                    if os.path.isdir(save_path):
                                        generate_pdf_report(
                                            aramis_results, 
                                            stress_analysis_results, 
                                            file_data, 
                                            params, 
                                            selected_parameter, 
                                            selected_series,
                                            width,
                                            thickness,
                                            length,
                                            instron_data, save_path  
                                        )

                    else:
                        st.error("Analysis failed. Please check the error messages above.")
        else:
            st.warning("Please enter a valid folder path.")

def main():
    parser = argparse.ArgumentParser(description="Shankar Dutt's Carbon Fibre Strength Testing Platform")
    parser.add_argument('--streamlit', action='store_true', help='Run as a Streamlit app')
    args = parser.parse_args()

    if args.streamlit or not sys.argv[0].endswith('sdcf'):
        # This block will be executed when run as a module (python -m sdcf) or with --streamlit flag
        import streamlit.web.bootstrap as bootstrap
        bootstrap.run(__file__, '', [], {})
    else:
        print("Command-line functionality not implemented yet.")
        print("To run the Streamlit app, use: sdcf --streamlit")

if __name__ == "__main__":
    run_app()