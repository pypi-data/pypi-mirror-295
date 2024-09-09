from dataclasses import dataclass
import numpy as np
from typing import Optional, Tuple
from scipy.stats import norm, lognorm, uniform
from FlowCyPy import ureg

class Distribution:
    """
    Base class for distributions used to define particle sizes in the flow cytometer.

    This class provides a structure for generating random scatterer sizes based on different statistical distributions.
    Each subclass must implement the `generate` method to generate a distribution of sizes and `get_pdf` to compute the
    probability density function (PDF) values.

    Attributes
    ----------
    scale_factor : float
        A scaling factor applied to the PDF of the distribution. By default, it is set to 1 (equal weight).
    """

    scale_factor: Optional[float] = 1.0

    def generate(self, n_samples: int) -> np.ndarray:
        """Generate a distribution of scatterer sizes."""
        raise NotImplementedError("Must be implemented by subclasses")

    def get_pdf(self, x: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Compute the probability density function (PDF) values."""
        raise NotImplementedError("Must be implemented by subclasses")


@dataclass
class NormalDistribution(Distribution):
    """
    Represents a normal (Gaussian) distribution for particle sizes.

    The normal distribution is described by its mean and standard deviation:

    .. math::
        f(x) = \frac{1}{\sqrt{2 \pi \sigma^2}} \exp \left( - \frac{(x - \mu)^2}{2 \sigma^2} \right)

    where:
    - :math:`\mu` is the mean of the distribution (average particle size).
    - :math:`\sigma` is the standard deviation (width of the distribution).
    - :math:`x` represents particle sizes.

    Attributes
    ----------
    mean : float
        The mean (average) particle size in meters.
    std_dev : float
        The standard deviation of particle sizes in meters.
    scale_factor : float, optional
        A scaling factor applied to the PDF (not the sizes).
    """

    mean: float
    std_dev: float
    scale_factor: float = 1.0

    def generate(self, n_samples: int) -> np.ndarray:
        """
        Generates a normal distribution of scatterer sizes.

        The generated sizes are based on the normal distribution's mean and standard deviation.

        Parameters
        ----------
        n_samples : int
            The number of particle sizes to generate.

        Returns
        -------
        np.ndarray
            An array of scatterer sizes in meters.
        """
        return np.random.normal(self.mean, self.std_dev, n_samples.magnitude) * ureg.meter

    def get_pdf(self, x: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Returns the x-values and the scaled PDF values for the normal distribution.

        The `scale_factor` is applied to the PDF, not the generated sizes.

        Parameters
        ----------
        x : np.ndarray
            The input x-values (particle sizes) over which to compute the PDF.

        Returns
        -------
        Tuple[np.ndarray, np.ndarray]
            The input x-values and the corresponding scaled PDF values.
        """
        pdf = norm.pdf(x, loc=self.mean, scale=self.std_dev)
        return x, self.scale_factor * pdf


@dataclass
class LogNormalDistribution(Distribution):
    """
    Represents a log-normal distribution for particle sizes.

    The log-normal distribution is described by its mean and standard deviation of the logarithm of the values:

    .. math::
        f(x) = \frac{1}{x \sigma \sqrt{2 \pi}} \exp \left( - \frac{(\ln(x) - \mu)^2}{2 \sigma^2} \right)

    where:
    - :math:`\mu` is the mean of the natural logarithm of the particle sizes.
    - :math:`\sigma` is the standard deviation of the logarithm of particle sizes.

    Attributes
    ----------
    mean : float
        The mean particle size in meters.
    std_dev : float
        The standard deviation of the logarithm of particle sizes.
    scale_factor : float, optional
        A scaling factor applied to the PDF (not the sizes).
    """

    mean: float
    std_dev: float
    scale_factor: float = 1.0

    def generate(self, n_samples: int) -> np.ndarray:
        """
        Generates a log-normal distribution of scatterer sizes.

        The generated sizes follow a log-normal distribution, where the logarithm of the sizes is normally distributed.

        Parameters
        ----------
        n_samples : int
            The number of particle sizes to generate.

        Returns
        -------
        np.ndarray
            An array of scatterer sizes in meters.
        """
        return np.random.lognormal(np.log(self.mean), self.std_dev, n_samples.magnitude) * ureg.meter

    def get_pdf(self, x: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Returns the x-values and the scaled PDF values for the log-normal distribution.

        The `scale_factor` is applied to the PDF, not the generated sizes.

        Parameters
        ----------
        x : np.ndarray
            The input x-values (particle sizes) over which to compute the PDF.

        Returns
        -------
        Tuple[np.ndarray, np.ndarray]
            The input x-values and the corresponding scaled PDF values.
        """
        pdf = lognorm.pdf(x, s=self.std_dev, scale=self.mean)
        return x, self.scale_factor * pdf


@dataclass
class UniformDistribution(Distribution):
    """
    Represents a uniform distribution for particle sizes.

    The uniform distribution assigns equal probability to all particle sizes within a specified range:

    .. math::
        f(x) = \frac{1}{b - a} \quad \text{for} \quad a \leq x \leq b

    where:
    - :math:`a` is the lower bound of the distribution.
    - :math:`b` is the upper bound of the distribution.

    Attributes
    ----------
    lower_bound : float
        The lower bound for particle sizes in meters.
    upper_bound : float
        The upper bound for particle sizes in meters.
    scale_factor : float, optional
        A scaling factor applied to the PDF (not the sizes).
    """

    lower_bound: float
    upper_bound: float
    scale_factor: float = 1.0

    def generate(self, n_samples: int) -> np.ndarray:
        """
        Generates a uniform distribution of scatterer sizes.

        The generated sizes are uniformly distributed between the specified `lower_bound` and `upper_bound`.

        Parameters
        ----------
        n_samples : int
            The number of particle sizes to generate.

        Returns
        -------
        np.ndarray
            An array of scatterer sizes in meters.
        """
        return np.random.uniform(self.lower_bound, self.upper_bound, n_samples.magnitude) * ureg.meter

    def get_pdf(self, x: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Returns the x-values and the scaled PDF values for the uniform distribution.

        The `scale_factor` is applied to the PDF, not the generated sizes.

        Parameters
        ----------
        x : np.ndarray
            The input x-values (particle sizes) over which to compute the PDF.

        Returns
        -------
        Tuple[np.ndarray, np.ndarray]
            The input x-values and the corresponding scaled PDF values.
        """
        pdf = uniform.pdf(x, loc=self.lower_bound, scale=self.upper_bound - self.lower_bound)
        return x, self.scale_factor * pdf


@dataclass
class SingularDistribution(Distribution):
    """
    Represents a singular (delta-like) distribution for particle sizes.

    In a singular distribution, all particle sizes are the same (delta function-like):

    .. math::
        f(x) = \delta(x - x_0)

    where:
    - :math:`x_0` is the singular particle size.

    Attributes
    ----------
    size_value : float
        The singular particle size in meters.
    scale_factor : float, optional
        A scaling factor applied to the PDF (not the sizes).
    """

    size_value: float
    scale_factor: float = 1.0

    def generate(self, n_samples: int) -> np.ndarray:
        """
        Generates a singular distribution of scatterer sizes.

        All sizes generated will be exactly the same as `size_value`.

        Parameters
        ----------
        n_samples : int
            The number of particle sizes to generate.

        Returns
        -------
        np.ndarray
            An array of identical scatterer sizes in meters.
        """
        return np.full(n_samples.magnitude, self.size_value) * ureg.meter

    def get_pdf(self, x: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Returns the x-values and the scaled PDF values for the singular distribution.

        The PDF is represented as a delta-like function centered at `size_value`.

        Parameters
        ----------
        x : np.ndarray
            The input x-values (particle sizes) over which to compute the PDF.

        Returns
        -------
        Tuple[np.ndarray, np.ndarray]
            The input x-values and the corresponding scaled PDF values.
        """
        pdf = np.zeros_like(x)
        idx = (np.abs(x - self.size_value)).argmin()  # Delta-like function for singular value
        pdf[idx] = 1.0
        return x, self.scale_factor * pdf
