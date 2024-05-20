import csv
import matplotlib.pyplot as plt
import numpy as np

def display_dot_plot_from_csv(csv_filename):
    data = []

    # Read the data from the CSV file
    with open(csv_filename, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            data.append([int(value) for value in row])

    if not data:
        print("The CSV file is empty or does not contain valid data.")
        return

    # Create a dot plot
    plt.figure(figsize=(10, 5))  # Adjust the figure size as needed
    plt.plot(np.arange(len(data[0])), data[0], 'bo', label='Data')  # Plot the first line of data as blue dots

    # Customize the plot if needed (e.g., set labels, titles, etc.)
    plt.xlabel('Data Point Index')
    plt.ylabel('Values')
    plt.title('Dot Plot of Data')

    # Show the plot
    plt.legend()
    plt.grid()
    plt.show()

# Specify the CSV file containing lines of 15 integers
csv_filename = 'Saved Drama Data/dramaValues.csv'

# Call the function to display the dot plot
display_dot_plot_from_csv(csv_filename)

def showcase_means_from_csv(csv_filename):
    x_values = []
    y_values = []

    # Read the data from the CSV file
    with open(csv_filename, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) == 2:
                x, y = map(float, row)
                x_values.append(x)
                y_values.append(y)

    if not x_values or not y_values:
        print("The CSV file is empty or does not contain valid data.")
        return

    # Calculate the mean of the y-values
    y_mean = sum(y_values) / len(y_values)

    # Create a bar chart to showcase the mean
    plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
    plt.bar(x_values, y_values, label='Y Values', alpha=0.6)
    plt.axhline(y=y_mean, color='red', linestyle='--', label=f'Mean Y Value: {y_mean:.2f}')

    # Customize the plot
    plt.xlabel('X Values')
    plt.ylabel('Y Values')
    plt.title('Means of Y Values')
    plt.legend()

    # Show the plot
    plt.grid()
    plt.show()

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# Specify the CSV file containing X and Y values
csv_filename = 'Saved Drama Data/alpha+visitedStatesCorrectedSimple.csv'
# Load data from CSV into a DataFrame
data = pd.read_csv(csv_filename, header=None, names=['P Value', 'Explored Worldstates'])

# Create a scatter plot using Seaborn
sns.scatterplot(x='P Value', y='Explored Worldstates', data=data)

# Set labels for axes
plt.xlabel("$P$ Value")
plt.ylabel('Explored Worldstates')
fig = plt.figure(figsize=(12, 10))
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
ax.set_ylim(-1000, 12000)
ax.set_xlim(-0.1, 1.1)

# Show the plot
plt.show()





