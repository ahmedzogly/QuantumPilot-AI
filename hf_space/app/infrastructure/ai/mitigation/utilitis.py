import numpy as np
from typing import Union, Tuple, Optional, Callable
from dataclasses import dataclass
from scipy import interpolate, optimize

def mean_squared_error(y_true, y_pred, sample_weight=None, multioutput='uniform_average', squared=True):
    """
    Compute mean squared error between y_true and y_pred.
    
    Parameters
    ----------
    y_true : array-like of shape (n_samples,) or (n_samples, n_outputs)
        Ground truth (correct) target values.
    
    y_pred : array-like of shape (n_samples,) or (n_samples, n_outputs)
        Estimated target values.
    
    sample_weight : array-like of shape (n_samples,), default=None
        Sample weights.
    
    multioutput : {'raw_values', 'uniform_average'} or array-like of shape (n_outputs,), default='uniform_average'
        Defines aggregating of multiple output values.
        'raw_values' : Returns a full set of errors in case of multioutput input.
        'uniform_average' : Errors of all outputs are averaged with uniform weight.
        array-like : Array of weights used to average errors.
    
    squared : bool, default=True
        If True returns MSE value, if False returns RMSE value.
    
    Returns
    -------
    loss : float or ndarray of floats
        A non-negative floating point value (the best value is 0.0), or an
        array of floating point values, one for each individual target.
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    if y_true.shape != y_pred.shape:
        raise ValueError("y_true and y_pred have different shapes")
    
    output_errors = np.average((y_true - y_pred) ** 2, axis=0, weights=sample_weight)
    
    if isinstance(multioutput, str):
        if multioutput == 'raw_values':
            if not squared:
                output_errors = np.sqrt(output_errors)
            return output_errors
        elif multioutput == 'uniform_average':
            output_errors = np.average(output_errors)
        else:
            raise ValueError("multioutput must be 'raw_values', 'uniform_average' or array-like")
    else:
        multioutput = np.array(multioutput)
        if multioutput.shape[0] != output_errors.shape[0]:
            raise ValueError("multioutput must have same length as number of outputs")
        output_errors = np.average(output_errors, weights=multioutput)
    
    if not squared:
        output_errors = np.sqrt(output_errors)
    
    return output_errors


def mean_absolute_error(y_true, y_pred, sample_weight=None, multioutput='uniform_average'):
    """
    Compute mean absolute error between y_true and y_pred.
    
    Parameters
    ----------
    y_true : array-like of shape (n_samples,) or (n_samples, n_outputs)
        Ground truth (correct) target values.
    
    y_pred : array-like of shape (n_samples,) or (n_samples, n_outputs)
        Estimated target values.
    
    sample_weight : array-like of shape (n_samples,), default=None
        Sample weights.
    
    multioutput : {'raw_values', 'uniform_average'} or array-like of shape (n_outputs,), default='uniform_average'
        Defines aggregating of multiple output values.
        'raw_values' : Returns a full set of errors in case of multioutput input.
        'uniform_average' : Errors of all outputs are averaged with uniform weight.
        array-like : Array of weights used to average errors.
    
    Returns
    -------
    loss : float or ndarray of floats
        A non-negative floating point value (the best value is 0.0), or an
        array of floating point values, one for each individual target.
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    if y_true.shape != y_pred.shape:
        raise ValueError("y_true and y_pred have different shapes")
    
    output_errors = np.average(np.abs(y_true - y_pred), axis=0, weights=sample_weight)
    
    if isinstance(multioutput, str):
        if multioutput == 'raw_values':
            return output_errors
        elif multioutput == 'uniform_average':
            output_errors = np.average(output_errors)
        else:
            raise ValueError("multioutput must be 'raw_values', 'uniform_average' or array-like")
    else:
        multioutput = np.array(multioutput)
        if multioutput.shape[0] != output_errors.shape[0]:
            raise ValueError("multioutput must have same length as number of outputs")
        output_errors = np.average(output_errors, weights=multioutput)
    
    return output_errors


@dataclass
class ExtrapolationResult:
    """Data class for extrapolation results"""
    extrapolated_value: float
    x_data: np.ndarray
    y_data: np.ndarray
    x_fit: np.ndarray
    y_fit: np.ndarray
    method: str
    order: Optional[int] = None
    # For generality, polynomial might not be poly1d (e.g., spline or function), changed to callable
    fit_function: Optional[Callable] = None

def extrapolation(
    y_values: Union[list, np.ndarray], 
    x_values: Union[list, np.ndarray], 
    method: str = 'linear',
    order: Optional[int] = None,
    x_target: float = 0.0,
    x_range: Optional[Tuple[float, float]] = None,
    spline_smoothing: float = 0.0  # Only for spline
) -> ExtrapolationResult:
    """
    Perform interpolation/fitting on given data points and extrapolate to specified point (default: 0)
    
    Parameters:
    -----------
    y_values : array-like
        Dependent variable data points (function values)
    x_values : array-like  
        Independent variable data points
    method : str
        Extrapolation method:
        - 'linear', 'quadratic', 'cubic', 'poly': Least squares polynomial fitting
        - 'linear_interp': Linear interpolation + linear extrapolation
        - 'spline': Spline interpolation (supports extrapolation)
        - 'exponential': Exponential fitting y = a*exp(b*x) + c
        - 'logarithmic': Logarithmic fitting y = a*log(x) + b (requires x > 0)
        - 'power_law': Power law fitting y = a * x^b (requires x > 0, y > 0)
        - 'nearest': Nearest neighbor extrapolation
        - 'constant': Constant extrapolation (mean value)
    order : int, optional
        Polynomial order, required when method='poly'
    x_target : float
        Target extrapolation point, default is 0
    x_range : tuple, optional
        X range for plotting fitted curve
    spline_smoothing : float
        Spline smoothing parameter (0 = interpolation, >0 = smoothing fit)
        
    Returns:
    --------
    ExtrapolationResult
    """
    y_values = np.array(y_values, dtype=float)
    x_values = np.array(x_values, dtype=float)

    if len(x_values) != len(y_values):
        raise ValueError("x_values and y_values must have same length")
    if len(x_values) == 0:
        raise ValueError("Input data cannot be empty")

    # Default plot range
    if x_range is None:
        x_min, x_max = np.min(x_values), np.max(x_values)
        range_extend = (x_max - x_min) * 0.2 if x_max != x_min else 1.0
        x_plot_min = min(x_target, x_min) - range_extend
        x_plot_max = max(x_target, x_max) + range_extend
    else:
        x_plot_min, x_plot_max = x_range

    x_fit = np.linspace(x_plot_min, x_plot_max, 200)
    extrapolated_value = None
    fit_func = None

    # ========== Polynomial fitting (least squares) ==========
    if method in ['linear', 'quadratic', 'cubic', 'poly']:
        if method == 'linear':
            poly_order = 1
        elif method == 'quadratic':
            poly_order = 2
        elif method == 'cubic':
            poly_order = 3
        elif method == 'poly':
            if order is None:
                raise ValueError("When method='poly', order parameter must be specified")
            poly_order = order
        else:
            raise RuntimeError("Should not reach here")

        if poly_order >= len(x_values):
            raise ValueError(f"Polynomial order {poly_order} cannot be >= number of data points {len(x_values)}")

        coeffs = np.polyfit(x_values, y_values, poly_order)
        polynomial = np.poly1d(coeffs)
        extrapolated_value = polynomial(x_target)
        y_fit = polynomial(x_fit)
        fit_func = polynomial
        order_out = poly_order

    # ========== Linear interpolation + extrapolation ==========
    elif method == 'linear_interp':
        # Use scipy's interp1d with extrapolation enabled
        f_interp = interpolate.interp1d(
            x_values, y_values, kind='linear', fill_value="extrapolate"
        )
        extrapolated_value = f_interp(x_target)
        y_fit = f_interp(x_fit)
        fit_func = f_interp
        order_out = None

    # ========== Spline interpolation (supports extrapolation) ==========
    elif method == 'spline':
        if len(x_values) < 2:
            raise ValueError("Spline interpolation requires at least 2 points")
        # Automatically select order (3 for cubic spline)
        k = min(3, len(x_values) - 1)
        try:
            spl = interpolate.UnivariateSpline(x_values, y_values, k=k, s=spline_smoothing)
        except Exception as e:
            # Fallback to interpolation spline
            spl = interpolate.make_interp_spline(x_values, y_values, k=k)
        extrapolated_value = spl(x_target)
        y_fit = spl(x_fit)
        fit_func = spl
        order_out = k

    # ========== Exponential fitting: y = a * exp(b * x) + c ==========
    elif method == 'exponential':
        def exp_func(x, a, b, c):
            return a * np.exp(b * x) + c

        # Initial guess
        y_mean = np.mean(y_values)
        a0 = (np.max(y_values) - np.min(y_values)) or 1.0
        b0 = 0.1 if x_values[-1] != x_values[0] else 0.0
        c0 = y_mean

        try:
            popt, _ = optimize.curve_fit(exp_func, x_values, y_values, p0=[a0, b0, c0], maxfev=5000)
            fit_func = lambda x: exp_func(x, *popt)
            extrapolated_value = fit_func(x_target)
            y_fit = fit_func(x_fit)
        except Exception as e:
            raise RuntimeError(f"Exponential fitting failed: {e}")
        order_out = None

    # ========== Logarithmic fitting: y = a * log(x) + b (requires x > 0) ==========
    elif method == 'logarithmic':
        if np.any(x_values <= 0):
            raise ValueError("Logarithmic fitting requires all x > 0")
        log_x = np.log(x_values)
        coeffs = np.polyfit(log_x, y_values, 1)  # Linear fitting log(x) vs y
        a, b = coeffs
        fit_func = lambda x: a * np.log(x) + b
        extrapolated_value = fit_func(x_target)
        y_fit = fit_func(x_fit)
        order_out = None

    # ========== Power law fitting: y = a * x^b (requires x > 0, y > 0) ==========
    elif method == 'power_law':
        if np.any(x_values <= 0) or np.any(y_values <= 0):
            raise ValueError("Power law fitting requires x > 0 and y > 0")
        log_x = np.log(x_values)
        log_y = np.log(y_values)
        coeffs = np.polyfit(log_x, log_y, 1)
        b, log_a = coeffs
        a = np.exp(log_a)
        fit_func = lambda x: a * np.power(x, b)
        extrapolated_value = fit_func(x_target)
        y_fit = fit_func(x_fit)
        order_out = None

    # ========== Richardson extrapolation: use interpolation polynomial to extrapolate to x=0 ==========
    elif method == 'richardson':
        n_points = len(x_values)
        
        # Recommended maximum order (avoid high-order oscillation)
        max_order = n_points  # Use at most 3rd order (4 points)
        poly_order = max_order

        if poly_order >= n_points:
            poly_order = n_points - 1

        try:
            coeffs = np.polyfit(x_values, y_values, poly_order)
            polynomial = np.poly1d(coeffs)
            extrapolated_value = polynomial(x_target)
            y_fit = polynomial(x_fit)
            fit_func = polynomial
            order_out = poly_order
        except Exception as e:
            raise RuntimeError(f"Richardson extrapolation failed: {e}")

    # ========== Nearest neighbor extrapolation ==========
    elif method == 'nearest':
        if x_target <= np.min(x_values):
            extrapolated_value = y_values[np.argmin(x_values)]
        elif x_target >= np.max(x_values):
            extrapolated_value = y_values[np.argmax(x_values)]
        else:
            # Within range, use interpolation
            extrapolated_value = np.interp(x_target, x_values, y_values)
        # Fitted curve: piecewise constant (simplified as nearest neighbor)
        y_fit = np.array([extrapolated_value] * len(x_fit))  # Simplified handling
        fit_func = lambda x: np.full_like(x, extrapolated_value, dtype=float)
        order_out = None

    # ========== Constant extrapolation (mean value) ==========
    elif method == 'constant':
        const_val = np.mean(y_values)
        extrapolated_value = const_val
        y_fit = np.full_like(x_fit, const_val)
        fit_func = lambda x: np.full_like(x, const_val, dtype=float)
        order_out = None

    else:
        raise ValueError(f"Unsupported extrapolation method: {method}")

    return ExtrapolationResult(
        extrapolated_value=float(extrapolated_value),
        x_data=x_values.copy(),
        y_data=y_values.copy(),
        x_fit=x_fit,
        y_fit=y_fit,
        method=method,
        order=order_out,
        fit_function=fit_func
    )