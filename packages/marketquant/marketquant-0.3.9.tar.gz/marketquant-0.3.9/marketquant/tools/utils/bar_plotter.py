import matplotlib.pyplot as plt
import pandas as pd

class BarPlotter:
    def __init__(self, dataframe: pd.DataFrame, x_col: str, y_col: str):
        """
        Initialize the BarChartPlotter with the given DataFrame and column names.
        :param dataframe: A pandas DataFrame containing the data.
        :param x_col: The column name for the x-axis (e.g., 'strikePrice').
        :param y_col: The column name for the y-axis (e.g., 'gammaExposure').
        """
        self.dataframe = dataframe
        self.x_col = x_col
        self.y_col = y_col

    def validate_data(self):
        """
        Validate if the DataFrame contains the required columns.
        :return: True if valid, False otherwise.
        """
        required_columns = {self.x_col, self.y_col}
        if required_columns.issubset(self.dataframe.columns):
            print("Data validation successful. The DataFrame contains the required columns.")
            return True
        else:
            missing_columns = required_columns - set(self.dataframe.columns)
            print(f"Data validation failed. Missing columns: {missing_columns}")
            return False

    def plot_barchart(self, positive_color='blue', negative_color='red', title=" ", line_data=None, line_color='green'):
        """
        Plot a bar chart with customizable colors for positive and negative y-values, and optional line data.
        :param positive_color: Color for positive values (default: 'blue').
        :param negative_color: Color for negative values (default: 'red').
        :param title: Title of the bar chart.
        :param line_data: Optional dictionary with keys as x-values and values as line y-values.
        :param line_color: Color of the line (default: 'green').
        """
        if not self.validate_data():
            return

        positive_data = self.dataframe[self.dataframe[self.y_col] >= 0]
        negative_data = self.dataframe[self.dataframe[self.y_col] < 0]

        plt.figure(figsize=(10, 6))
        plt.bar(positive_data[self.x_col], positive_data[self.y_col], color=positive_color, label='Positive')
        plt.bar(negative_data[self.x_col], negative_data[self.y_col], color=negative_color, label='Negative')

        if line_data:
            plt.plot(list(line_data.keys()), list(line_data.values()), color=line_color, label='Line Data', linewidth=2)

        plt.axhline(0, color='black', linewidth=1.5)
        plt.title(title)
        plt.xlabel(self.x_col)
        plt.ylabel(self.y_col)
        plt.legend()

        plt.show()

    def confirm_valid_data(self):
        """
        Confirms that the data is in the correct format for plotting.
        """
        return self.validate_data()
