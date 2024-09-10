# Py1DTDF

This Python package provides a comprehensive set of standard, fractal, nonlinear, and information-theoretic time-domain features for 1-D signals. The features are computed using an adjustable sliding window and overlap mechanism, allowing flexibility in analyzing different segments of a signal.Hence the name 1DTDF : 1-Dimensional Time-Domain Features.

## Features

### 1. Standard Time-Domain Features
These features capture the statistical and structural properties of the signal over time.

- **Mean**: Measures the central tendency of the signal ([Wikipedia](https://en.wikipedia.org/wiki/Mean)).
- **Standard Deviation**: Measures the variability of the signal ([Wikipedia](https://en.wikipedia.org/wiki/Standard_deviation)).
- **RMS (Root Mean Square)**: Measures the magnitude of the signal ([Wikipedia](https://en.wikipedia.org/wiki/Root_mean_square)).
- **Skewness**: Measures the asymmetry of the signal distribution ([Wikipedia](https://en.wikipedia.org/wiki/Skewness)).
- **Kurtosis**: Measures the "tailedness" of the signal distribution ([Wikipedia](https://en.wikipedia.org/wiki/Kurtosis)).
- **Zero-Crossing Rate**: Measures how often the signal crosses zero ([Wikipedia](https://en.wikipedia.org/wiki/Zero-crossing_rate)).
- **Maximum Value**: Returns the maximum value in the window ([Wikipedia](https://en.wikipedia.org/wiki/Maxima_and_minima)).
- **Minimum Value**: Returns the minimum value in the window ([Wikipedia](https://en.wikipedia.org/wiki/Maxima_and_minima)).
- **Peak-to-Peak**: Measures the range between maximum and minimum values ([Wikipedia](https://en.wikipedia.org/wiki/Peak-to-peak)).
- **Variance**: Measures the variability of the signal ([Wikipedia](https://en.wikipedia.org/wiki/Variance)).
- **IQR (Interquartile Range)**: Measures the spread of the middle 50% of the data ([Wikipedia](https://en.wikipedia.org/wiki/Interquartile_range)).
- **Number of Peaks**: Returns the number of peaks in the window ([Wikipedia](https://en.wikipedia.org/wiki/Peak_detection)).
- **Signal Line Length**: Measures the cumulative sum of absolute differences in the signal ([Wikipedia](https://en.wikipedia.org/wiki/Signal_line)).
- **Crest Factor**: Ratio of the peak value to the RMS value ([Wikipedia](https://en.wikipedia.org/wiki/Crest_factor)).
- **Shape Factor**: Ratio of the RMS value to the mean absolute value ([Wikipedia](https://en.wikipedia.org/wiki/Shape_factor_(signal_processing))).
- **Impulse Factor**: Ratio of the peak value to the mean absolute value ([Wikipedia](https://en.wikipedia.org/wiki/Impulse_factor)).
- **Signal Range**: Difference between the maximum and minimum values ([Wikipedia](https://en.wikipedia.org/wiki/Range_(statistics))).
- **Mean Crossing Rate**: Measures how often the signal crosses its mean value ([Wikipedia](https://en.wikipedia.org/wiki/Mean_crossing_rate)).
- **Signal Variability**: Standard deviation divided by the square root of the signal length ([Wikipedia](https://en.wikipedia.org/wiki/Standard_error)).
- **Peak Amplitude**: Returns the peak value of the signal ([Wikipedia](https://en.wikipedia.org/wiki/Peak_amplitude)).
- **Energy**: Sum of squared values in the signal ([Wikipedia](https://en.wikipedia.org/wiki/Energy_(signal_processing))).
- **Median**: Returns the median value of the signal ([Wikipedia](https://en.wikipedia.org/wiki/Median)).
- **Root Sum of Squares (RSS)**: Square root of the sum of squared values ([Wikipedia](https://en.wikipedia.org/wiki/Root_sum_of_squares)).
- **DASDV**: Measures the variability of differences between consecutive points ([IEEE](https://ieeexplore.ieee.org/document/7516723)).
- **Range Ratio**: Ratio of the range (max - min) to the standard deviation ([Wikipedia](https://en.wikipedia.org/wiki/Range_(statistics))).

### 2. Fractal Features
These features describe the complexity and self-similarity of the signal.

- **Higuchi Fractal Dimension**: Measures complexity using Higuchi's algorithm ([Scientific Article](https://www.sciencedirect.com/science/article/abs/pii/0167278988900814)).
- **Hurst Exponent**: Measures the long-term memory of the signal ([Wikipedia](https://en.wikipedia.org/wiki/Hurst_exponent)).
- **Lyapunov Exponent**: Indicates chaos in the signal by measuring sensitivity to initial conditions ([Wikipedia](https://en.wikipedia.org/wiki/Lyapunov_exponent)).
- **Katz Fractal Dimension**: Measures signal complexity using Katz's method ([IEEE](https://ieeexplore.ieee.org/document/6170137)).
- **Petrosian Fractal Dimension**: Measures complexity by detecting changes in signal direction ([IEEE](https://ieeexplore.ieee.org/document/517198)).
- **Box-Counting Fractal Dimension**: Uses the box-counting method to estimate fractal dimension ([Wikipedia](https://en.wikipedia.org/wiki/Box-counting_fractal_dimension)).
- **Correlation Dimension**: Estimates the fractal dimension using the correlation integral ([Wikipedia](https://en.wikipedia.org/wiki/Correlation_dimension)).

### 3. Complexity and Nonlinear Features
These features capture the irregularity, randomness, or chaotic nature of the signal.

- **Approximate Entropy**: Measures the complexity and unpredictability of the signal ([Wikipedia](https://en.wikipedia.org/wiki/Approximate_entropy)).
- **Sample Entropy**: A more robust version of Approximate Entropy ([Wikipedia](https://en.wikipedia.org/wiki/Sample_entropy)).
- **Shannon Entropy**: Measures the uncertainty or randomness of the signal ([Wikipedia](https://en.wikipedia.org/wiki/Entropy_(information_theory))).
- **Lempel-Ziv Complexity**: Measures the number of distinct patterns in the signal ([Wikipedia](https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv_complexity)).
- **Permutation Entropy**: Evaluates the complexity by analyzing the order of neighboring values ([Wikipedia](https://en.wikipedia.org/wiki/Permutation_entropy)).
- **Largest Lyapunov Exponent**: Quantifies the divergence of nearby trajectories, indicating chaos ([Wikipedia](https://en.wikipedia.org/wiki/Lyapunov_exponent)).
- **Mobility**: Measures the rate of change in the variance of the signal ([Wikipedia](https://en.wikipedia.org/wiki/Mobility_(physics))).

### 4. Information-Theoretic Features
These features quantify the information content and uncertainty in the signal.

- **Entropy**: Shannon entropy of the signal ([Wikipedia](https://en.wikipedia.org/wiki/Entropy_(information_theory))).
- **Mutual Information**: Measures the shared information between two parts of the signal ([Wikipedia](https://en.wikipedia.org/wiki/Mutual_information)).
- **Symbolic Dynamics Entropy**: Measures randomness in symbolic transitions ([Wikipedia](https://en.wikipedia.org/wiki/Symbolic_dynamics)).
- **Conditional Entropy**: The entropy of the signal conditioned on its past values ([Wikipedia](https://en.wikipedia.org/wiki/Conditional_entropy)).

### 5. Statistical Moments and Distribution-Based Features
These features capture statistical properties of the signal distribution.

- **Higher-Order Moments**: Measures higher-order statistical moments (up to 6th order) ([Wikipedia](https://en.wikipedia.org/wiki/Moment_(mathematics))).
- **Percentiles**: Returns a specific percentile of the signal ([Wikipedia](https://en.wikipedia.org/wiki/Percentile)).
- **L-Moments**: Linear combinations of order statistics to describe the shape of the distribution ([Wikipedia](https://en.wikipedia.org/wiki/L-moment)).
- **Quantile Range**: Measures the spread between upper and lower percentiles ([Wikipedia](https://en.wikipedia.org/wiki/Quantile)).
- **Autoregressive Coefficients**: Coefficients from an autoregressive model fitted to the signal ([Wikipedia](https://en.wikipedia.org/wiki/Autoregressive_model)).

### 6. Geometric and Recurrence-Based Features
These features analyze the geometric structure of the signal trajectory and its recurrence.

- **Recurrence Quantification**: Measures the recurrence patterns of the signal ([Wikipedia](https://en.wikipedia.org/wiki/Recurrence_quantification_analysis)).
- **Attractor Reconstruction**: Reconstructs the attractor of the signal in phase space ([Wikipedia](https://en.wikipedia.org/wiki/Phase_space_reconstruction)).
- **Mean Crossing Rate**: Measures how often the signal crosses its mean value ([Wikipedia](https://en.wikipedia.org/wiki/Mean_crossing_rate)).
- **Max Slope**: Measures the steepest slope between consecutive points ([Wikipedia](https://en.wikipedia.org/wiki/Slope)).

## Installation

To install the package, run:

```bash
pip install py1dtdf

## Usage

The software is licensed under the MIT License.
Please see LICENSE file for more details.

```python
import numpy as np
from py1dtdf import all_features

# Example signal
signal = np.sin(np.linspace(0, 10, 1000))  # Sine wave signal

# Set window size and overlap
window_size = 200
overlap = 100

# Compute all features for the signal
features = all_features(signal, window_size, overlap)

# Print all features
for feature_name, feature_values in features.items():
    print(f"{feature_name}: {feature_values}")
