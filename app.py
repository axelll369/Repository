import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def euler_method(k, x0, y0, x_target, h):
    """
    Implements Euler's method for solving dy/dx = ky
    
    Parameters:
    k: constant in the differential equation
    x0: initial x value
    y0: initial y value
    x_target: target x value to stop at
    h: step size
    
    Returns:
    DataFrame with columns: step, x, y, dy_dx, delta_y
    """
    # Calculate number of steps
    n_steps = int((x_target - x0) / h)
    
    # Initialize arrays to store results
    steps = []
    x_values = []
    y_values = []
    dy_dx_values = []
    delta_y_values = []
    
    # Set initial values
    x = x0
    y = y0
    
    # Add initial point
    steps.append(0)
    x_values.append(x)
    y_values.append(y)
    dy_dx_values.append(k * y)
    delta_y_values.append(0)  # No change for initial point
    
    # Perform Euler's method iterations
    for i in range(1, n_steps + 1):
        # Calculate dy/dx at current point
        dy_dx = k * y
        
        # Calculate change in y
        delta_y = h * dy_dx
        
        # Update x and y
        x = x + h
        y = y + delta_y
        
        # Store results
        steps.append(i)
        x_values.append(x)
        y_values.append(y)
        dy_dx_values.append(dy_dx)
        delta_y_values.append(delta_y)
    
    # Create DataFrame
    results_df = pd.DataFrame({
        'Step': steps,
        'x': x_values,
        'y': y_values,
        'dy/dx': dy_dx_values,
        'Δy': delta_y_values
    })
    
    return results_df

def analytical_solution(k, x0, y0, x_values):
    """
    Calculate the analytical solution for dy/dx = ky
    The solution is y = y0 * e^(k*(x-x0))
    """
    return y0 * np.exp(k * (x_values - x0))

def main():
    st.title("Euler's Method for Differential Equations")
    st.markdown("### Solving dy/dx = ky using Euler's Method")
    
    st.markdown("""
    This application implements Euler's method to solve first-order differential equations 
    of the form **dy/dx = ky**, where the rate of change is directly proportional to the 
    amount present.
    """)
    
    # Create input sections
    st.header("Input Parameters")
    
    # Create two columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Differential Equation Parameters")
        k = st.number_input(
            "Constant k (in dy/dx = ky)", 
            value=0.1, 
            step=0.01,
            help="The proportionality constant in the differential equation"
        )
        
        st.subheader("Initial Conditions")
        x0 = st.number_input(
            "Initial x value (x₀)", 
            value=0.0, 
            step=0.1,
            help="The starting x coordinate"
        )
        y0 = st.number_input(
            "Initial y value (y₀)", 
            value=1.0, 
            step=0.1,
            help="The starting y coordinate"
        )
    
    with col2:
        st.subheader("Calculation Parameters")
        x_target = st.number_input(
            "Target x value", 
            value=2.0, 
            step=0.1,
            help="The x value to stop the calculation at"
        )
        h = st.number_input(
            "Step size (h)", 
            value=0.1, 
            min_value=0.001,
            max_value=1.0,
            step=0.01,
            help="The step size for Euler's method (smaller values give more accuracy)"
        )
    
    # Input validation
    if x_target <= x0:
        st.error("Target x value must be greater than initial x value")
        return
    
    if h <= 0:
        st.error("Step size must be positive")
        return
    
    # Calculate button
    if st.button("Calculate Using Euler's Method", type="primary"):
        
        # Perform Euler's method calculation
        try:
            results_df = euler_method(k, x0, y0, x_target, h)
            
            # Display results
            st.header("Results")
            
            # Show summary
            final_x = results_df['x'].iloc[-1]
            final_y = results_df['y'].iloc[-1]
            n_steps = len(results_df) - 1
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Final x value", f"{final_x:.4f}")
            with col2:
                st.metric("Final y value", f"{final_y:.4f}")
            with col3:
                st.metric("Number of steps", n_steps)
            
            # Display step-by-step calculations
            st.subheader("Step-by-Step Calculations")
            
            # Format the dataframe for better display
            display_df = results_df.copy()
            display_df['x'] = display_df['x'].round(4)
            display_df['y'] = display_df['y'].round(6)
            display_df['dy/dx'] = display_df['dy/dx'].round(6)
            display_df['Δy'] = display_df['Δy'].round(6)
            
            st.dataframe(display_df, use_container_width=True)
            
            # Create plot comparing Euler's method with analytical solution
            st.subheader("Graphical Comparison")
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Plot Euler's method results
            ax.plot(results_df['x'], results_df['y'], 'bo-', label="Euler's Method", linewidth=2, markersize=4)
            
            # Plot analytical solution
            x_analytical = np.linspace(x0, x_target, 1000)
            y_analytical = analytical_solution(k, x0, y0, x_analytical)
            ax.plot(x_analytical, y_analytical, 'r--', label='Analytical Solution', linewidth=2)
            
            # Formatting
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_title(f'Euler\'s Method vs Analytical Solution\ndy/dx = {k}y, Initial: ({x0}, {y0}), Step size: {h}')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            st.pyplot(fig)
            
            # Calculate and display error analysis
            st.subheader("Error Analysis")
            
            # Calculate analytical values at Euler's method points
            y_analytical_points = analytical_solution(k, x0, y0, results_df['x'])
            absolute_errors = np.abs(results_df['y'] - y_analytical_points)
            relative_errors = np.abs((results_df['y'] - y_analytical_points) / y_analytical_points) * 100
            
            error_df = pd.DataFrame({
                'x': results_df['x'],
                'Euler\'s Method': results_df['y'],
                'Analytical Solution': y_analytical_points,
                'Absolute Error': absolute_errors,
                'Relative Error (%)': relative_errors
            })
            
            # Round for display
            error_df = error_df.round(6)
            
            st.dataframe(error_df, use_container_width=True)
            
            # Show maximum error
            max_abs_error = absolute_errors.max()
            max_rel_error = relative_errors.max()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Maximum Absolute Error", f"{max_abs_error:.6f}")
            with col2:
                st.metric("Maximum Relative Error", f"{max_rel_error:.4f}%")
            
        except Exception as e:
            st.error(f"An error occurred during calculation: {str(e)}")
    
    # Add explanation section
    st.header("About Euler's Method")
    
    with st.expander("Method Explanation"):
        st.markdown("""
        **Euler's Method** is a numerical technique for solving first-order ordinary differential equations.
        
        For a differential equation of the form dy/dx = f(x,y), Euler's method uses the formula:
        
        **y(n+1) = y(n) + h × f(x(n), y(n))**
        
        Where:
        - h is the step size
        - f(x,y) is the derivative function
        
        For our specific case where dy/dx = ky:
        - f(x,y) = ky
        - So: y(n+1) = y(n) + h × k × y(n)
        
        The analytical solution for this differential equation is:
        **y = y₀ × e^(k×(x-x₀))**
        
        Euler's method approximates this solution by taking small steps and using the slope at each point
        to estimate the next point.
        """)
    
    with st.expander("Usage Tips"):
        st.markdown("""
        - **Smaller step sizes** generally give more accurate results but require more computation
        - **Positive k values** result in exponential growth
        - **Negative k values** result in exponential decay
        - **k = 0** results in a constant function
        - Try different step sizes to see how accuracy changes
        - The error typically accumulates over longer intervals
        """)

if __name__ == "__main__":
    main()
