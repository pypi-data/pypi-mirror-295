import numpy as np
from cached_property import cached_property
from spike_handling import cluster_exceptions

from spike_handling.get_cluster_region_labels import get_cluster_region_label


class Cluster(object):
    def __init__(self, spike_struct, cluster_id):
        self.spike_struct = spike_struct
        self.cluster_id = cluster_id
        self.stimuli = []


    @property
    def group(self):
        """

        :return group: the group label assigned by manual clustering
        (usually done in phy: https://github.com/kwikteam/phy-contrib)
        """
        return self.spike_struct.groups[self.cluster_id]

    @property
    def best_channel_waveforms(self):
        """

        :return array best_channel_waveforms: every spike waveform for this cluster from the channel that is calculated
        as being closest to the source
        """
        return np.squeeze(self.waveforms[:, self.best_channel, :])

    @property
    def best_channel(self):
        """

        :return best_channel: the index of the channel that is calculated as being closest to the source
        """
        return self._get_channel_with_greatest_negative_deflection()

    def _get_channel_with_greatest_negative_deflection(self):
        _, min_channel = np.unravel_index(
            self.normalised_avg_waveforms.argmin(), self.avg_waveforms.shape
        )
        return min_channel

    @property
    def avg_waveforms(self):
        """

        :return avg_waveforms: the average waveform of the cluster's spikes, calculated for every channel and organised
         in a n_chan x t array where n_chan is the number of channels on the probe and t the number of samples in each
         waveform
        """
        return np.array(np.mean(self.waveforms, axis=2))

    @property
    def normalised_avg_waveforms(self):
        wfm = self.avg_waveforms
        med = np.median(wfm, axis=0)
        return wfm - med

    def _subtract_baseline_from_waveforms(self, waveforms):
        """

        :param waveforms:
        :return: median normalised waveforms
        """
        return waveforms - self.spike_struct.get_traces_median(
            n_samples=100000
        )

    @cached_property
    def waveforms(self, subtract_baseline=False, limit=100):
        """

        :param subtract_baseline: if the data are not normalised, some median correction needs to be applied to correct
        for the different baselines of the channels
        :return array waveforms: all spike waveforms across all channels and n_chan x t x n_waveforms
        """
        waveforms = self._get_spike_waveforms_on_all_channels(
            n_samples_before_peak=20, n_samples_after_peak=40, limit=limit
        )
        if subtract_baseline:
            waveforms = self._subtract_baseline_from_waveforms(waveforms)
        return waveforms

    def _get_spike_waveforms_on_all_channels(
        self, n_samples_before_peak, n_samples_after_peak, limit=None
    ):
        """

        :param int n_samples_before_peak:
        :param int n_samples_after_peak:
        :return np.array all_waveforms:
        """
        n_chan = self.spike_struct.n_chan
        spike_times = self.spike_times[:limit]
        n_waveforms = len(spike_times)
        n_waveform_samples = n_samples_before_peak + n_samples_after_peak

        all_waveforms = np.zeros((n_waveform_samples, n_chan, n_waveforms))

        for i, spike_time in enumerate(spike_times):
            if not (
                np.issubdtype(type(spike_time), np.int)
                or np.issubdtype(type(spike_time), np.uint)
            ):
                raise cluster_exceptions.SpikeTimeTypeError(
                    "got spike time:{}, type:{} expected "
                    "type: {}".format(spike_time, type(spike_time), int)
                )

            start_of_waveform = max(0, int(spike_time - n_samples_before_peak))
            end_of_waveform = int(
                spike_time + n_samples_after_peak
            )  # TODO min(len(trace), )

            waveform_on_all_channels = self.spike_struct.traces[
                start_of_waveform:end_of_waveform, :
            ]
            all_waveforms[:, :, i] = waveform_on_all_channels

        return all_waveforms

    def get_spike_times_in_interval(self, start, end):
        """

        :param start:
        :param end:
        :return spike_times: the time (n_samples) of all spikes that occur between the given start and end samples
        """
        spike_mask = np.logical_and(
            self.spike_times > start, self.spike_times < end
        )
        spike_times = self.spike_times[spike_mask]
        return spike_times

    @property
    def spike_times(self):
        """

        :return spike_times: the time of all spikes that belong to this cluster
        """
        return self.spike_struct.get_spike_times_in_cluster(self.cluster_id)

    def passes_criteria(self):
        (
            cluster_ids,
            _,
        ) = self.spike_struct.cluster_ids_that_pass_quality_measures()
        return self.cluster_id in cluster_ids

    def region_label(self, implant_distance=3000, tip_taper_distance=175):
        print(f"implant distance: {implant_distance}")
        print(f"tip taper distance: {tip_taper_distance}")
        cid, region_label, depth = get_cluster_region_label(
            self.spike_struct.mtd.histology_dir,
            self.spike_struct.mtd.kilosort_dir,
            self.cluster_id,
            implant_distance_um=implant_distance,
            tip_taper_distance=tip_taper_distance
        )
        return region_label, depth

    def __gt__(self, other):
        implant_distance=self.spike_struct.implant_distance
        return self.region_label(implant_distance)[1] < other.region_label(implant_distance)[1]

    def __lt__(self, other):
        implant_distance=self.spike_struct.implant_distance
        return self.region_label(implant_distance)[1] > other.region_label(implant_distance)[1]

    def curation_group(self):
        return self.spike_struct.groups[
            self.spike_struct.groups["cluster_id"] == self.cluster_id
        ]["group"].values[0]

    def metric_dict(self, implant_distance=3000):
        region, depth = self.region_label(implant_distance)
        metric_dict = {
            "mouse_id": self.spike_struct.mtd.mouse_id,
            "cluster_id": self.cluster_id,
            "passes_quality_criteria": self.passes_criteria(),
            "curation_group": self.curation_group(),
            "region": region,
            "depth": depth,
        }
        return metric_dict
