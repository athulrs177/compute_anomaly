# -*- coding: utf-8 -*-

import numpy as np
import xarray as xr

def smthClmDay(clmDay, nHarm):
    """
    Smooth climatology data by removing high-frequency harmonic modes.
    
    Parameters:
        clmDay (xarray.DataArray): Input climatological data array with dimensions ('hourofyear', 'lat', 'lon').
        nHarm (int): Number of harmonic modes to retain.
        
    Returns:
        xarray.DataArray: Smoothed climatological data array.
    """
    cf = np.fft.rfft(clmDay, axis=0)  # Compute the Fourier transform of climatological data
    
    # Retain only the specified number of harmonic modes
    cf[nHarm,:,:] = 0.5 * cf[nHarm,:,:]  # Apply a mini-taper
    cf[nHarm+1:,:,:] = 0.0               # Set all higher coefficients to zero
    
    # Compute the inverse Fourier transform to obtain smoothed climatological data
    clmDaySmth = np.fft.irfft(cf, axis=0)
    
    # Pad the last day with zeros if necessary to match the length
    if clmDaySmth.shape[0] < clmDay.shape[0]:
        clmDaySmth = np.concatenate((clmDaySmth, np.zeros_like(clmDaySmth[0:1, :, :])), axis=0)
    
    # Convert the smoothed climatological data array to xarray.DataArray
    clmDaySmth = xr.DataArray(clmDaySmth, dims=('hourofyear', 'lat', 'lon'),
                              coords={'hourofyear': clmDay.hourofyear, 'lat': clmDay.lat, 'lon': clmDay.lon})
    
    return clmDaySmth

def anomaly(data, nHarm):
    """
    Compute anomaly by subtracting smoothed climatology from the input data.
    
    Parameters:
        data (xarray.DataArray): Input data array with dimensions ('time', 'lat', 'lon').
        nHarm (int): Number of harmonic modes to retain for smoothing climatology.
        
    Returns:
        xarray.DataArray: Anomaly data array.
    """
    # Compute hour-of-year climatology
    data['hourofyear'] = xr.DataArray(data.indexes['time'].strftime('%m-%d %H'), coords=data.time.coords)
    clm = data.groupby('hourofyear').mean('time')
    
    # Smooth climatology
    sm_clm = smthClmDay(clm, nHarm)
    
    # Compute anomaly by subtracting smoothed climatology from raw data
    anom = data.groupby('hourofyear') - sm_clm
    
    return anom

