import pytest
import numpy as np
from FlowCyPy.distribution import NormalDistribution, LogNormalDistribution, UniformDistribution, SingularDistribution
from FlowCyPy import ureg

# Test parameters
N_SAMPLES = 1000
X_VALUES = np.linspace(1e-8, 1e-6, 1000)

def test_normal_distribution_generate():
    """Test the generate method of the NormalDistribution class."""
    normal_dist = NormalDistribution(mean=1e-6, std_dev=0.2e-6, scale_factor=1.0)
    sizes = normal_dist.generate(N_SAMPLES * ureg.particle)

    assert sizes.shape == (N_SAMPLES,), "Normal distribution: Generated size array has incorrect shape."
    assert np.all(sizes > 0), "Normal distribution: Generated sizes should all be positive."


def test_normal_distribution_pdf():
    """Test the get_pdf method of the NormalDistribution class."""
    normal_dist = NormalDistribution(mean=1e-6, std_dev=0.2e-6, scale_factor=2.0)
    x, pdf = normal_dist.get_pdf(X_VALUES)

    assert x.shape == pdf.shape, "Normal distribution: X values and PDF values must have the same shape."
    assert np.all(pdf >= 0), "Normal distribution: PDF values should be non-negative."
    assert np.isclose(np.sum(pdf), np.sum(normal_dist.get_pdf(X_VALUES)[1]), rtol=1e-4), "Normal distribution: PDF scaling seems incorrect."


def test_lognormal_distribution_generate():
    """Test the generate method of the LogNormalDistribution class."""
    lognormal_dist = LogNormalDistribution(mean=1e-6, std_dev=0.2e-6, scale_factor=1.0)
    sizes = lognormal_dist.generate(N_SAMPLES * ureg.particle)

    assert sizes.shape == (N_SAMPLES,), "Log-normal distribution: Generated size array has incorrect shape."
    assert np.all(sizes > 0), "Log-normal distribution: Generated sizes should all be positive."


def test_lognormal_distribution_pdf():
    """Test the get_pdf method of the LogNormalDistribution class."""
    lognormal_dist = LogNormalDistribution(mean=1e-6, std_dev=0.2e-6, scale_factor=1.5)
    x, pdf = lognormal_dist.get_pdf(X_VALUES)

    assert x.shape == pdf.shape, "Log-normal distribution: X values and PDF values must have the same shape."
    assert np.all(pdf >= 0), "Log-normal distribution: PDF values should be non-negative."
    assert np.isclose(np.sum(pdf), np.sum(lognormal_dist.get_pdf(X_VALUES)[1]), rtol=1e-4), "Log-normal distribution: PDF scaling seems incorrect."


# def test_uniform_distribution_generate():
    """Test the generate method of the UniformDistribution class."""
    uniform_dist = UniformDistribution(lower_bound=1e-7, upper_bound=1e-6, scale_factor=1.0)
    sizes = uniform_dist.generate(N_SAMPLES * ureg.particle)

    assert sizes.shape == (N_SAMPLES,), "Uniform distribution: Generated size array has incorrect shape."
    assert np.all(sizes.magnitude >= 1e-7), "Uniform distribution: Sizes should not be smaller than the lower bound."
    assert np.all(sizes.magnitude <= 1e-6), "Uniform distribution: Sizes should not exceed the upper bound."


def test_uniform_distribution_pdf():
    """Test the get_pdf method of the UniformDistribution class."""
    uniform_dist = UniformDistribution(lower_bound=1e-7, upper_bound=1e-6, scale_factor=1.0)
    x, pdf = uniform_dist.get_pdf(X_VALUES)

    assert x.shape == pdf.shape, "Uniform distribution: X values and PDF values must have the same shape."
    assert np.all(pdf >= 0), "Uniform distribution: PDF values should be non-negative."
    assert np.isclose(np.sum(pdf), np.sum(uniform_dist.get_pdf(X_VALUES)[1]), rtol=1e-4), "Uniform distribution: PDF scaling seems incorrect."


def test_singular_distribution_generate():
    """Test the generate method of the SingularDistribution class."""
    singular_dist = SingularDistribution(size_value=5e-7, scale_factor=1.0)
    sizes = singular_dist.generate(N_SAMPLES * ureg.particle)

    assert sizes.shape == (N_SAMPLES,), "Singular distribution: Generated size array has incorrect shape."
    assert np.all(sizes.magnitude == 5e-7), "Singular distribution: All sizes should be exactly equal to size_value."


def test_singular_distribution_pdf():
    """Test the get_pdf method of the SingularDistribution class."""
    singular_dist = SingularDistribution(size_value=5e-7, scale_factor=2.0)
    x, pdf = singular_dist.get_pdf(X_VALUES)

    assert x.shape == pdf.shape, "Singular distribution: X values and PDF values must have the same shape."
    assert np.any(pdf > 0), "Singular distribution: PDF should have a delta-like spike at the singular value."
    idx = (np.abs(X_VALUES - 5e-7)).argmin()
    assert pdf[idx] > 0, "Singular distribution: PDF should have a peak at the singular value (size_value)."
    assert np.isclose(np.sum(pdf), singular_dist.scale_factor, rtol=1e-4), "Singular distribution: PDF scaling seems incorrect."


if __name__ == "__main__":
    pytest.main([__file__])
