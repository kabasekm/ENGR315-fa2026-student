
"""
CULMINATING ASSIGNMENT 2: RSI

Create a program which will provide answers to the tasks posed in the assignment description.

For this assignment, you will start from scratch with this blank template.
It is your reponsibility to include all necessary program components in this file.
Your code needs to be successful as well as sufficiently commented/documented to receive full credit.

The relevant data file is named "all_participant_data_rsi.csv" and is located in data > drop-jump.

All file paths need to be relative and execute from this file's directory;
the Visual Studio Code setting "Python > Terminal: Execute in File Dir" 
must be enabled in File > Preferences > Settings.

See Canvas for additional requirements.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_rel, norm, chisquare, t, sem


DATA_PATH = '../../data/drop-jump/all_participant_data_rsi.csv'
ALPHA = 0.05


def paired_rsi_test(data):
    """
    Task 1: Compare force plate and accelerometer RSI values.
    Each trial has two measurements, so a paired t-test is used.
    """

    # Get the two RSI columns from the dataframe
    force = data['force_plate_rsi'].to_numpy()
    accel = data['accelerometer_rsi'].to_numpy()

    # Both RSI measurements come from the same trial, so a paired t-test is used.
    # Check if the average difference between the two methods is zero.
    statistic, p_value = ttest_rel(force, accel)

    print('TASK 1: PAIRED T-TEST')
    print('H0: Mean(force plate RSI - accelerometer RSI) = 0')
    print('H1: Mean(force plate RSI - accelerometer RSI) != 0')

    print(f'Number of paired trials: {len(data)}')
    print(f'Mean force plate RSI: {np.mean(force):.4f}')
    print(f'Mean accelerometer RSI: {np.mean(accel):.4f}')
    print(f't-statistic: {statistic:.4f}')
    print(f'p-value: {p_value:.6g}')

    # Compare the p-value with alpha = 0.05
    if p_value < ALPHA:
        print('Decision: Reject H0.')
        print('There is a significant difference between the two methods.')
    else:
        print('Decision: Fail to reject H0.')
        print('There is not enough evidence of a difference between the methods.')

    print()


def accelerometer_fit_test(data):
    """
    Task 2: Fit a normal distribution to accelerometer RSI data
    and check the fit using a chi-square test.
    """

    # Select the accelerometer data
    accel = data['accelerometer_rsi'].to_numpy()

    # Find the mean and standard deviation of the fitted normal curve
    fitted_mean, fitted_std = norm.fit(accel)

    # Create bins around the mean and include both ends of the distribution
    bin_edges = np.r_[
        -np.inf,
        np.linspace(
            fitted_mean - 1.5 * fitted_std,
            fitted_mean + 1.5 * fitted_std,
            7
        ),
        np.inf
    ]

    # Count how many data points fall into each bin
    observed, _ = np.histogram(accel, bins=bin_edges)

    # Subtract the CDF values at each bin edge to find the probability for that bin.
    # Multiply each probability by the total samples to get the expected counts.
    probabilities = np.diff(
        norm.cdf(bin_edges, loc=fitted_mean, scale=fitted_std)
    )
    expected = probabilities * len(accel)

    # Use ddof=2 since the mean and standard deviation were fitted
    chi_stat, p_value = chisquare(
        f_obs=observed,
        f_exp=expected,
        ddof=2
    )

    print('TASK 2: NORMAL FIT AND CHI-SQUARE GOODNESS OF FIT')
    print('H0: Accelerometer RSI follows the fitted normal distribution.')
    print('H1: Accelerometer RSI does not follow the fitted normal distribution.')

    print(f'Fitted mean: {fitted_mean:.4f}')
    print(f'Fitted standard deviation: {fitted_std:.4f}')
    print(f'Chi-square statistic: {chi_stat:.4f}')
    print(f'p-value: {p_value:.6g}')
    print(f'Smallest expected bin count: {expected.min():.2f}')

    # Decide whether the normal distribution is a reasonable fit
    if p_value < ALPHA:
        print('Decision: Reject H0.')
        print('The data does not fit the normal distribution well.')
    else:
        print('Decision: Fail to reject H0.')
        print('The data is consistent with the fitted normal distribution.')

    print()

    # Plot the accelerometer data and fitted normal curve
    plt.figure(figsize=(9, 5))

    plt.hist(
        accel,
        bins=10,
        density=True,
        alpha=0.65,
        edgecolor='black',
        label='Accelerometer RSI data'
    )

    # Calculate points for the fitted normal curve
    x = np.linspace(accel.min() - 0.1, accel.max() + 0.1, 500)

    plt.plot(
        x,
        norm.pdf(x, loc=fitted_mean, scale=fitted_std),
        linewidth=2,
        label='Fitted normal distribution'
    )

    plt.title('Accelerometer RSI: Histogram and Fitted Normal Distribution')
    plt.xlabel('Reactive Strength Index (RSI)')
    plt.ylabel('Probability density')
    plt.legend()
    plt.tight_layout()
    plt.show()


def participant_f_intervals(data):
    """
    Task 3: Select Participant F's trials and calculate
    95% confidence intervals for both RSI measurements.
    """

    # Trial names start with the participant letter
    participant_f = data[
        data['trial'].str.split('_').str[0] == 'F'
    ]

    print('TASK 3: PARTICIPANT F')
    print('Participant F trials:')
    print(participant_f.to_string(index=False))
    print()

    # Calculate the confidence interval for each measurement method
    for column, label in [
        ('force_plate_rsi', 'Force plate'),
        ('accelerometer_rsi', 'Accelerometer')
    ]:

        values = participant_f[column].to_numpy()
        mean = np.mean(values)

        # Calculate the 95% confidence interval using the mean and standard error.
        # Use the t-distribution since the population standard deviation is unknown.
        lower, upper = t.interval(
            0.95,
            df=len(values) - 1,
            loc=mean,
            scale=sem(values)
        )

        print(
            f'{label}: n={len(values)}, mean={mean:.4f}, '
            f'95% confidence interval=({lower:.4f}, {upper:.4f})'
        )


def main():
    """
    Load the RSI data and run the three analysis tasks.
    """

    # Read the CSV file from the course data folder
    data = pd.read_csv(DATA_PATH)

    paired_rsi_test(data)
    accelerometer_fit_test(data)
    participant_f_intervals(data)


if __name__ == '__main__':
    main()
