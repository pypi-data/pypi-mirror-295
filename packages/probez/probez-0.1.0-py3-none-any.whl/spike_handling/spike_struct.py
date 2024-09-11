import os
import pathlib
from bisect import bisect_left

import numpy as np
import pandas as pd
from cached_property import cached_property
from util import generic_functions
from spike_handling import waveforms
from spike_handling import cluster_exceptions
from spike_handling.cluster import Cluster


FS = 30000


class SpikeStruct(object):

    """
    class for loading and manipulating KiloSort output files and processed data

    example usage:
    >>> sp = SpikeStruct(directory)  # create the SpikeStruct and load all variables
    >>> good_clusters = sp.get_clusters_in_group('good')  # get all the clusters in a specific group
    >>> depth_ordered_good_clusters =  sp.sort_cluster_ids_by_depth(good_clusters, descend=True)  # order them


    """

    def __init__(self, session_mtd, sample_rate=30000, implant_distance=None):
        self.mtd = session_mtd
        self.sample_rate = sample_rate
        self.n_chan = 384
        self.traces_path = self.mtd.kilosort_dir / "temp_wh.dat"
        #self.unique_cluster_ids = np.unique(self.data["spike_times"])

        self.x_coords = self.data["channel_positions"][:, 0]
        self.y_coords = self.data["channel_positions"][:, 1]

        if implant_distance is not None:
            self.implant_distance = implant_distance

        self.groups = self.read_groups()
        if self.read_groups() is not None:
            if "KSLabel" in self.groups.keys():
                self.read_ks_uncurated_outputs()
            else:
                self.read_curated_ks_groups()

    def read_curated_ks_groups(self):
        grouplabel = "group"
        self.good_clusters = self.groups[
            self.groups[grouplabel] == "good"
            ]["cluster_id"].values
        self.MUA_clusters = self.groups[
            self.groups[grouplabel] == "mua"
            ]["cluster_id"].values
        self.noise_clusters = self.groups[
            self.groups[grouplabel] == "noise"
            ]["cluster_id"].values
        self.unsorted_clusters = self.groups[
            self.groups[grouplabel] == "unsorted"
            ]["cluster_id"].values
        self.other = set(
            np.unique(self.data["spike_times"])
        ).difference(set(self.groups["cluster_id"]))

    def read_ks_uncurated_outputs(self):
        grouplabel = "KSLabel"
        self.good_clusters = self.groups[
            self.groups[grouplabel] == "good"
            ]["cluster_id"].values
        self.MUA_clusters = self.groups[
            self.groups[grouplabel] == "mua"
            ]["cluster_id"].values
        self.noise_clusters = self.groups[
            self.groups[grouplabel] == "noise"
            ]["cluster_id"].values
        self.unsorted_clusters = self.groups[
            self.groups[grouplabel] == "unsorted"
            ]["cluster_id"].values

    def cluster_ids_that_pass_quality_measures(self, good_only=True):
        if good_only:
            cluster_ids = self.good_clusters
        else:
            cluster_ids = np.unique(
                np.concatenate([self.good_clusters, self.MUA_clusters])
            )
        (
            quality_cluster_ids,
            quality_df,
        ) = get_cluster_ids_that_pass_quality_criteria(self.mtd.quality_path)
        for cid in cluster_ids:
            filtered_cids = [
                cid for cid in cluster_ids if cid in quality_cluster_ids
            ]
        return filtered_cids, quality_df

    def bombcell_quality(self):
        bombcell_groups = pd.read_table(self.mtd.kilosort_dir / "cluster_bc_unitType.tsv")
        self.good_clusters = bombcell_groups[
            bombcell_groups['bc_unitType'] == 'GOOD'
            ]["cluster_id"].values
        self.MUA_clusters = bombcell_groups[
            bombcell_groups['bc_unitType'] == "MUA"
            ]["cluster_id"].values
        self.noise_clusters = bombcell_groups[
            bombcell_groups['bc_unitType'] == "NOISE"
            ]["cluster_id"].values
        self.non_somatic = bombcell_groups[
            bombcell_groups['bc_unitType'] == "NON-SOMA"
            ]["cluster_id"].values

    @cached_property
    def data(self):
        data = {
            p.stem: np.load(str(p))
            for p in self.mtd.kilosort_dir.rglob("*.npy")
        }
        data['spike_clusters'] = data['spike_clusters'].flatten()
        data['spike_times'] = data['spike_times'].flatten()
        return data

    @cached_property
    def traces(self):
        """
        Traces_path should be the path to the raw or processed binary data. This is used primarily for extracting
        waveforms so it helps if the data are high pass filtered or processed in some way, but it shouldn't be essential
        :param limit: restrict the size of the data used to improve speed
        :return shaped_data:
        """
        return load_traces(self.traces_path, self.n_chan)

    def read_groups(self):
        """
        manual sorting output (from e.g. phy) is stored as cluster_groups.csv
        :return dictionary manually_labelled_cluster_groups: a dictionary of group_ids for every cluster
        """
        path = os.path.join(self.mtd.kilosort_dir, "cluster_group.tsv")
        if not os.path.isfile(path):
            print("no cluster groups file")
            return None
        df = pd.read_csv(path, sep="\t")

        return df

    def get_clusters_in_group(self, group):
        """
        :param group: the group that the user wants clusters from
        :return clusters: a list of all cluster_ids classified to a user defined group:
        """
        if self.groups is None:
            return
        return [key for key in self.groups.keys() if self.groups[key] == group]


    def get_spike_times_in_interval(self, start_t, end_t, spike_times=None):
        """

        :param start_t: start point (n_samples)
        :param end_t: end point (n_samples)
        :param spike_times: the set of spikes from which to get subset from
        :return spike_times: all spike times within a user specified interval
        """
        if spike_times is None:
            spike_times = self.data["spike_times"]
        start_idx = bisect_left(spike_times, start_t)
        end_idx = bisect_left(spike_times, end_t)
        return spike_times[start_idx:end_idx]

    def get_spike_cluster_ids_in_interval(
        self, start_t, end_t, spike_times=None, spike_clusters=None
    ):
        """

        :param start_t: start point (n_samples)
        :param end_t: end point (n_samples)
        :param spike_clusters: the set of spikes from which to get subset from
        :param spike_times:
        :return spike_clusters: all cluster ids within a user specified interval
        """
        if spike_times is None:
            spike_times = self.data["spike_times"]
        if spike_clusters is None:
            spike_clusters = self.data["spike_times"]
        start_idx = bisect_left(spike_times, start_t)
        end_idx = bisect_left(spike_times, end_t)
        return spike_clusters[start_idx:end_idx]

    def get_spike_times_in_cluster(self, cluster_id):
        """

        :param int cluster_id:
        :return spike times: an array of all spike times within a user specified cluster
        """

        return self.data["spike_times"][
            self.spikes_in_cluster_mask(cluster_id).squeeze()
        ]

    def spikes_in_cluster_mask(self, cluster_id):
        """
        a boolean mask of all indices of spikes that belong to a group of user defined clusters

        :param int cluster_id:
        :return:
        """

        return self.data["spike_times"] == cluster_id

    def cluster_spike_times_in_interval(
        self, cluster_id, start, end, spike_times=None, spike_clusters=None
    ):
        """
        This function returns the spikes within an interval for a particular cluster id.
        NOTE the implementation is designed to allow arbitrary sets of spike times to be divided up, so doesnt
        always have to work from the full set of spike times and clusters.

        :param cluster_id:
        :param start:
        :param end:
        :param spike_times:
        :param spike_clusters:
        :return:
        """

        if spike_times is None:
            spike_times = self.data["spike_times"]
            spike_clusters = self.data["spike_clusters"]

        cluster_ids_in_interval, spike_times_in_interval = self.get_spikes_and_clusters_in_interval(start,
                                                                                                    end,
                                                                                                    spike_clusters,
                                                                                                    spike_times)

        this_cluster = cluster_ids_in_interval == cluster_id
        spikes_in_cluster_and_interval = spike_times_in_interval[
            this_cluster.squeeze()
        ]

        return spikes_in_cluster_and_interval

    def get_spikes_and_clusters_in_interval(self, start, end, spike_clusters, spike_times):
        spike_times_in_interval = self.get_spike_times_in_interval(
            start, end, spike_times
        )
        cluster_ids_in_interval = self.get_spike_cluster_ids_in_interval(
            start, end, spike_times, spike_clusters
        )
        return cluster_ids_in_interval, spike_times_in_interval

    def get_cluster_channel_from_avg_waveforms(self, cluster_id, n_spikes=100):
        """
        calculates the location of the cluster based on the greatest deflection from baseline of the average waveforms
        on all channels. channel*10 roughly corresponds to the depth of the channel on the probe

        :param cluster_id:
        :param n_spikes: number of spikes considered to form average waveform
        :return:
        """
        spike_times = self.get_spike_times_in_cluster(cluster_id)
        cluster_channel = waveforms.get_channel_of_max_amplitude_avg_waveform(
            spike_times[:n_spikes], self.traces, self.n_chan
        )

        return cluster_channel

    @cached_property
    def cluster_depths(self):
        df = pd.read_csv(
            pathlib.Path(self.mtd.kilosort_dir) / "cluster_info.tsv", sep="\t"
        )[["cluster_id", "depth", "group"]]

        return df

    def all_unsorted_cluster_ids(self):
        df = pd.read_csv(
            pathlib.Path(self.mtd.kilosort_dir) / "cluster_info.tsv", sep="\t"
        )[["cluster_id", "depth", "group"]]
        unsorted = df['cluster_id'].unique()
        noise = self.groups[self.groups['group'] == 'noise']['cluster_id'].unique()

        return set(unsorted) - set(noise)

    def get_clusters_in_depth_range(self, lower, upper, group_label="mua"):
        """
        :param cluster_ids:
        :param lower: the lower layer (channel) bound
        :param upper: the upper layer (channel) bound
        :return cluster_ids: a list of clusters within the two bounds
        """
        df = self.cluster_depths
        df_in_depth_boundaries = df[
            (df["depth"] > lower)
            & (df["depth"] < upper)
            & (df["group"] == group_label)
        ]
        return df_in_depth_boundaries["cluster_id"].unique()

    def sort_cluster_ids_by_depth(
        self, cluster_ids=None, cluster_depths=None, descend=True
    ):
        """
        :param cluster_ids:
        :param cluster_depths:
        :param descend: if descending order is required then set this to true
        :return:
        """
        if cluster_ids is None:
            cluster_ids = self.good_clusters
        if cluster_depths is None:
            cluster_depths = self.cluster_depths

        sorted_cluster_ids, cluster_depths = generic_functions.sort_by(
            cluster_ids, cluster_depths, descend=descend
        )
        return sorted_cluster_ids, cluster_depths

    def get_data_for_spikes_in_interval_and_unit(
        self, cluster_id, start, end, data_key="amplitudes"
    ):
        spike_time_mask = np.logical_and(
            self.data["spike_times"] > start, self.data["spike_times"] < end
        )
        cluster_id_mask = np.logical_and(
            self.data["spike_clusters"] == cluster_id, spike_time_mask
        )
        spike_data = self.data[data_key][cluster_id_mask]
        return spike_data

    def get_spike_amplitudes(self, cid, start, end):
        amplitudes = self.get_data_for_spikes_in_interval_and_unit(
            cid, start, end, "amplitudes"
        )
        return np.array(generic_functions.flatten_list(amplitudes))

    def clusters(self, cluster_ids=None):
        if cluster_ids is None:
            cluster_ids = self.cluster_ids_that_pass_quality_measures()[0]
        return [Cluster(self, cid) for cid in cluster_ids]

    def all_non_noise_clusters(self):
        cluster_ids= self.all_unsorted_cluster_ids()
        clusters =[Cluster(self, cid) for cid in cluster_ids]
        return clusters #sorted(clusters)

    def clusters_by_region(self, implant_distance, tip_taper_distance):
        cluster_region_dict = {}
        for c in self.all_non_noise_clusters():
            cluster_region_dict.setdefault(c.region_label(implant_distance=implant_distance,
                                                          tip_taper_distance=tip_taper_distance)[0], []).append(c.cluster_id)
        return cluster_region_dict


def load_traces(traces_path, n_chan):
    if not os.path.isfile(traces_path):
        raise cluster_exceptions.SpikeStructLoadDataError(
            "file: {} does not exist".format(self.traces_path)
        )
    data = np.memmap(traces_path, dtype=np.int16)
    if data.shape[0] % n_chan != 0:
        raise cluster_exceptions.IncorrectNchanTracesStructError(
            data.shape[0], self.n_chan
        )
    shape = (int(data.shape[0] / n_chan), n_chan)
    shaped_data = np.memmap(traces_path, shape=shape, dtype=np.int16)
    return shaped_data
