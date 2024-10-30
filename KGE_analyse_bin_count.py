import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Define file path
results_file = '/Users/tomdeboer/Documents/Universiteit/Master/Scriptie/Scriptie_240408_Tom_de_Boer/developing/output/kge_results/kge_results_top_layer_additive_bias_correction.csv'

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

# Define the bins
bins_kge = [-5, -4, -3, -2, -1.5, -1.0, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1, 2, 3, 5]
bins_general = 20  # Number of bins for other metrics

# Plotting settings
fig, axs = plt.subplots(2, 2, figsize=(15, 10), facecolor='#f7f7f7')
fig.suptitle('Histograms of KGE and Components from Top Layer', fontsize=20, fontweight='bold')

# Font sizes for customization
title_fontsize = 20
label_fontsize = 16
tick_fontsize = 15

# Custom styling options
bar_color = '#4c72b0'
edge_color = 'black'
alpha_value = 0.7

# Function to print the number of entries per bin
def print_bin_counts(values, bins, metric_name):
    counts, bin_edges = np.histogram(values, bins=bins)
    print(f"\nBin counts for {metric_name}:")
    for count, edge_start, edge_end in zip(counts, bin_edges[:-1], bin_edges[1:]):
        print(f"Bin [{edge_start:.2f}, {edge_end:.2f}]: {count} entries")

# Plot histogram for KGE
axs[0, 0].hist(results_df['kge'], bins=bins_kge, color=bar_color, edgecolor=edge_color, alpha=alpha_value)
axs[0, 0].axvline(-0.41, color='red', linestyle='dashed', linewidth=2)  # Highlight important KGE value
axs[0, 0].set_title('KGE', fontsize=title_fontsize)
axs[0, 0].set_xlabel('KGE', fontsize=label_fontsize)
axs[0, 0].set_ylabel('Frequency', fontsize=label_fontsize)
print_bin_counts(results_df['kge'], bins_kge, "KGE")

# Plot histogram for Correlation
axs[0, 1].hist(results_df['correlation'], bins=bins_general, color=bar_color, edgecolor=edge_color, alpha=alpha_value)
axs[0, 1].set_title('Correlation', fontsize=title_fontsize)
axs[0, 1].set_xlabel('Correlation', fontsize=label_fontsize)
axs[0, 1].set_ylabel('Frequency', fontsize=label_fontsize)
print_bin_counts(results_df['correlation'], bins_general, "Correlation")

# Plot histogram for Bias
axs[1, 0].hist(results_df['bias'], bins=bins_general, color=bar_color, edgecolor=edge_color, alpha=alpha_value)
axs[1, 0].set_title('Bias', fontsize=title_fontsize)
axs[1, 0].set_xlabel('Bias', fontsize=label_fontsize)
axs[1, 0].set_ylabel('Frequency', fontsize=label_fontsize)
print_bin_counts(results_df['bias'], bins_general, "Bias")

# Plot histogram for Variability
axs[1, 1].hist(results_df['variability'], bins=bins_general, color=bar_color, edgecolor=edge_color, alpha=alpha_value)
axs[1, 1].set_title('Variability', fontsize=title_fontsize)
axs[1, 1].set_xlabel('Variability', fontsize=label_fontsize)
axs[1, 1].set_ylabel('Frequency', fontsize=label_fontsize)
print_bin_counts(results_df['variability'], bins_general, "Variability")

# Customizing ticks
for ax in axs.flat:
    ax.tick_params(axis='both', which='major', labelsize=tick_fontsize)
    ax.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()