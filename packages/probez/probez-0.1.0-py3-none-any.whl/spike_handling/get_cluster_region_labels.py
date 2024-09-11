import pandas as pd
import pathlib
import numpy as np

shank_mapping = {
    0: 0,
    32: 0,
    250: 1,
    282: 1,
    500: 2,
    532: 2,
    750: 3,
    782: 3,
}


def load_data(kilosort_output_directory):
    """load all kilosort numpy variables into a dictionary"""

    p = pathlib.Path(kilosort_output_directory)
    file_paths = list(p.rglob("*.npy"))
    return {p.stem: np.load(str(p)) for p in file_paths}


def get_best_channel(cluster_id, waveforms_folder):
    """Using output from quality measures, load waveforms and pick best channel for a given cluster"""

    waveforms_files = list(
        waveforms_folder.rglob("waveforms_{}.npy".format(cluster_id))
    )
    if len(waveforms_files) == 1:
        waveforms_file = waveforms_files[0]
    else:
        return None

    waveform = np.load(str(waveforms_file))
    avg_waveform = np.mean(waveform, axis=0)
    channel_mins = []
    for x in avg_waveform.T:
        channel_mins.append(np.min(x))

    return np.argmin(channel_mins)


def get_cluster_depth(cluster_id, data, kilosort_directory, shank_id=None):
    """use the estimation of the best channel to determine cluster location"""
    p = list(pathlib.Path(kilosort_directory).rglob("cluster_info.tsv"))
    phy_metadata = pd.read_table(str(p[0]))
    channel_id = phy_metadata[phy_metadata["cluster_id"] == cluster_id][
        "ch"
    ].values[0]
    if channel_id is None:
        return None, None
    channel_positions = data["channel_positions"]
    x, y = channel_positions[channel_id]
    if shank_id is None:
        shank_id = shank_mapping[x]
    depth = y
    return shank_id, depth


def get_region(track, depth, distance_key=None):
    """Use channel depth to select region from brainreg-segment data"""
    def find_nearest(array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx], idx

    if "Position" in track:
        distance_key = "Position"

    elif "Distance from first position [um]" in track:
        distance_key = "Distance from first position [um]"

    if distance_key is not None:
        distances = track[distance_key].values
        nearest_track_pos, nearest_track_pos_idx = find_nearest(distances, depth)
        region = track.iloc[nearest_track_pos_idx]["Region acronym"]

    else:
        print("couldn't find any position information for this track.. returning None")
        region = None
    return region


def get_cluster_region_label(
    brainreg_segment_dir,
    kilosort_folder,
    cluster_id,
    implant_distance_um=3000,
    surface=0,
    tip_taper_distance=175,
    shank_id=None,
):
    """use the channel position to select a brain region label for each cluster
    tracks must be drawn in the 'correct' order in brainreg-segment

    In phy 0 depth is the first channel. So we also need to add tip distance of 175um
    """
    data = load_data(kilosort_folder)
    p = pathlib.Path(brainreg_segment_dir)
    shank_id, depth = get_cluster_depth(
        cluster_id, data, kilosort_folder, shank_id=shank_id
    )

    if depth is not None:
        depth += tip_taper_distance

    if shank_id is None:
        return cluster_id, None, None

    print("cluster id: {}".format(cluster_id))
    print("shank id: {}".format(shank_id))
    print("cluster depth: {}".format(depth))

    this_track_path = list(p.rglob("track_{}.csv".format(shank_id)))
    assert len(this_track_path) == 1

    this_track = pd.read_csv(this_track_path[0])

    assert len(this_track) == implant_distance_um

    if surface == 0:
        depth = implant_distance_um - depth

    print(depth, implant_distance_um)

    if depth > 0:
        region = get_region(this_track, depth)
    else:
        region = None
    return cluster_id, region, depth
