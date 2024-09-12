import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_cor(df, main='Correlation Matrix', subplot=None):
    """
    Generates a heatmap for the correlation matrix of a DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame for which to compute the correlation matrix.
        main (str, optional): Main title of the plot.
        xlab (str, optional): Label for the x-axis.
        ylab (str, optional): Label for the y-axis.

    Returns:
        None. Displays the heatmap.
    """
    # Calculate the correlation matrix
    corr_matrix = df.corr()

    # Set the diagonal elements to NaN to make them white
    np.fill_diagonal(corr_matrix.values, np.nan)

    # Create a custom colormap with black for NaN values
    cmap = sns.color_palette("coolwarm", as_cmap=True)
    cmap.set_bad(color='black')

    # Draw the heatmap
    sns.heatmap(corr_matrix, annot=True, cmap=cmap, vmax=1, vmin=-1, square=True, linewidths=.5)

    # Add main title
    plt.title(main, fontsize=18)

    # Rotate the tick labels for better readability
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)

    # Show the plot if subplot is not specified
    if subplot is None:
        plt.show()
        plt.clf()
        plt.close()
