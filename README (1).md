# Euler's Method Differential Equation Solver

A Streamlit web application that implements Euler's method for solving first-order differential equations of the form dy/dx = ky.

## Features

- **Interactive Interface**: Easy-to-use web interface for entering parameters
- **Step-by-Step Calculations**: Shows detailed calculations for each step
- **Visual Comparison**: Graphs comparing Euler's method with the analytical solution
- **Error Analysis**: Displays absolute and relative errors
- **Educational Content**: Includes explanations about Euler's method

## Installation

1. Make sure you have Python 3.11 or higher installed
2. Install the required dependencies:
   ```bash
   pip install streamlit numpy pandas matplotlib
   ```

## Usage

1. Run the application:
   ```bash
   streamlit run app.py
   ```

2. Open your web browser and navigate to the displayed URL (usually http://localhost:8501)

3. Enter your parameters:
   - **k**: The constant in the differential equation dy/dx = ky
   - **Initial x value (x₀)**: The starting x coordinate
   - **Initial y value (y₀)**: The starting y coordinate
   - **Target x value**: The x value to stop the calculation at
   - **Step size (h)**: The step size for Euler's method

4. Click "Calculate Using Euler's Method" to see the results

## What the App Shows

- **Step-by-Step Table**: Shows each calculation step with x, y, dy/dx, and Δy values
- **Graph**: Visual comparison between Euler's method and the analytical solution
- **Error Analysis**: Table showing absolute and relative errors at each step
- **Summary Metrics**: Final values and maximum errors

## Example

For the differential equation dy/dx = 0.1y with initial condition (0, 1):
- The analytical solution is y = e^(0.1x)
- Euler's method approximates this by taking small steps
- Smaller step sizes give more accurate results

## Files

- `app.py`: Main application file
- `.streamlit/config.toml`: Streamlit configuration
- `pyproject.toml`: Python project dependencies
- `README.md`: This file

## Educational Use

This app is perfect for:
- Learning about numerical methods
- Understanding how Euler's method works
- Seeing the difference between numerical and analytical solutions
- Experimenting with different step sizes and their effects on accuracy