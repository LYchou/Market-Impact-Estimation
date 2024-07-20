import numpy as np
import pandas as pd
from numba import njit, prange
from numba.typed import List
import bottleneck as bn
from functools import wraps

EPSILON = 1e-15

@njit
def cs_zscore(input, univ):
    m = cs_mean(input, univ)
    s = cs_std(input, univ)
    res = (input - m) / s
    return res

@njit
def cs_mean(input, univ):
    res = input.copy()
    valid = np.bitwise_and(np.isfinite(input), univ)
    for t in prange(input.shape[0]):
        cs = res[t, :]
        v_cs = valid[t, :]
        m = np.mean(cs[v_cs]) if len(cs[v_cs]) > 0 else np.nan
        cs[v_cs] = m
        cs[~v_cs] = np.nan
        res[t, :] = cs
    return res

@njit
def cs_std(input, univ):
    res = input.copy()
    valid = np.bitwise_and(np.isfinite(input), univ)
    for t in prange(input.shape[0]):
        cs = res[t, :]
        v_cs = valid[t, :]
        s = np.std(cs[v_cs]) if len(cs[v_cs]) > 0 else np.nan
        cs[v_cs] = s
        cs[~v_cs] = np.nan
        cs[cs < EPSILON] = np.nan
        res[t, :] = cs
    return res