import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat
import cluster_exceptions as ce

from util import mat_utils

SAMPLE_RATE = 30000


class Stimulus(object):

    """
    locations of stimuli, and sub-stimuli to be interpreted by Cluster instances and used to extract spikes
    """

    def __init__(self, n_samples, wfm=None, condition=None, sp=None):
        self.start = 0
        self.end = n_samples
        self.relative_start = 0  # FIXME: probably can be removed
        self.relative_end = self.end - self.start
        self.sub_stimuli = []
        self.condition = condition
        self.offset = 0
        self.sp = sp
        self.duration_in_samples = self.end - self.start
        self.duration_in_seconds = self.duration_in_samples / SAMPLE_RATE

    @property
    def labels(self):
        return [sub.label for sub in self.sub_stimuli]

    def create_sub_stimulus(self, start, end, label):
        sub_stimulus = SubStimulus(start, end, label)
        self._append_sub_stimulus(sub_stimulus)

    def create_sub_stimuli(self, sub_region_starts, sub_region_ends, labels):
        for start, end, label in zip(
            sub_region_starts, sub_region_ends, labels
        ):
            sub_stimulus = SubStimulus(self, start, end, label)
            self._append_sub_stimulus(sub_stimulus)

    def _append_sub_stimuli(self, sub_stimuli):
        """

        :param list sub_stimuli:
        :return:
        """
        for sub_stimulus in sub_stimuli:
            self._append_sub_stimulus(sub_stimulus)

    def _append_sub_stimulus(self, sub_stimulus):
        if not self.relative_start <= sub_stimulus.start <= self.relative_end:
            raise ce.SubStimulusNotInRangeError(
                "sub_stimulus of start: {} and end: {} does not fit in "
                "range start: {} end: {}".format(
                    sub_stimulus.start,
                    sub_stimulus.end,
                    self.relative_start,
                    self.relative_end,
                )
            )

        if any([sub_stimulus == x for x in self.sub_stimuli]):
            raise ce.SubStimulusAlreadyPresentError(
                "sub-stimulus with start: {} and end: {} is already attached to "
                "this stimulus".format(sub_stimulus.start, sub_stimulus.end)
            )
            # TODO: more info in exception?

        self.sub_stimuli.append(sub_stimulus)

    def plot_waveform(self):
        plt.plot(self.wfm)

    def sort_sub_stimuli(self):
        self.sub_stimuli = np.sort(self.sub_stimuli)

    def __add__(self, other):
        # if not isinstance(other, int):
        #     raise TypeError('expected {} got {}'.format(int, type(other)))

        self.start += other
        self.end += other

        for sub_stimulus in self.sub_stimuli:
            sub_stimulus += other

    def reset(self):
        self.end -= self.start
        for sub_stimulus in self.sub_stimuli:
            sub_stimulus -= self.start
        self.start -= self.start


class SubStimulus(object):
    def __init__(self, stimulus, relative_start, relative_end, label=None):
        """

        :param stimulus_struct.stimulus:
        :param relative_start:
        :param relative_end:
        :param label:
        """
        self.start = relative_start
        self.end = relative_end
        self.duration_in_samples = relative_end - relative_start
        self.label = label
        self.stimulus = stimulus
        self.duration_in_seconds = self.duration_in_samples / SAMPLE_RATE

    def __lt__(self, other):
        return self.start < other.start

    def __gt__(self, other):
        return self.start > other.start

    def __eq__(self, other):
        if self.start == other.start and self.end == other.end:
            return True

    def __add__(self, other):
        self.start += other
        self.end += other

    def __sub__(self, other):
        self.start -= other
        self.end -= other

    def __same_group__(self, other):
        return np.isclose(
            self.duration_in_samples, other.duration_in_samples, rtol=1e-04
        )

    def get_data(self, cid, key):
        if key == "events":
            return self.events(cid)
        elif key == "n_events":
            return self.n_events(cid)
        elif key == "rate":
            return self.rate(cid)

    def events(self, cid):
        events = self.stimulus.sp.cluster_spike_times_in_interval(
            cid, self.start, self.end
        )
        return events

    def n_events(self, cid):
        return len(self.events(cid))

    def rate(self, cid):
        return self.n_events(cid) / self.duration_in_seconds

    @property
    def stripped_label(self):
        return "".join([i for i in self.label if not i.isdigit()])

    def plot(self, shift_factor=0):
        plt.plot(
            self.stimulus.waveform[self.start : self.end] + shift_factor,
            color="k",
            linewidth=0.5,
        )


class MateoStimulus(Stimulus):
    def __init__(self, n_samples, matlab_waveform_path=None, waveform=None):
        if waveform:
            self.waveform = waveform
        if matlab_waveform_path is not None:
            wfm = self.load_waveform_in_ms_from_matlab(matlab_waveform_path)
            self.waveform = self.upsample_waveform(wfm)
            n_samples = len(self.waveform)

        super().__init__(n_samples)

    def rotation_sub_stimuli(self, baseline_start=0, baseline_end=60000):
        peaks = mat_utils.findSinePeaks(self.waveform)
        cw1 = SubStimulus(peaks[0], peaks[1], "cw_1")
        acw1 = SubStimulus(peaks[1], peaks[2], "acw_1")
        bsl1 = SubStimulus(baseline_start, baseline_end, "bsl_1")
        cw2 = SubStimulus(peaks[2], peaks[3], "cw_2")
        acw2 = SubStimulus(peaks[3], peaks[4], "acw_2")
        bsl2 = SubStimulus(
            baseline_start + baseline_end, 2 * baseline_end, "bsl_2"
        )
        self._append_sub_stimuli([cw1, acw1, bsl1, cw2, acw2, bsl2])

    def stimulus_and_stationary_sub_stimuli(self):
        (
            rotation_start,
            rotation_end,
        ) = self.get_stimulus_boundaries_from_waveform()
        baseline_pre = SubStimulus(0, rotation_start, "baseline_pre")
        stimulus = SubStimulus(rotation_start, rotation_end, "stimulus")
        baseline_post = SubStimulus(
            rotation_end, len(self.waveform), "baseline_post"
        )
        self._append_sub_stimuli([baseline_pre, stimulus, baseline_post])

    def get_stimulus_boundaries_from_waveform(self):
        rotation_locations = np.where(self.waveform)[0]
        stimulus_start = rotation_locations[0]
        stimulus_end = rotation_locations[-1]
        return stimulus_start, stimulus_end

    @staticmethod
    def upsample_waveform(wfm, scale_factor=30):
        x = np.linspace(0, len(wfm) * scale_factor, len(wfm))
        y = wfm.flatten()
        x_vals = np.linspace(
            0, len(wfm) * scale_factor, len(wfm) * scale_factor
        )
        upsampled_command_waveform = np.interp(x_vals, x, y)
        return upsampled_command_waveform

    @staticmethod
    def load_waveform_in_ms_from_matlab(path):
        return loadmat(path)["waveform"]["data"][0][0]

    def _as_dictionary(self):
        import collections

        stim_dict = collections.OrderedDict()
        for sub in sorted(self.sub_stimuli):
            stim_dict[sub.label] = (sub.start, sub.end)
        return stim_dict


class SepiStimulus(Stimulus):
    def __init__(
        self,
        trigger,
        matlab_waveform_path=None,
        waveform=None,
        sp=None,
        condition=None,
    ):
        self.condition = condition
        self.matlab_waveform_path_template = matlab_waveform_path
        self.trigger = trigger

        if waveform:
            self.waveform = waveform

        if matlab_waveform_path is not None:
            wfm = self.load_waveform_in_ms_from_matlab(
                self.matlab_waveform_path
            )
            self.waveform = self.upsample_waveform(wfm)

        n_samples = len(self.waveform)
        super().__init__(n_samples, condition=condition, sp=sp)
        self.rotation_sub_stimuli()

    def rotation_sub_stimuli(self):
        peaks = mat_utils.findSinePeaks(self.waveform)
        (
            rotation_start,
            rotation_end,
        ) = self.get_stimulus_boundaries_from_waveform()
        cw = SubStimulus(self, peaks[0], peaks[1], "cw1")
        acw = SubStimulus(self, peaks[1], peaks[2], "acw1")
        baseline_pre_short = SubStimulus(
            self,
            rotation_start - cw.duration_in_samples,
            rotation_start,
            "baseline_pre_short",
        )
        baseline_post_short = SubStimulus(
            self,
            rotation_end,
            rotation_end + cw.duration_in_samples,
            "baseline_post_short",
        )

        baseline_pre = SubStimulus(self, 0, rotation_start, "baseline_pre")
        rotation = SubStimulus(self, rotation_start, rotation_end, "stimulus")
        baseline_post = SubStimulus(
            self, rotation_end, len(self.waveform), "baseline_post"
        )
        self._append_sub_stimuli(
            [
                baseline_pre_short,
                cw,
                acw,
                baseline_post_short,
                baseline_pre,
                rotation,
                baseline_post,
            ]
        )

    def stimulus_and_stationary_sub_stimuli(self):
        (
            rotation_start,
            rotation_end,
        ) = self.get_stimulus_boundaries_from_waveform()
        baseline_pre = SubStimulus(self, 0, rotation_start, "baseline_pre")
        stimulus = SubStimulus(self, rotation_start, rotation_end, "stimulus")
        baseline_post = SubStimulus(
            self, rotation_end, len(self.waveform), "baseline_post"
        )
        self._append_sub_stimuli([baseline_pre, stimulus, baseline_post])

    def get_stimulus_boundaries_from_waveform(self):
        rotation_locations = np.where(self.waveform)[0]
        stimulus_start = rotation_locations[0]
        stimulus_end = rotation_locations[-1]
        return stimulus_start, stimulus_end

    def substimuli_grouped_by_duration(self):
        stimuli_groups = {}
        for sub in self.sub_stimuli:
            if sub.duration_in_samples not in stimuli_groups.keys():
                stimuli_groups[sub.duration_in_samples] = []
            stimuli_groups[sub.duration_in_samples].extend(sub)
        return stimuli_groups

    @staticmethod
    def upsample_waveform(wfm, scale_factor=30):
        x = np.linspace(0, len(wfm) * scale_factor, len(wfm))
        y = wfm.flatten()
        x_vals = np.linspace(
            0, len(wfm) * scale_factor, len(wfm) * scale_factor
        )
        upsampled_command_waveform = np.interp(x_vals, x, y)
        return upsampled_command_waveform

    @staticmethod
    def load_waveform_in_ms_from_matlab(path):
        return loadmat(path)["waveform"]["data"][0][0]

    def _as_dictionary(self):
        import collections

        stim_dict = collections.OrderedDict()
        for sub in sorted(self.sub_stimuli):
            stim_dict[sub.label] = (sub.start, sub.end)
        return stim_dict

    def plot_sub_stimuli(self):
        self.plot_waveform(scale_factor=0.4)
        sub_stimulus_groups = self.substimuli_grouped_by_duration()
        for i, (duration, sub_stimuli) in enumerate(
            sub_stimulus_groups.items()
        ):
            for sub, color in zip(
                sub_stimuli, ["r", "b", "c", "g", "y"]
            ):  # FIXME: flexible color
                plt.hlines(
                    i, sub.start, sub.end, color=color, linewidth=20, alpha=0.4
                )

    def unique_labels(self):
        all_labels = np.array([sub.stripped_label for sub in self.sub_stimuli])
        _, idx = np.unique(all_labels, return_index=True)
        unique_labels_order_preserved = all_labels[np.sort(idx)]
        return unique_labels_order_preserved

    def plot_waveform(self, shift_factor=0, scale_factor=1.0, ax=None):
        x = np.arange(len(self.waveform)) + self.trigger
        if ax is None:
            ax = plt.subplot(111)
        ax.plot(
            x,
            self.waveform * scale_factor + shift_factor,
            color="k",
            linewidth=0.5,
        )

    def set_condition(self, condition):
        self.condition = condition

    @property
    def matlab_waveform_path(self):
        import re

        if self.condition is None:
            return None
        if self.condition == "None":
            return None
        rotation_angle = int(re.search(r"\d+", self.condition).group())
        waveform_filepath = self.matlab_waveform_path_template.format(
            rotation_angle
        )
        return waveform_filepath

    def get_data(self, cid, key):
        if key == "events":
            return self.events(cid)
        elif key == "n_events":
            return self.n_events(cid)
        elif key == "rate":
            return self.rate(cid)

    def events(self, cid):
        events = self.sp.cluster_spike_times_in_interval(
            cid, self.start, self.end
        )
        return events

    def n_events(self, cid):
        return len(self.events(cid))

    def rate(self, cid):
        return self.n_events(cid) / self.duration_in_seconds


class LoomStimulus(Stimulus):
    def __init__(self, loom_idx, sp=None, condition=None):
        self.condition = condition
        self.trigger = loom_idx[0]

        super().__init__(15 * 30000, condition=condition, sp=sp)
        self.loom_idx = loom_idx
        self.loom_sub_stimuli()

    def loom_sub_stimuli(self):
        start = 0
        stimulus_onset = 5 * 30000
        stimulus_offset = 10 * 30000
        end = 15 * 30000
        looms = [
            SubStimulus(
                self,
                loom - self.trigger + stimulus_onset,
                loom - self.trigger + 0.45 * 28000 + stimulus_onset,
                "loom{}".format(i),
            )
            for i, loom in enumerate(self.loom_idx)
        ]
        baseline_pre = SubStimulus(self, start, stimulus_onset, "baseline_pre")
        rotation = SubStimulus(
            self, stimulus_onset, stimulus_offset, "stimulus"
        )
        baseline_post = SubStimulus(
            self, stimulus_offset, end, "baseline_post"
        )
        self._append_sub_stimuli([baseline_pre, rotation, baseline_post])
        self._append_sub_stimuli(looms)

    def substimuli_grouped_by_duration(self):
        stimuli_groups = {}
        for sub in self.sub_stimuli:
            if sub.duration_in_samples not in stimuli_groups.keys():
                stimuli_groups[sub.duration_in_samples] = []
            stimuli_groups[sub.duration_in_samples].extend(sub)
        return stimuli_groups

    def _as_dictionary(self):
        import collections

        stim_dict = collections.OrderedDict()
        for sub in sorted(self.sub_stimuli):
            stim_dict[sub.label] = (sub.start, sub.end)
        return stim_dict

    def plot_sub_stimuli(self, relative=False):
        sub_stimulus_groups = self.substimuli_grouped_by_duration()
        for i, (duration, sub_stimuli) in enumerate(
            sub_stimulus_groups.items()
        ):
            for sub, color in zip(
                sub_stimuli, ["r", "b", "c", "g", "y"]
            ):  # FIXME: flexible color
                if "loom" in sub.label:
                    if relative:
                        plt.hlines(
                            i,
                            sub.start - 150000,
                            sub.end - 150000,
                            color=color,
                            linewidth=80,
                            alpha=0.4,
                        )
                    else:
                        plt.hlines(
                            i,
                            sub.start,
                            sub.end,
                            color=color,
                            linewidth=8000,
                            alpha=0.4,
                        )

    def unique_labels(self):
        all_labels = np.array([sub.stripped_label for sub in self.sub_stimuli])
        _, idx = np.unique(all_labels, return_index=True)
        unique_labels_order_preserved = all_labels[np.sort(idx)]
        return unique_labels_order_preserved

    def set_condition(self, condition):
        self.condition = condition

    def get_data(self, cid, key):
        if key == "events":
            return self.events(cid)
        elif key == "n_events":
            return self.n_events(cid)
        elif key == "rate":
            return self.rate(cid)

    def events(self, cid):
        events = self.sp.cluster_spike_times_in_interval(
            cid, self.start, self.end
        )
        return events

    def n_events(self, cid):
        return len(self.events(cid))

    def rate(self, cid):
        return self.n_events(cid) / self.duration_in_seconds
