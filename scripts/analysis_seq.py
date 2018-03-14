import numpy as np
from scipy import signal

x = 0
y = 1
z = 2
value = 3

def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    r"""Smooth (and optionally differentiate) data with a Savitzky-Golay filter.
    The Savitzky-Golay filter removes high frequency noise from data.
    It has the advantage of preserving the original shape and
    features of the signal better than other types of filtering
    approaches, such as moving averages techniques.
    Parameters
    ----------
    y : array_like, shape (N,)
        the values of the time history of the signal.
    window_size : int
        the length of the window. Must be an odd integer number.
    order : int
        the order of the polynomial used in the filtering.
        Must be less then `window_size` - 1.
    deriv: int
        the order of the derivative to compute (default = 0 means only smoothing)
    Returns
    -------
    ys : ndarray, shape (N)
        the smoothed signal (or it's n-th derivative).
    """
    from math import factorial
    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
    except ValueError, msg:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order+1)
    half_window = (window_size -1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve( m[::-1], y, mode='valid')

class Analysis:
    def __init__(self, data):
        arr, unique = np.unique(data[:,:3],axis = 0,return_index=True)
        self.data = data[unique]
        self.zcut = np.empty(0)
        self.minimum = np.zeros(4)
        self.xy = None
        self.trap_depth = None
        self.max_e = None
    def getCentralZCut(self):
        line = np.array([i for i in self.data if (i[x] == 0 and i[y] == 0)])
        line[:,value] = savitzky_golay(line[:,value],11,4)
        self.zcut = line
        return self.zcut
    def getCentralMinimum(self):
        if (len(self.zcut) == 0):
            self.getCentralZCut()
        if (self.minimum.all() != 0):
            return self.minimum
        values = self.zcut[:,value]
        min_index = signal.argrelextrema(self.zcut[:,value],np.less)[0]
        if (len(min_index) > 0):
            self.minimum = self.zcut[np.where(self.zcut[:,value] == np.amin(self.zcut[min_index][:,value]))[0]][0]
        return self.minimum
    def getXYAtMinimumZ(self):
        if (self.minimum.any() == False):
            self.getCentralMinimum()
        if (self.minimum.any() == False):
            raise "No minimum."
        else:
            z_value = self.minimum[z]
            self.xy = np.array([i for i in self.data if i[z] == z_value])
            return self.xy
    def getTrapDepth(self):
        if (self.minimum.any() == False):
            self.getCentralMinimum()
        if (self.minimum.any() == False):
            self.trap_depth = 0
            return self.trap_depth
        max_index = signal.argrelextrema(self.zcut[:,value],np.greater)[0]
        if (len(max_index) > 0):
            i = 0
            while (self.zcut[i][value] == 0):
                i += 1
            max_peaks = np.append(self.zcut[np.where(self.zcut[:,value] == np.amax(self.zcut[max_index][:,value]))[0]][0],self.zcut[i]) #Can only be one maximum due to maxwell's equations
            max_peaks = max_peaks.reshape(len(max_peaks)/4,4)
            self.trap_depth = np.amin(max_peaks[:,value]) - self.minimum[value]
        else:
            self.trap_depth = 0
        return self.trap_depth
    def getMaximumE(self):
        self.max_e = np.amax(self.data[:,value])
        return self.max_e
    def getTrapRatio(self):
        if (self.trap_depth == None):
            self.getTrapDepth()
        if (self.max_e == None):
            self.getMaximumE()
        return self.trap_depth/self.max_e
