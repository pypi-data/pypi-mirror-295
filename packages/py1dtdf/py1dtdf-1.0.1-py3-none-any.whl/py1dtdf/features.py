'''
Copyright (c) 2024 Rakshit Mittal

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
import numpy as np
from scipy.signal import find_peaks
import nolds
import math

# --- Helper function for sliding window ---
def apply_sliding_window(signal, window_size, overlap, func, **kwargs):
    step_size = window_size - overlap
    num_windows = (len(signal) - window_size) // step_size + 1
    result = []

    for i in range(num_windows):
        start_idx = i * step_size
        end_idx = start_idx + window_size
        window_signal = signal[start_idx:end_idx]
        result.append(func(window_signal, **kwargs))

    return np.array(result)


# --- Standard Time-Domain Features ---

# Mean: Measures the central tendency of the signal.
# Reference: https://en.wikipedia.org/wiki/Mean
def mean(signal, window_size, overlap):
    return apply_sliding_window(signal, window_size, overlap, np.mean)

# Standard Deviation: Measures the variability of the signal.
# Reference: https://en.wikipedia.org/wiki/Standard_deviation
def std_dev(signal, window_size, overlap):
    return apply_sliding_window(signal, window_size, overlap, np.std)

# RMS (Root Mean Square): Measures the magnitude of the signal.
# Reference: https://en.wikipedia.org/wiki/Root_mean_square
def rms(signal, window_size, overlap):
    return apply_sliding_window(signal, window_size, overlap, lambda x: np.sqrt(np.mean(x**2)))

# Skewness: Measures the asymmetry of the signal distribution.
# Reference: https://en.wikipedia.org/wiki/Skewness
def skewness(signal, window_size, overlap):
    return apply_sliding_window(signal, window_size, overlap, lambda x: np.mean(((x - np.mean(x)) / np.std(x))**3))

# Kurtosis: Measures the "tailedness" of the distribution.
# Reference: https://en.wikipedia.org/wiki/Kurtosis
def kurtosis(signal, window_size, overlap):
    return apply_sliding_window(signal, window_size, overlap, lambda x: np.mean(((x - np.mean(x)) / np.std(x))**4) - 3)

# Zero-Crossing Rate: Measures how often the signal crosses zero.
# Reference: https://en.wikipedia.org/wiki/Zero-crossing_rate
def zero_crossing_rate(signal, window_size, overlap):
    return apply_sliding_window(signal, window_size, overlap, lambda x: np.sum(np.diff(np.signbit(x))) / len(x))

# Maximum Value: Returns the maximum value in the window.
# Reference: https://en.wikipedia.org/wiki/Maxima_and_minima
def max_value(signal, window_size, overlap):
    return apply_sliding_window(signal, window_size, overlap, np.max)

# Minimum Value: Returns the minimum value in the window.
# Reference: https://en.wikipedia.org/wiki/Maxima_and_minima
def min_value(signal, window_size, overlap):
    return apply_sliding_window(signal, window_size, overlap, np.min)

# Peak-to-Peak: Measures the range between maximum and minimum values.
# Reference: https://en.wikipedia.org/wiki/Peak-to-peak
def peak_to_peak(signal, window_size, overlap):
    return apply_sliding_window(signal, window_size, overlap, lambda x: np.ptp(x))

# Variance: Measures the variability of the signal.
# Reference: https://en.wikipedia.org/wiki/Variance
def variance(signal, window_size, overlap):
    return apply_sliding_window(signal, window_size, overlap, np.var)

# IQR (Interquartile Range): Measures the range between the 25th and 75th percentiles.
# Reference: https://en.wikipedia.org/wiki/Interquartile_range
def iqr(signal, window_size, overlap):
    return apply_sliding_window(signal, window_size, overlap, lambda x: np.percentile(x, 75) - np.percentile(x, 25))

# Number of Peaks: Returns the number of peaks in the window.
# Reference: https://en.wikipedia.org/wiki/Peak_detection
def num_peaks(signal, window_size, overlap):
    return apply_sliding_window(signal, window_size, overlap, lambda x: len(find_peaks(x)[0]))

# Signal Line Length: Measures the cumulative sum of absolute differences.
# Reference: https://en.wikipedia.org/wiki/Signal_line
def signal_line_length(signal, window_size, overlap):
    return apply_sliding_window(signal, window_size, overlap, lambda x: np.sum(np.abs(np.diff(x))))

# Crest Factor: Ratio of the peak value to the RMS value.
# Reference: https://en.wikipedia.org/wiki/Crest_factor
def crest_factor(signal, window_size, overlap):
    return apply_sliding_window(signal, window_size, overlap, lambda x: np.max(np.abs(x)) / np.sqrt(np.mean(x**2)))

# Shape Factor: Ratio of RMS value to the mean absolute value.
# Reference: https://en.wikipedia.org/wiki/Shape_factor_(signal_processing)
def shape_factor(signal, window_size, overlap):
    return apply_sliding_window(signal, window_size, overlap, lambda x: np.sqrt(np.mean(x**2)) / np.mean(np.abs(x)))

# Impulse Factor: Ratio of the peak value to the mean absolute value.
# Reference: https://en.wikipedia.org/wiki/Impulse_factor
def impulse_factor(signal, window_size, overlap):
    return apply_sliding_window(signal, window_size, overlap, lambda x: np.max(np.abs(x)) / np.mean(np.abs(x)))

# Signal Range: Measures the difference between the maximum and minimum values.
# Reference: https://en.wikipedia.org/wiki/Range_(statistics)
def signal_range(signal, window_size, overlap):
    return apply_sliding_window(signal, window_size, overlap, lambda x: np.max(x) - np.min(x))

# Mean Crossing Rate: Measures how often the signal crosses its mean.
# Reference: https://en.wikipedia.org/wiki/Mean_crossing_rate
def mean_crossing_rate(signal, window_size, overlap):
    return apply_sliding_window(signal, window_size, overlap, lambda x: np.sum(np.diff(x > np.mean(x)) != 0) / len(x))

# Signal Variability: Standard deviation divided by the square root of the signal length.
# Reference: https://en.wikipedia.org/wiki/Standard_error
def signal_variability(signal, window_size, overlap):
    return apply_sliding_window(signal, window_size, overlap, lambda x: np.std(x) / np.sqrt(len(x)))

# Peak Amplitude: Returns the peak value of the signal.
# Reference: https://en.wikipedia.org/wiki/Peak_amplitude
def peak_amplitude(signal, window_size, overlap):
    return apply_sliding_window(signal, window_size, overlap, np.max)

# Energy: Sum of squared values in the signal.
# Reference: https://en.wikipedia.org/wiki/Energy_(signal_processing)
def energy(signal, window_size, overlap):
    return apply_sliding_window(signal, window_size, overlap, lambda x: np.sum(x**2))

# Median: Returns the median value of the signal.
# Reference: https://en.wikipedia.org/wiki/Median
def median(signal, window_size, overlap):
    return apply_sliding_window(signal, window_size, overlap, np.median)

# Root Sum of Squares (RSS): Square root of the sum of squared values.
# Reference: https://en.wikipedia.org/wiki/Root_sum_of_squares
def rss(signal, window_size, overlap):
    return apply_sliding_window(signal, window_size, overlap, lambda x: np.sqrt(np.sum(x**2)))

# DASDV (Difference Absolute Standard Deviation Value): Measures the variability of differences.
# Reference: https://ieeexplore.ieee.org/document/7516723
def dasdv(signal, window_size, overlap):
    return apply_sliding_window(signal, window_size, overlap, lambda x: np.sqrt(np.mean(np.diff(x)**2)))

# Range Ratio: Ratio of the range (max - min) to the standard deviation.
# Reference: https://en.wikipedia.org/wiki/Range_(statistics)
def range_ratio(signal, window_size, overlap):
    return apply_sliding_window(signal, window_size, overlap, lambda x: (np.max(x) - np.min(x)) / np.std(x))

# --- Fractal Features ---

# Higuchi Fractal Dimension: Measures the complexity of the signal using Higuchi's algorithm.
# Reference: https://www.sciencedirect.com/science/article/abs/pii/0167278988900814
def higuchi_fractal_dimension(signal, window_size, overlap, kmax=10):
    return apply_sliding_window(signal, window_size, overlap, lambda x: nolds.higuchi_fd(x, kmax=kmax))

# Hurst Exponent: Measures the long-term memory of the signal.
# Reference: https://en.wikipedia.org/wiki/Hurst_exponent
def hurst_exponent(signal, window_size, overlap):
    return apply_sliding_window(signal, window_size, overlap, nolds.hurst_rs)

# Lyapunov Exponent: Measures the sensitivity of the signal to initial conditions, indicating chaotic behavior.
# Reference: https://en.wikipedia.org/wiki/Lyapunov_exponent
def lyapunov_exponent(signal, window_size, overlap, emb_dim=6):
    return apply_sliding_window(signal, window_size, overlap, lambda x: nolds.lyap_r(x, emb_dim=emb_dim))

# Katz Fractal Dimension: Measures the complexity of the signal using Katz's method.
# Reference: https://ieeexplore.ieee.org/document/6170137
def katz_fractal_dimension(signal, window_size, overlap):
    return apply_sliding_window(signal, window_size, overlap, lambda x: math.log(np.sum(np.abs(np.diff(x)))) / (math.log(np.max(np.abs(x - x[0]))) + math.log(np.sum(np.abs(np.diff(x)))))

# Petrosian Fractal Dimension: Measures the complexity by detecting changes in signal direction.
# Reference: https://ieeexplore.ieee.org/document/517198
def petrosian_fractal_dimension(signal, window_size, overlap):
    return apply_sliding_window(signal, window_size, overlap, lambda x: np.log(len(x)) / (np.log(len(x)) + np.log(len(x) / (len(x) + 0.4 * np.sum(np.diff(np.sign(x)) != 0)))))

# Box-Counting Fractal Dimension: Uses the box-counting method to estimate the fractal dimension.
# Reference: https://en.wikipedia.org/wiki/Box-counting_fractal_dimension
def box_counting_fractal_dimension(signal, window_size, overlap):
    return apply_sliding_window(signal, window_size, overlap, lambda x: -np.polyfit(np.log(np.arange(1, len(x)//2)), np.log([np.sum(np.diff(x, n=s) > 0) for s in np.arange(1, len(x)//2)]), 1)[0])

# Correlation Dimension: Estimates the fractal dimension using the correlation integral.
# Reference: https://en.wikipedia.org/wiki/Correlation_dimension
def correlation_dimension(signal, window_size, overlap):
    return apply_sliding_window(signal, window_size, overlap, lambda x: nolds.corr_dim(x, 2))

# --- Complexity and Nonlinear Features ---

# Approximate Entropy: Measures the regularity and complexity of fluctuations in the signal.
# Reference: https://en.wikipedia.org/wiki/Approximate_entropy
def approximate_entropy(signal, window_size, overlap, m=2, r=0.2):
    def approx_entropy_func(x):
        N = len(x)
        def _phi(m):
            x_embedded = np.array([x[i:i + m] for i in range(N - m + 1)])
            C = np.sum(np.abs(x_embedded[:, None] - x_embedded[None, :]).max(axis=2) <= r, axis=0) / (N - m + 1)
            return np.sum(np.log(C)) / (N - m + 1)
        return abs(_phi(m) - _phi(m + 1))

    return apply_sliding_window(signal, window_size, overlap, approx_entropy_func)

# Sample Entropy: A robust version of Approximate Entropy.
# Reference: https://en.wikipedia.org/wiki/Sample_entropy
def sample_entropy(signal, window_size, overlap, m=2, r=0.2):
    return apply_sliding_window(signal, window_size, overlap, lambda x: nolds.sampen(x, m=m, r=r))

# Shannon Entropy: Measures the uncertainty or randomness in the signal.
# Reference: https://en.wikipedia.org/wiki/Entropy_(information_theory)
def shannon_entropy(signal, window_size, overlap, bins=50):
    return apply_sliding_window(signal, window_size, overlap, lambda x: -np.sum(np.histogram(x, bins=bins, density=True)[0] * np.log2(np.histogram(x, bins=bins, density=True)[0] + 1e-12)))

# Lempel-Ziv Complexity: Measures the complexity of the signal by counting the number of distinct patterns.
# Reference: https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv_complexity
def lempel_ziv_complexity(signal, window_size, overlap):
    return apply_sliding_window(signal, window_size, overlap, lambda x: nolds.sampen(x))

# Permutation Entropy: Captures the complexity of the signal by evaluating permutations of neighboring points.
# Reference: https://en.wikipedia.org/wiki/Permutation_entropy
def permutation_entropy(signal, window_size, overlap):
    return apply_sliding_window(signal, window_size, overlap, lambda x: nolds.perm_entropy(x))

# Largest Lyapunov Exponent: Quantifies the divergence of trajectories in chaotic systems.
# Reference: https://en.wikipedia.org/wiki/Lyapunov_exponent
def largest_lyapunov_exponent(signal, window_size, overlap, emb_dim=6):
    return apply_sliding_window(signal, window_size, overlap, lambda x: nolds.lyap_r(x, emb_dim=emb_dim))

# Mobility: Measures the rate of change in the variance of the signal.
# Reference: https://en.wikipedia.org/wiki/Mobility_(physics)
def mobility(signal, window_size, overlap):
    return apply_sliding_window(signal, window_size, overlap, lambda x: np.sqrt(np.var(np.diff(x)) / np.var(x)))

# --- Information-Theoretic Features ---

# Entropy: Shannon entropy of the signal.
# Reference: https://en.wikipedia.org/wiki/Entropy_(information_theory)
def entropy(signal, window_size, overlap, bins=50):
    return apply_sliding_window(signal, window_size, overlap, lambda x: -np.sum(np.histogram(x, bins=bins, density=True)[0] * np.log2(np.histogram(x, bins=bins, density=True)[0] + 1e-12)))

# Mutual Information: Measures the shared information between two signals.
# Reference: https://en.wikipedia.org/wiki/Mutual_information
def mutual_information(signal, window_size, overlap, bins=50):
    return apply_sliding_window(signal, window_size, overlap, lambda x: np.sum(np.histogram2d(x[:-1], x[1:], bins=bins)[0] * np.log2(np.histogram2d(x[:-1], x[1:], bins=bins)[0] / np.outer(np.histogram(x[:-1], bins=bins)[0], np.histogram(x[1:], bins=bins)[0] + 1e-12))))

# Symbolic Dynamics Entropy: Measures the randomness in symbolic transitions.
# Reference: https://en.wikipedia.org/wiki/Symbolic_dynamics
def symbolic_dynamics_entropy(signal, window_size, overlap):
    return apply_sliding_window(signal, window_size, overlap, lambda x: nolds.perm_entropy(x))

# Conditional Entropy: The entropy of the signal conditioned on its past values.
# Reference: https://en.wikipedia.org/wiki/Conditional_entropy
def conditional_entropy(signal, window_size, overlap, m=2):
    def conditional_entropy_func(x):
        N = len(x)
        x_embedded = np.array([x[i:i + m] for i in range(N - m + 1)])
        C = np.sum(np.abs(x_embedded[:, None] - x_embedded[None, :]).max(axis=2) <= 0.2 * np.std(x), axis=0) / (N - m + 1)
        return np.sum(np.log(C)) / (N - m + 1)
    return apply_sliding_window(signal, window_size, overlap, conditional_entropy_func)

# --- Statistical Moments and Distribution-Based Features ---

# Higher-Order Moments: Captures the higher-order statistical moments of the signal.
# Reference: https://en.wikipedia.org/wiki/Moment_(mathematics)
def higher_order_moments(signal, window_size, overlap, order=5):
    return apply_sliding_window(signal, window_size, overlap, lambda x: np.mean(((x - np.mean(x)) / np.std(x))**order))

# Percentiles: Returns a specific percentile of the signal.
# Reference: https://en.wikipedia.org/wiki/Percentile
def percentiles(signal, window_size, overlap, percentile_value=50):
    return apply_sliding_window(signal, window_size, overlap, lambda x: np.percentile(x, percentile_value))

# L-moments: Linear combinations of order statistics to capture distribution shape.
# Reference: https://en.wikipedia.org/wiki/L-moment
def l_moments(signal, window_size, overlap):
    return apply_sliding_window(signal, window_size, overlap, lambda x: (np.mean(x), np.var(x), np.mean(np.abs(x - np.median(x))), np.mean(np.abs(np.diff(x)))))

# Quantile Range: The difference between upper and lower percentiles.
# Reference: https://en.wikipedia.org/wiki/Quantile
def quantile_range(signal, window_size, overlap, lower_quantile=0.25, upper_quantile=0.75):
    return apply_sliding_window(signal, window_size, overlap, lambda x: np.percentile(x, upper_quantile * 100) - np.percentile(x, lower_quantile * 100))

# Autoregressive Coefficients: Coefficients from an autoregressive model fitted to the signal.
# Reference: https://en.wikipedia.org/wiki/Autoregressive_model
def autoregressive_coefficients(signal, window_size, overlap, order=4):
    from numpy.linalg import lstsq
    def ar_func(x):
        N = len(x)
        X = np.vstack([x[i:N - order + i] for i in range(order)]).T
        y = x[order:]
        ar_coeffs = lstsq(X, y, rcond=None)[0]
        return ar_coeffs

    return apply_sliding_window(signal, window_size, overlap, ar_func)

# --- Geometric and Recurrence-Based Features ---

# Recurrence Quantification: Measures the recurrence patterns in the signal.
# Reference: https://en.wikipedia.org/wiki/Recurrence_quantification_analysis
def recurrence_quantification(signal, window_size, overlap):
    return apply_sliding_window(signal, window_size, overlap, lambda x: nolds.corr_dim(x, 2))

# Attractor Reconstruction: Reconstructs the signal's attractor in phase space.
# Reference: https://en.wikipedia.org/wiki/Phase_space_reconstruction
def attractor_reconstruction(signal, window_size, overlap):
    from sklearn.manifold import Isomap
    return apply_sliding_window(signal, window_size, overlap, lambda x: Isomap(n_components=2).fit_transform(x.reshape(-1, 1)))

# Mean Crossing Rate: Measures how often the signal crosses its mean value.
# Reference: https://en.wikipedia.org/wiki/Mean_crossing_rate
def mean_crossing_rate(signal, window_size, overlap):
    return apply_sliding_window(signal, window_size, overlap, lambda x: np.sum(np.diff(x > np.mean(x)) != 0))

# Max Slope: Measures the steepest slope between consecutive points.
# Reference: https://en.wikipedia.org/wiki/Slope
def max_slope(signal, window_size, overlap):
    return apply_sliding_window(signal, window_size, overlap, lambda x: np.max(np.diff(x)))


# --- All Features Combined ---
def all_features(signal, window_size, overlap):
    return {
        'mean': mean(signal, window_size, overlap),
        'std_dev': std_dev(signal, window_size, overlap),
        'rms': rms(signal, window_size, overlap),
        'skewness': skewness(signal, window_size, overlap),
        'kurtosis': kurtosis(signal, window_size, overlap),
        'zero_crossing_rate': zero_crossing_rate(signal, window_size, overlap),
        'max_value': max_value(signal, window_size, overlap),
        'min_value': min_value(signal, window_size, overlap),
        'peak_to_peak': peak_to_peak(signal, window_size, overlap),
        'variance': variance(signal, window_size, overlap),
        'iqr': iqr(signal, window_size, overlap),
        'num_peaks': num_peaks(signal, window_size, overlap),
        'signal_line_length': signal_line_length(signal, window_size, overlap),
        'crest_factor': crest_factor(signal, window_size, overlap),
        'shape_factor': shape_factor(signal, window_size, overlap),
        'impulse_factor': impulse_factor(signal, window_size, overlap),
        'signal_range': signal_range(signal, window_size, overlap),
        'mean_crossing_rate': mean_crossing_rate(signal, window_size, overlap),
        'signal_variability': signal_variability(signal, window_size, overlap),
        'peak_amplitude': peak_amplitude(signal, window_size, overlap),
        'energy': energy(signal, window_size, overlap),
        'median': median(signal, window_size, overlap),
        'rss': rss(signal, window_size, overlap),
        'dasdv': dasdv(signal, window_size, overlap),
        'range_ratio': range_ratio(signal, window_size, overlap),
        'higuchi_fractal_dimension': higuchi_fractal_dimension(signal, window_size, overlap),
        'hurst_exponent': hurst_exponent(signal, window_size, overlap),
        'lyapunov_exponent': lyapunov_exponent(signal, window_size, overlap),
        'katz_fractal_dimension': katz_fractal_dimension(signal, window_size, overlap),
        'petrosian_fractal_dimension': petrosian_fractal_dimension(signal, window_size, overlap),
        'box_counting_fractal_dimension': box_counting_fractal_dimension(signal, window_size, overlap),
        'correlation_dimension': correlation_dimension(signal, window_size, overlap),
        'approximate_entropy': approximate_entropy(signal, window_size, overlap),
        'sample_entropy': sample_entropy(signal, window_size, overlap),
        'shannon_entropy': shannon_entropy(signal, window_size, overlap),
        'lempel_ziv_complexity': lempel_ziv_complexity(signal, window_size, overlap),
        'permutation_entropy': permutation_entropy(signal, window_size, overlap),
        'largest_lyapunov_exponent': largest_lyapunov_exponent(signal, window_size, overlap),
        'mobility': mobility(signal, window_size, overlap),
        'entropy': entropy(signal, window_size, overlap),
        'mutual_information': mutual_information(signal, window_size, overlap),
        'symbolic_dynamics_entropy': symbolic_dynamics_entropy(signal, window_size, overlap),
        'conditional_entropy': conditional_entropy(signal, window_size, overlap),
        'higher_order_moments': higher_order_moments(signal, window_size, overlap),
        'percentiles': percentiles(signal, window_size, overlap),
        'l_moments': l_moments(signal, window_size, overlap),
        'quantile_range': quantile_range(signal, window_size, overlap),
        'autoregressive_coefficients': autoregressive_coefficients(signal, window_size, overlap),
        'recurrence_quantification': recurrence_quantification(signal, window_size, overlap),
        'attractor_reconstruction': attractor_reconstruction(signal, window_size, overlap),
        'max_slope': max_slope(signal, window_size, overlap),
    }

