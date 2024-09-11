import pandas as pd


def get_events(starts, ends, cids, sp):
    """

    :param starts:
    :param ends:
    :param cids:
    :param sp:
    :return:
    """
    histograms_all = []
    raster_all = [[] for x in range(len(starts))]
    for cid in cids:
        histogram = get_events_from_cluster(cid, starts, ends, sp, flat=True)
        raster = get_events_from_cluster(cid, starts, ends, sp, flat=False)
        spike_times = get_events_from_cluster(
            cid, starts, ends, sp, flat=True, relative=False
        )
        histograms_all.extend(histogram)
        for i, t in enumerate(raster):
            raster_all[i].extend(list(t))
    return histograms_all, raster_all, spike_times


def get_events_from_cluster(cid, starts, ends, sp, flat=False, relative=True, time=True):
    events = []
    for s, e in zip(starts, ends):
        subtract_start = s if relative else 0
        spikes_in_window = (
            sp.cluster_spike_times_in_interval(cid, s, e) - subtract_start
        )
        if time:
            if len(spikes_in_window) > 0:
                spikes_in_window = spikes_in_window / sp.sample_rate
        if flat:
            events.extend(spikes_in_window)
        else:
            events.append(spikes_in_window)

    return events


def get_trial_events(trial, sp, camera_frame_times_on_probe_samples, relative=True, time=True):
    s = trial.session.time_to_ephys(trial.start, camera_frame_times_on_probe_samples)
    e = s + (sp.sample_rate * 6)
    cluster_ids_in_interval, \
    spike_times_in_interval = sp.get_spikes_and_clusters_in_interval(s,
                                                                     e,
                                                                     sp.data["spike_clusters"],
                                                                     sp.data["spike_times"])
    subtract_start = s if relative else 0
    spikes_in_window = (
        spike_times_in_interval - subtract_start
    )
    if time:
        if len(spikes_in_window) > 0:
            spikes_in_window = spikes_in_window / sp.sample_rate
    data_dict = {
                 "cluster_id": cluster_ids_in_interval,
                 "spike_times": spikes_in_window,
    }
    df = pd.DataFrame.from_dict(data_dict)

    return df
