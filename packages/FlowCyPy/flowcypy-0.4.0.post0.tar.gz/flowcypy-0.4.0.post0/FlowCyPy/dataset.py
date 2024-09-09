import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
from dataclasses import dataclass


@dataclass
class DataSet:
    """
    A dataclass to store features extracted from signal peaks.

    Attributes:
    ----------
    height : np.ndarray
        Array of peak heights.
    width : np.ndarray
        Array of peak widths.
    area : np.ndarray
        Array of areas under each peak.
    time : np.ndarray
        Array of times at which peaks occur.
    """
    height: np.ndarray = None
    width: np.ndarray = None
    area: np.ndarray = None
    time: np.ndarray = None

    def __iter__(self):
        """
        Iterator that yields one peak's features at a time.

        Returns:
        -------
        tuple
            A tuple containing (time, height, width, area) for each peak.
        """
        self._index = 0  # Initialize the index for iteration
        return self

    def __next__(self):
        """
        Returns the next peak's features during iteration.

        Raises:
        -------
        StopIteration
            Raised when all peaks have been iterated over.

        Returns:
        -------
        tuple
            A tuple containing (time, height, width, area) for the current peak.
        """
        if self._index >= len(self.time):
            raise StopIteration

        peak_data = (
            self.time[self._index],
            self.height[self._index],
            self.width[self._index],
            self.area[self._index] if self.area is not None else None
        )
        self._index += 1
        return peak_data

    def _add_to_ax(self, ax: plt.Axes, t_time: np.ndarray, signal: np.ndarray) -> None:
        """
        Add the peak information to a matplotlib axis.

        Parameters:
        ----------
        ax : plt.Axes
            The matplotlib axis where the plot will be added.
        t_time : np.ndarray
            Time axis for the signal.
        signal : np.ndarray
            Signal values to plot.
        """
        for time, width in zip(self.time, self.width):
            where = (t_time >= time - width / 2) & (t_time <= time + width / 2)
            ax.fill_between(
                x=t_time.magnitude,
                y1=0,
                y2=signal.magnitude,
                where=where,
                color='red',
                alpha=0.3,
                label='Width at Half-Max'
            )

    def print_properties(self) -> None:
        """
        Displays extracted peak features in a tabular format.
        Handles the case where 'self.area' might be None.
        """
        headers = ["Peak", "Time [s]", "Height", "Width", "Area"]
        table = []

        # If area is None, fill the 'area' column with 'Not calculated'
        if self.area is None:
            for idx, (time, height, width) in enumerate(zip(self.time, self.height, self.width)):
                table.append([
                    idx + 1,  # Peak number
                    f"{time:.2f~#P}",  # Time in scientific notation
                    f"{height:.2f~#P}",  # Height in scientific notation
                    f"{width:.2f~#P}",  # Width in scientific notation
                    "Not calculated"  # Area (if not available)
                ])
        else:
            # Iterate over time, height, width, and area if area is available
            for idx, (time, height, width, area) in enumerate(zip(self.time, self.height, self.width, self.area)):
                table.append([
                    idx + 1,  # Peak number
                    f"{time:.2f~#P}",  # Time in scientific notation
                    f"{height:.2f~#P}",  # Height in scientific notation
                    f"{width:.2f~#P}",  # Width in scientific notation
                    f"{area:.2f~#P}"  # Area (if available)
                ])

        # Print the table using tabulate
        print(tabulate(table, headers=headers, tablefmt="grid"))
