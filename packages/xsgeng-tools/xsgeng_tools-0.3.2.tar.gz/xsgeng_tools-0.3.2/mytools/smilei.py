import os
import numpy as np
from scipy.constants import pi
import h5py


def read_scalar(path, keyword):
    scalars = os.path.join(path, 'scalars.txt')

    data = []
    with open(scalars, mode='r') as f:
        data_start = False
        data_loc = None
        for line in f.readlines():
            if line.find(keyword) > 0:
                if line.strip('#').split()[0].isnumeric():
                    continue
                data_start = True
                data_loc = line.strip('#').split().index(keyword)
                continue
            if data_start:
                data.append(float(line.split()[data_loc]))
    return np.asarray(data, dtype=float)

def get_timesteps(result_path, number=0):
    with h5py.File(os.path.join(result_path, f'Fields{number}.h5'), 'r', locking=False) as h5f:
        ts = list(h5f['data'].keys())   
    return ts


def get_extent(result_path, number=0, component='Ey', lambda0=0.8e-6):
    '''
    get 2D extent
    '''
    with h5py.File(os.path.join(result_path, f'Fields{number}.h5'), 'r', locking=False) as h5f:
        ts = list(h5f['data'].keys())
        nx, ny = h5f['data'][ts[0]][component].shape
        dx, dy = h5f['data'][ts[0]][component].attrs['gridSpacing']

    return np.array([0, nx*dx, 0, ny*dy]) / 2/pi * lambda0 /1e-6


def get_cellsize(result_path, number=0, component='Ey', lambda0=0.8e-6):
    '''
    get 2D or 3D cell size in um
    '''
    with h5py.File(os.path.join(result_path, f'Fields{number}.h5'), 'r', locking=False) as h5f:
        ts = list(h5f['data'].keys())
        dset = h5f['data'][ts[0]][component]
        if dset.dims == 2:
            dx, dy = dset.attrs['gridSpacing']
            return dx/2/pi*lambda0/1e-6, dy/2/pi*lambda0/1e-6

        if dset.dims == 3:
            dx, dy, dz = dset.attrs['gridSpacing']
            return dx/2/pi*lambda0/1e-6, dy/2/pi*lambda0/1e-6, dz/2/pi*lambda0/1e-6

def get_field(result_path, ts, component, number=0, slice=()) -> np.ndarray:
    if isinstance(ts, int):
        ts = f'{ts:010d}'
    with h5py.File(os.path.join(result_path, f'Fields{number}.h5'), 'r', locking=False) as h5f:
        dset = h5f['data'][ts][component]
        if len(dset.shape) == 2:
            return dset[slice].T
        else:
            return dset[slice]


def get_traj(result_path, name, component):
    with h5py.File(os.path.join(result_path, f'TrackParticles_{name}.h5'), 'r', locking=False) as h5f:
        return h5f[component][()]