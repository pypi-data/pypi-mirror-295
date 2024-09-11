def load_probe_data_memmap(path, n_chan):
    data = np.memmap(path, dtype="int16")
    if data.shape[0] % n_chan != 0:
        raise ValueError("n_chan is incorrect, try again")
    shape = (int(data.shape[0] / n_chan), n_chan)
    shaped_data = np.memmap(path, shape=shape, dtype="int16")
    return shaped_data, shape
