import pandas as pd
import matplotlib.pyplot as plt

# Define file path
results_file = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/important_data/input/tables/kge_results/kge_bottom_layer_results_cor_bias_var.csv'

# Load the results data
results_df = pd.read_csv(results_file)

# Function to remove brackets and convert to float
def remove_brackets(x):
    if isinstance(x, str):
        return float(x.strip('[]'))
    return x

# Apply the function to the relevant columns
results_df['kge'] = results_df['kge'].apply(remove_brackets)
results_df['correlation'] = results_df['correlation'].apply(remove_brackets)
results_df['bias'] = results_df['bias'].apply(remove_brackets)
results_df['variability'] = results_df['variability'].apply(remove_brackets)

# Define the bins for KGE
bins_kge = [-float('inf'), -0.41, 0, 0.25, 0.5, 0.75, 1, float('inf')]

# Define the bins for correlation, bias, and variability
bins_other = [-float('inf'), -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2,float('inf')]

# Plotting
fig, axs = plt.subplots(2, 2, figsize=(15, 10))

# Plot histogram for KGE
axs[0, 0].hist(results_df['kge'], bins=bins_kge, edgecolor='black')
axs[0, 0].set_title('Histogram of KGE bottom_layer')
axs[0, 0].set_xlabel('KGE')
axs[0, 0].set_ylabel('Frequency')

# Plot histogram for Correlation
axs[0, 1].hist(results_df['correlation'], bins=bins_other, edgecolor='black')
axs[0, 1].set_title('Histogram of Correlation bottom_layer')
axs[0, 1].set_xlabel('Correlation')
axs[0, 1].set_ylabel('Frequency')

# Plot histogram for Bias
axs[1, 0].hist(results_df['bias'], bins=bins_other, edgecolor='black')
axs[1, 0].set_title('Histogram of Bias bottom_layer')
axs[1, 0].set_xlabel('Bias')
axs[1, 0].set_ylabel('Frequency')

# Plot histogram for Variability
axs[1, 1].hist(results_df['variability'], bins=bins_other, edgecolor='black')
axs[1, 1].set_title('Histogram of Variability bottom_layer')
axs[1, 1].set_xlabel('Variability')
axs[1, 1].set_ylabel('Frequency')

plt.tight_layout()
plt.show()