import csv

import numpy as np
from scipy.integrate import quad
from scipy.optimize import curve_fit
from scipy.signal import savgol_filter, find_peaks
from scipy.special import erf


def asym_peak(t, pars):
    'from Anal. Chem. 1994, 66, 1294-1301'
    a0 = pars[0]  # peak area
    a1 = pars[1]  # elution time
    a2 = pars[2]  # width of gaussian
    a3 = pars[3]  # exponential damping term
    f = (a0 / 2 / a3 * np.exp(a2 ** 2 / 2.0 / a3 ** 2 + (a1 - t) / a3)
         * (erf((t - a1) / (np.sqrt(2.0) * a2) - a2 / np.sqrt(2.0) / a3) + abs(a3) / a3))
    return f


def fit_peaks(x, *param):
    """fit multiple peaks """
    num_peak = int(len(param) / 4)
    for i in range(num_peak):
        peak_param = param[i * 4:(i + 1) * 4]
        peak = asym_peak(x, peak_param)
        if i == 0:
            peak_sum = peak
        else:
            peak_sum += peak
    return peak_sum


def find_baseline(absorbance, smooth_window):
    """
    find baselines according to first derivative of absorbance
    """
    linear_baseline = savgol_filter(absorbance, polyorder=2, window_length=smooth_window)
    dv = np.gradient(linear_baseline)
    dv = savgol_filter(dv, polyorder=2, window_length=smooth_window)
    linear_baseline = np.copy(absorbance)
    # print(linear_baseline)
    zeros = [i for i in range(len(dv) - 1) if dv[i] < 0 and dv[i] * dv[i + 1] < 0]
    down, _ = find_peaks(-absorbance, prominence=(1, None), width=(10, None))
    zeros = [i for i in zeros if not any(abs(down - i) < 50)]
    for start, end in zip(([0] + zeros), (zeros + [len(linear_baseline) - 1])):
        linear_baseline[start:end] = np.linspace(absorbance[start], absorbance[end], end - start)

    return linear_baseline, zeros


def find_para(x, y, peaks, tailing_fronting='tailing', peak_width=0.05):
    """find peak fit parameters and boundaries"""
    damping = 1 if tailing_fronting == 'tailing' else -1
    peak_params = []
    lower_bounds = []
    upper_bounds = []

    def area_under_gaussian(peak_height):
        """use gaussian to estimate peak area"""
        gaussian = lambda x: peak_height * np.exp(-x ** 2 / (2 * 0.1 ** 2))
        area, _ = quad(gaussian, -np.inf, np.inf)
        return max(0, area)

    for peak in peaks:
        retention = x[peak]
        peak_area = area_under_gaussian(y[peak])
        params = [peak_area, retention, peak_width, peak_width * damping]
        peak_params.extend(params)
        lower_bound = [0,       retention - 0.03,   0,              -peak_width*1.5 if damping == -1 else peak_width*0.5]
        upper_bound = [np.inf,  retention + 0.01,   peak_width*3,   -peak_width*0.5 if damping == -1 else peak_width*2.5]
        lower_bounds.extend(lower_bound)
        upper_bounds.extend(upper_bound)
        # t = len(x[np.where(x < 0.25)])
    return peak_params, (lower_bounds, upper_bounds)


def group_items(retention_time_list, peak_shift):
    """group peaks between data if they are within a certain retention time"""
    grouped_list = []
    if not retention_time_list:
        return grouped_list
    current_group = [retention_time_list[0]]
    for i in range(1, len(retention_time_list)):
        if (retention_time_list[i] - retention_time_list[i - 1]) < peak_shift:
            current_group.append(retention_time_list[i])
        else:
            grouped_list.append([current_group[0], current_group[-1]])
            current_group = [retention_time_list[i]]
    grouped_list.append([current_group[0], current_group[-1]])
    return grouped_list


def format_save_csv(result, retention_time, peak_shift):
    """save time course data to csv"""
    retention_time = sorted(retention_time)
    retention_time = group_items(retention_time, peak_shift)
    new_list = []
    for data_name in result:
        old_retention_time = result[data_name]
        new_dict = {}
        new_dict['time'] = data_name
        for retention_time_range in retention_time:
            new_dict[str(retention_time_range)] = 0
            for i in old_retention_time:
                if retention_time_range[0] <= i <= retention_time_range[1]:
                    new_dict[str(retention_time_range)] = old_retention_time[i]
        new_list.append(new_dict)
    with open('results.csv', 'w', newline='') as file:
        dict_writer = csv.DictWriter(file, new_list[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(new_list)


def second_derivative(y, smooth_window: int = 25, smooth_derivative: bool = True):
    """find second derivative with option to smooth both derivatives"""
    dy = np.gradient(y)
    if smooth_derivative:
        dy = savgol_filter(dy * 100, window_length=2 * smooth_window + 1, polyorder=2)
    dy2 = np.gradient(dy)
    if smooth_derivative:
        dy2 = savgol_filter(dy2 * 100, window_length=2 * smooth_window + 1, polyorder=2)
    return -dy2


def find_peak_group(y, smooth_window):
    """group peaks if they are overlapped, by detecting range without auto-detected baselines"""
    # smoothed_y = savgol_filter(y, window_length=smooth_window, polyorder=2)
    baseline, zeros = find_baseline(y, smooth_window)
    peaks, properties = find_peaks(y, prominence=(1, None))
    ranges = []
    for i in peaks:
        left = zeros[np.where(np.array(zeros) < i)[0][-1]] if len(np.where(np.array(zeros) < i)[0]) > 0 else 0
        right = zeros[np.where(np.array(zeros) > i)[0][0]] if len(np.where(np.array(zeros) > i)[0]) > 0 else len(y)
        if [left, right] not in ranges:
            ranges.append([left, right])
    return baseline, ranges
