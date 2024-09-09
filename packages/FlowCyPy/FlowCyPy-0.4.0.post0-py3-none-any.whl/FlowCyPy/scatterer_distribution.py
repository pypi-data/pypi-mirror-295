from typing import List, Optional, Tuple
import matplotlib.pyplot as plt
from MPSPlots.styles import mps
from dataclasses import dataclass
import numpy as np
from FlowCyPy.distribution import Distribution
from FlowCyPy import ureg

@dataclass
class ScattererDistribution:
    """
    A class to define and analyze the size and position distribution of scatterers (particles) passing through a flow cytometer.

    The class combines multiple distributions (normal, lognormal, uniform, or singular), each with its own scaling factor,
    to generate particle sizes. The total distribution of particle sizes is the combination of these distributions.

    Attributes
    ----------
    flow: object
        The flow setup used for generating longitudinal positions.
    refractive_index: float
        The refractive index of the particles.
    distributions: List[Distribution]
        List of distribution objects that define the size distributions (Normal, LogNormal, etc.).
    coupling_factor: str, optional
        The type of coupling factor to generate ('rayleigh', 'uniform'). Default is 'rayleigh'.
    """

    flow: object  # Flow object that defines flow properties
    refractive_index: float  # Refractive index of the particles
    distributions: List[Distribution]  # List of distribution objects (Normal, LogNormal, etc.)
    coupling_factor: Optional[str] = 'rayleigh'  # Coupling factor type: 'rayleigh', 'uniform'

    def __post_init__(self) -> None:
        """Initializes the scatterer distribution and generates particle sizes."""
        self.sizes = None  # Placeholder for generated sizes
        self.initalize_samples(n_samples=self.flow.n_events)

    def initalize_samples(self, n_samples: int) -> None:
        """
        Generates random scatterer sizes from the provided distributions and combines them, taking scale factors into account.

        Parameters
        ----------
        n_samples : int
            The number of particle sizes to generate.
        """
        sizes = []
        for distribution in self.distributions:
            sizes.append(distribution.generate(n_samples))  # Generate sizes from each distribution

        # Combine all sizes from different distributions
        self.sizes = np.concatenate(sizes)

        self.sizes = np.random.choice(
            self.sizes.magnitude,
            size=n_samples.magnitude,
            replace=True,
            p=None
        ) * ureg.meter

    def get_pdf(self, sampling: Optional[int] = 1000) -> Tuple[np.ndarray, np.ndarray]:
        """
        Combines the PDFs of all provided distributions, applying their respective scale factors.

        This method calculates the combined probability density function (PDF) for the particle sizes generated
        from all distributions.

        Parameters
        ----------
        sampling : int, optional
            The number of points to sample for plotting the continuous PDF (default is 1000).

        Returns
        -------
        x : np.ndarray
            The x-values (particle sizes) for the combined PDF.
        pdf : np.ndarray
            The combined PDF values corresponding to the x-values.
        """
        if self.sizes is None:
            raise ValueError("Sizes have not been generated. Use 'initalize_samples()' first.")

        # Generate x-values for the PDF
        x = np.linspace(self.sizes.min(), self.sizes.max(), sampling).magnitude

        # Combine the PDFs of all distributions, applying scale factors
        pdf = np.zeros_like(x)
        for distribution in self.distributions:
            _, dist_pdf = distribution.get_pdf(x)  # Get the PDF for each distribution
            pdf += dist_pdf  # Sum the PDFs from all distributions, accounting for scaling

        return x, pdf

    def plot(self, bins: Optional[int] = 50) -> None:
        """
        Plots the histogram of scatterer sizes and overlays the continuous probability density function (PDF).

        The method uses the combined sizes from all distributions and plots a histogram of the generated sizes
        with the corresponding PDF.

        Parameters
        ----------
        bins : int, optional
            The number of bins for the histogram (default is 50).
        """
        with plt.style.context(mps):
            fig, ax = plt.subplots(1, 1, figsize=(8, 5))
            self._add_to_ax(ax=ax, bins=bins)
            plt.show()

    def _add_to_ax(self, ax: plt.Axes, bins: Optional[int] = 50) -> None:
        """
        Plots the histogram of scatterer sizes and overlays the PDF.

        Parameters
        ----------
        ax : plt.Axes
            The matplotlib axis where the plot will be drawn.
        bins : int, optional
            The number of bins for the histogram (default is 50).
        """
        if self.sizes is None:
            raise ValueError("Scatterer sizes have not been generated. Use 'initalize_samples()' first.")

        # Plot the histogram of sampled data
        counts, bin_edges, _ = ax.hist(
            self.sizes.magnitude,  # Convert to magnitudes (i.e., numerical values without units)
            bins=bins,
            edgecolor='black',
            alpha=0.7,
            label='Sampled Data'
        )

        # Plot the continuous PDF behind the histogram
        x_pdf, pdf = self.get_pdf()
        bin_width = bin_edges[1] - bin_edges[0]
        pdf_scaled = pdf * len(self.sizes) * bin_width

        ax_ = ax.twinx()
        ax_.plot(x_pdf, pdf_scaled, color='red', lw=2, label='PDF', zorder=0)
        ax_.axis('off')

        # Set labels and legend
        ax.set(title='Size Distribution of Scatterers', xlabel='Size [meters]', ylabel='Frequency')
        ax.legend()

    def print_properties(self) -> None:
        """
        Prints the core properties of the scatterer distribution and flow cytometer setup using `tabulate`.

        This method includes properties such as the number of events, mean size, and distribution type.
        """
        from tabulate import tabulate

        # Gather flow properties
        self.flow.print_properties()

        # Gather scatterer distribution properties
        properties = [
            ["Refractive Index", f"{self.refractive_index}"],
            ["Mean Size (all distributions)", f"{np.mean(self.sizes):.2e~#P}"],
            ["Number of Events", f"{len(self.sizes)}"],
        ]

        print("\nScatterers Properties")
        print(tabulate(properties, headers=["Property", "Value"], tablefmt="grid"))
