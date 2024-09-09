import pytest
from unittest.mock import patch
import matplotlib.pyplot as plt
import numpy as np
from FlowCyPy.scatterer_distribution import ScattererDistribution
from FlowCyPy.distribution import NormalDistribution, LogNormalDistribution, SingularDistribution, UniformDistribution
from FlowCyPy.flow import Flow

# Fixtures to set up a default Flow and Distributions
@pytest.fixture
def default_flow():
    """Fixture for creating a default Flow object."""
    return Flow(
        flow_speed=80e-6,
        flow_area=1e-6,
        total_time=1.0,
        scatterer_density=1e15
    )

@pytest.fixture
def normal_distribution():
    """Fixture for creating a NormalDistribution."""
    return NormalDistribution(
        mean=1e-6,
        std_dev=1e-7,
        scale_factor=1.0
    )

@pytest.fixture
def lognormal_distribution():
    """Fixture for creating a LogNormalDistribution."""
    return LogNormalDistribution(
        mean=1e-6,
        std_dev=1e-7,
        scale_factor=1.0
    )

@pytest.fixture
def uniform_distribution():
    """Fixture for creating a UniformDistribution."""
    return UniformDistribution(
        lower_bound=5e-7,
        upper_bound=1.5e-6,
        scale_factor=1.0
    )

@pytest.fixture
def singular_distribution():
    """Fixture for creating a SingularDistribution."""
    return SingularDistribution(
        size_value=1e-6,
        scale_factor=1.0
    )

@patch('matplotlib.pyplot.show')
@pytest.mark.parametrize(
    "distribution_fixture",
    ["normal_distribution", "lognormal_distribution", "uniform_distribution", "singular_distribution"]
)
def test_generate_distribution_size(mock_show, request, distribution_fixture, default_flow):
    """Test if the ScattererDistribution generates sizes correctly for each distribution type."""

    # Get the distribution from the fixtures
    distribution = request.getfixturevalue(distribution_fixture)

    # Create the ScattererDistribution object with the chosen distribution
    scatterer_distribution = ScattererDistribution(
        flow=default_flow,
        refractive_index=1.5,
        distributions=[distribution],
    )

    # Check that sizes were generated and are positive
    assert scatterer_distribution.sizes.size > 0, "Generated size array is empty."
    assert np.all(scatterer_distribution.sizes.magnitude > 0), "Some generated sizes are not positive."

    # Check if the sizes follow the expected bounds depending on the distribution type
    if isinstance(distribution, NormalDistribution):
        expected_mean = distribution.mean
        generated_mean = np.mean(scatterer_distribution.sizes.magnitude)
        assert np.isclose(generated_mean, expected_mean, atol=1e-7), (
            f"Normal distribution: Expected mean {expected_mean}, but got {generated_mean}"
        )

    elif isinstance(distribution, LogNormalDistribution):
        assert np.all(scatterer_distribution.sizes.magnitude > 0), "Lognormal distribution generated non-positive sizes."

    elif isinstance(distribution, UniformDistribution):
        lower_bound = distribution.lower_bound
        upper_bound = distribution.upper_bound
        assert np.all((scatterer_distribution.sizes.magnitude >= lower_bound) & (scatterer_distribution.sizes.magnitude <= upper_bound)), (
            f"Uniform distribution: Sizes are out of bounds [{lower_bound}, {upper_bound}]"
        )

    elif isinstance(distribution, SingularDistribution):
        singular_value = distribution.size_value
        assert np.all(scatterer_distribution.sizes.magnitude == singular_value), (
            f"Singular distribution: All sizes should be {singular_value}, but got varying sizes."
        )

    # Test plotting (matplotlib's plot will be called but won't be displayed due to the mock)
    scatterer_distribution.plot(bins=45)

    plt.close()



def test_generate_longitudinal_positions(default_flow, uniform_distribution):
    """Test the generation of longitudinal positions based on Poisson process."""
    n_samples = 1000

    distribution = ScattererDistribution(
        refractive_index=1.5,
        flow=default_flow,
        distributions=[uniform_distribution],
    )

    # Assert correct shape of generated longitudinal positions
    assert distribution.flow.longitudinal_positions.size > 0, "Generated longitudinal positions array has incorrect shape."

    # Assert that longitudinal positions are increasing (since they are cumulative)
    assert np.all(np.diff(distribution.flow.longitudinal_positions.magnitude) >= 0), "Longitudinal positions are not monotonically increasing."

    # Assert that no positions are negative
    assert np.all(distribution.flow.longitudinal_positions.magnitude >= 0), "Some longitudinal positions are negative."


def test_plot_positions(default_flow, uniform_distribution):
    """Test the plotting of longitudinal positions."""
    n_samples = 1000

    distribution = ScattererDistribution(
        refractive_index=1.5,
        flow=default_flow,
        distributions=[uniform_distribution],
    )

    # Plotting the positions (mocked plt.show)
    with patch('matplotlib.pyplot.show'):
        distribution.plot(bins=45)

    plt.close()


if __name__ == '__main__':
    pytest.main([__file__])
