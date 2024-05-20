from backbone_classes import *
from events.oldEvents import *
from events.restaurantEvents import *
from events.events import *
from events.health_events import *
from events.law_events import *
from events.love_events import *
from events.generatedEvents import *

from path_finding import *
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

import pandas as pd

import pandas as pd

def get_column_data(csv_filename):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_filename, header=None)

    # Transpose the DataFrame to get columns as rows
    transposed_df = df.transpose()

    # Convert the transposed DataFrame to a list of lists
    column_data = transposed_df.values.tolist()

    return column_data

def analyze_each_column(csv_filename, print = True):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_filename, header=None)

    # Initialize lists to store statistics for each column
    min_values = []
    max_values = []
    median_values = []
    first_quartile_values = []
    third_quartile_values = []

    # Iterate over each column
    for col in range(df.shape[1]):
        # Get descriptive statistics for the current column
        column_stats = df.iloc[:, col].describe(percentiles=[.25, .75])

        # Extract relevant statistics
        min_values.append(np.nanmin(column_stats))  # Use np.nanmin to ignore NaN values
        max_values.append(column_stats.loc['max'])  # describe handles NaN correctly for max
        median_values.append(np.nanmedian(column_stats))  # Use np.nanmedian to handle NaN in median
        first_quartile_values.append(
            np.nanpercentile(column_stats, 25))  # Use np.nanpercentile to handle NaN in quartiles
        third_quartile_values.append(
            np.nanpercentile(column_stats, 75))  # Use np.nanpercentile to handle NaN in quartiles

    if print:
        # Display the results
        for i in range(len(min_values)):
            print(f"\nColumn {i + 1} Statistics:")
            print("Min Value:", min_values[i])
            print("Max Value:", max_values[i])
            print("Median Value:", median_values[i])
            print("First Quartile Value (25th Percentile):", first_quartile_values[i])
            print("Third Quartile Value (75th Percentile):", third_quartile_values[i])
    else:
        return min_values, max_values, median_values, first_quartile_values, third_quartile_values

def replaceZeroes(data):
    # Use nested list comprehension to replace "0" with None starting from the second row
    updated_data = [
        [value if row_index == 0 or value != 0 else np.NaN for value in row]
        for row_index, row in enumerate(data)
    ]
    return updated_data

if __name__ == "__main__":

    # Target line data
    # Drama curve Initialization
    params = [[2.6, 6], [2, 13]]
    testCurve = DramaCurve(2, params, 16, 70)

    #params = [[5.5, 8], [2.5, 13]]
    #testCurve = DramaCurve(2, params, 16, 70)
    targets = testCurve.getDramaTargets()

    #csv_filename = 'dramaValues_0.4_15_70_penalize_incomplete.csv'
    #csv_filename = 'dramaValues_1_15_70_penalize_incomplete_no_cost.csv'
    #csv_filename = 'dramaValues_0.4_15_70.csv'
    #csv_filename = 'dramaValues_1_15_70.csv'
    #csv_filename = 'dramaValues_0.35_15_70.csv'
    #csv_filename = 'randomDramaWalk.csv'
    #csv_filename = 'Saved Drama Data/dramaValues_2_15_70_penalize_incomplete_no_cost_0.6.csv'
    csv_filename = 'FDG2024Demo.csv'


    currDramaData = get_column_data(csv_filename)
    currDramaData = replaceZeroes(currDramaData)
    dramaBoxPlotData = analyze_each_column(csv_filename, False)
    minValues = dramaBoxPlotData[0]
    maxValues = dramaBoxPlotData[1]
    medianValues = dramaBoxPlotData[2]
    firstQuarterValues = dramaBoxPlotData[3]
    thirdQuarterValues = dramaBoxPlotData[4]

    fig = plt.figure(figsize=(12, 10))

    # Creating axes instance
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

    sns.boxplot(data=currDramaData, notch=False)

    # Creating plot
    #bp = ax.boxplot(currDramaData, notch=False, vert=True, patch_artist=True)

    ax.yaxis.grid(True)

    colors = ['red']
#    for patch, color in zip(bp['boxes'], colors):
 #       patch.set_facecolor(color)

    xVals = np.arange(start=1, stop=16+1)
    plt.plot(xVals, targets, color="red", label='Target Drama Curve') #Target

    ax.set_xlabel('Plot Fragment Index')
    ax.set_ylabel('Drama Level')

    legend_elements = [Line2D([0], [0], color='red', lw=4, label='Target Drama Values'),
                       Patch(facecolor=sns.desaturate('blue', .5), edgecolor='grey', linewidth=1.5,
                             label='Produced Drama Values')]
    #legend_elements = [Patch(facecolor=sns.desaturate('blue', .5), edgecolor='grey', linewidth=1.5,
                             #label='Produced Drama Values')]
    ax.legend(handles=legend_elements, fontsize='xx-large')
    # Set x-axis limits
    ax.set_ylim(-35, 125)
    ax.set_xlim(-0.5, 15.5)# Adjust the upper limit as needed

    # show plot
    plt.show()


    xVals = np.arange(start=1, stop=16)
    plt.title("Drama Vals")
    plt.plot(xVals, medianValues, color="red") #current
    plt.plot(xVals, maxValues, color="blue") #upper bound
    plt.plot(xVals, minValues, color="blue") #Lower bound

    plt.show()
    #plt.plot(xVals, targets, color="green") #Target