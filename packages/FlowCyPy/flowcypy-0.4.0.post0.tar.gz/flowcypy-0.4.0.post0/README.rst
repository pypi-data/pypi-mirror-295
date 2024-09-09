FlowCyPy Simulation Tool
========================

|logo|

|python| |coverage| |PyPi| |PyPi_download| |docs|

Overview
--------

**FlowCyPy** is a Python-based simulation package for replicating the behavior of a flow cytometer. It simulates realistic Forward Scatter (FSC) and Side Scatter (SSC) signals, incorporating effects like noise, baseline shifts, signal saturation, and digitization, enabling detailed analysis and visualization of flow cytometry experiments. The tool is ideal for those looking to model particle events, scattering behavior, and detector responses in flow cytometry setups.

Features
--------

- **Simulate Particle Events**: Create realistic FSC and SSC signals using custom particle event parameters.
- **Noise and Baseline Shift Modeling**: Simulate Gaussian noise and baseline shifts to replicate real-world signal variations.
- **Signal Saturation**: Model detector saturation to reflect real-life limits.
- **Signal Discretization**: Quantize continuous signals into a specified number of bins for enhanced analysis.
- **Custom Plotting**: Visualize signals with customizable plotting options, including multi-channel plots.
- **Fully Configurable**: Offers flexibility with particle size distributions, flow parameters, and detector setup.

Installation
------------

To install **FlowCyPy**, use the following commands to clone the repository and install the package:

.. code-block:: bash

    git clone https://github.com/MartinPdeS/FlowCyPy.git
    cd FlowCyPy
    pip install .[testing]

Requirements
------------

FlowCyPy requires Python 3.10 or higher and the following dependencies:

- `numpy`
- `scipy`
- `pint`
- `tabulate`
- `seaborn`
- `MPSPlots`
- `PyMieSim`
- `pydantic>=2.6.3`

You can also install the optional dependencies for testing and documentation:

.. code-block:: bash

    pip install .[testing]        # Install testing dependencies
    pip install .[documentation]  # Install documentation dependencies

Usage Example
-------------

Below is a basic example to get started with **FlowCyPy**:

.. code-block:: python

    from FlowCyPy import FlowCytometer, ScattererDistribution, Flow, Detector, Source

    # Initialize the flow parameters
    flow = Flow(
        flow_speed=80e-6,       # 80 micrometers per second
        flow_area=1e-6,         # 1 square micrometer
        total_time=8.0,         # 8 seconds of flow simulation
        scatterer_density=1e11  # 1e11 particles per cubic meter
    )

    # Create a scatterer distribution
    scatterer_distribution = ScattererDistribution(
        flow=flow,
        refractive_index=1.5,
        distributions=[
            NormalDistribution(mean=10e-6, std_dev=1e-7),  # Normal particle size distribution
        ]
    )

    # Define a laser source
    source = Source(
        numerical_aperture=0.3,
        wavelength=1550e-9,   # Wavelength of 1550 nm
        optical_power=200e-3  # 200 mW optical power
    )

    # Add detectors to the flow cytometer
    detector_0 = Detector(theta_angle=90, numerical_aperture=0.4, acquisition_frequency=1e4)
    detector_1 = Detector(theta_angle=0, numerical_aperture=0.4, acquisition_frequency=1e4)

    # Create the flow cytometer
    cytometer = FlowCytometer(
        coupling_mechanism='mie',
        source=source,
        scatterer_distribution=scatterer_distribution,
        detectors=[detector_0, detector_1]
    )

    # Simulate the pulses
    cytometer.simulate_pulse()

    # Print properties of the simulation
    cytometer.print_properties()

    # Plot the simulated signals
    cytometer.plot()

This will produce a signal plot similar to the following:

|example_fcm|

Additional Examples
-------------------

Detailed examples and workflows are available in the `Examples <https://FlowCytometry.readthedocs.io/en/master/gallery/index.html>`_ section of the documentation, which includes:

- **Density Plots for Large and Small Scatterers**:
  |example_density_plot| |example_density_plot_small|

- **Two-Population Scatter Density Plot**:
  |example_density_plot_2pop|

Testing and Coverage
--------------------

To run tests, ensure you have installed the testing dependencies as described in the `pyproject.toml`. You can run tests with `pytest`:

.. code-block:: bash

    pytest --cov=FlowCyPy --cov-report=html

This generates a coverage report in `htmlcov/index.html`, providing detailed test coverage for the package.

Documentation
-------------

You can build the documentation locally using `Sphinx`:

.. code-block:: bash

    pip install .[documentation]
    cd docs
    make html

The HTML documentation will be available in the `docs/_build/html` directory.

Contact Information
-------------------

FlowCyPy is under active development, and contributions are always welcome! Please reach out if you'd like to collaborate or offer suggestions.

FlowCyPy was created by `Martin Poinsinet de Sivry-Houle <https://github.com/MartinPdS>`_.

- Email: `martin.poinsinet.de.sivry@gmail.com <mailto:martin.poinsinet.de.sivry@gmail.com?subject=FlowCyPy>`_

.. |python| image:: https://img.shields.io/pypi/pyversions/flowcypy.svg
   :target: https://www.python.org/

.. |logo| image:: https://github.com/MartinPdeS/FlowCyPy/raw/master/docs/images/logo.png

.. |example_fcm| image:: https://github.com/MartinPdeS/FlowCyPy/blob/master/docs/images/example_signal_FCM.png

.. |example_density_plot| image:: https://github.com/MartinPdeS/FlowCyPy/blob/master/docs/images/example_density_plot.png
   :width: 45%

.. |example_density_plot_small| image:: https://github.com/MartinPdeS/FlowCyPy/blob/master/docs/images/example_density_plot_small.png
   :width: 45%

.. |example_density_plot_2pop| image:: https://github.com/MartinPdeS/FlowCyPy/blob/master/docs/images/example_density_plot_2pop.png
   :width: 100%

.. |coverage| image:: https://raw.githubusercontent.com/MartinPdeS/FlowCyPy/python-coverage-comment-action-data/badge.svg
   :alt: Unittest coverage
   :target: https://htmlpreview.github.io/?https://github.com/MartinPdeS/FlowCyPy/blob/python-coverage-comment-action-data/htmlcov/index.html

.. |PyPi| image:: https://badge.fury.io/py/FlowCyPy.svg
   :target: https://badge.fury.io/py/FlowCyPy

.. |PyPi_download| image:: https://img.shields.io/pypi/dm/FlowCyPy.svg
   :target: https://pypistats.org/packages/flowcypy

.. |docs| image:: https://readthedocs.org/projects/flowcytometry/badge/?version=latest
   :target: https://flowcytometry.readthedocs.io/en/latest/
