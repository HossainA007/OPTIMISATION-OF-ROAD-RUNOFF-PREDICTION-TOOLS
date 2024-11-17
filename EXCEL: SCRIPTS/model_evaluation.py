
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score

def evaluate_model(input_file, observed_file, coefficients_file):
    # Load input variables, observed outputs, and coefficients
    input_data = pd.read_excel(input_file)
    observed_output = pd.read_excel(observed_file)
    coefficients = pd.read_excel(coefficients_file)

    # Map coefficients to variables
    beta_0 = coefficients.loc[coefficients['Parameter'] == 'Beta_0', 'Value'].values[0]
    a = coefficients.loc[coefficients['Parameter'] == 'a', 'Value'].values[0]
    b = coefficients.loc[coefficients['Parameter'] == 'b', 'Value'].values[0]
    c = coefficients.loc[coefficients['Parameter'] == 'c', 'Value'].values[0]
    d = coefficients.loc[coefficients['Parameter'] == 'd', 'Value'].values[0]
    e = coefficients.loc[coefficients['Parameter'] == 'e', 'Value'].values[0]

    # Extract input variables
    DA = input_data['DA']
    DL = input_data['DL']
    IF = input_data['IF']
    Pannual = input_data['Pannual']
    AADT = input_data['AADT']

    # Compute predicted values using the model equation
    ln_predicted = beta_0 + (a * DA) + (b * DL) + (c * IF) + (d * Pannual) + (e * AADT)
    predicted = np.exp(ln_predicted)

    # Extract observed values
    observed = observed_output['Observed']

    # Ensure alignment of observed and predicted data
    observed = observed.reset_index(drop=True)
    predicted = pd.Series(predicted[:len(observed)]).reset_index(drop=True)

    # Compute evaluation metrics
    rmse = np.sqrt(mean_squared_error(observed, predicted))
    r2 = r2_score(observed, predicted)
    ens = 1 - (np.sum((observed - predicted)**2) / np.sum((observed - observed.mean())**2))

    # Plot observed vs. predicted values
    plt.figure(figsize=(8, 6))
    plt.scatter(observed, predicted, color='blue', label='Data Points')
    plt.plot([observed.min(), observed.max()], [observed.min(), observed.max()],
             color='red', linestyle='--', label='1:1 Line')
    plt.title('Observed vs. Predicted Values')
    plt.xlabel('Observed Values')
    plt.ylabel('Predicted Values')
    plt.legend()
    plt.grid(True)
    plt.text(observed.min(), observed.max() - 10,
             f"RMSE: {rmse:.2f}\nR²: {r2:.2f}\nENS: {ens:.2f}", fontsize=12,
             bbox=dict(facecolor='white', alpha=0.5))
    plt.show()

# Example usage
input_file = 'input_variables.xlsx'
observed_file = 'observed_output.xlsx'
coefficients_file = 'coefficients.xlsx'

evaluate_model(input_file, observed_file, coefficients_file)
