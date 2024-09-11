import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from cached_property import cached_property
import stimulus_struct

from util import generic_functions

PLOT_SPACE = 5000
sns.set_color_codes("muted")

# TODO: make generic and extract rotation-based stuff to sub-class


class Stimuli(object):
    def __init__(self, trigger_indices, sp):
        """

        :param stimulus_struct.SepiStimulus stimulus:
        :param list trigger_indices: the sample numbers of all the triggers that you want to analyse
        """
        self.trigger_list = trigger_indices
        self.sp = sp

    def grouplen(self, sequence, chunk_size):
        return list(zip(*[iter(sequence)] * chunk_size))

    def get_stimulus_template(self):
        stimulus_template = stimulus_struct.LoomStimulus(
            list(np.linspace(0, 28000 * 4, 5)), sp=self.sp
        )  # FIXME: rm hard code
        return stimulus_template

    @cached_property
    def stimuli(self):
        stimuli = []
        for trigger_group in self.grouplen(self.trigger_list, 5):
            stim = stimulus_struct.LoomStimulus(trigger_group, sp=self.sp)
            stim + trigger_group[0]
            stimuli.append(stim)
        return stimuli

    def get_event_data_all_sub_stimuli(
        self, cid, stimuli=None, relative=True, key="events"
    ):
        if stimuli is None:
            stimuli = self.stimuli

        # print('getting {} for cluster: {}'.format(key, cid))
        all_events = []
        labels = stimuli[0].unique_labels()

        for lbl in labels:
            sub_stimulus_events = []

            for stimulus in stimuli:
                for sub in stimulus.sub_stimuli:
                    events = sub.get_data(cid, key)

                    if relative:
                        events = events - sub.start

                    if lbl == sub.stripped_label:
                        sub_stimulus_events.append(events)

            all_events.append(sub_stimulus_events)

        return all_events, labels

    def get_rates_all_sub_stimuli(self, cid, stimuli=None):
        return self.get_event_data_all_sub_stimuli(
            cid=cid, stimuli=stimuli, relative=False, key="rate"
        )

    def get_n_events_all_sub_stimuli(self, cid, stimuli=None):
        return self.get_event_data_all_sub_stimuli(
            cid=cid, stimuli=stimuli, relative=False, key="n_events"
        )

    def get_events_all_stimuli(
        self, cid, condition=None, relative=True, key="events"
    ):
        stimuli = (
            self.stimuli
            if condition is None
            else self.get_stimuli_in_condition(condition)
        )
        all_events = []
        if stimuli is None:
            stimuli = self.stimuli
        for stimulus in stimuli:
            events = stimulus.get_data(cid, key)
            if relative:
                events = events - stimulus.start
            all_events.append(events)
        return all_events

    def get_rates_all_stimuli(self, cid, condition=None):
        return self.get_events_all_stimuli(
            cid=cid, condition=condition, relative=False, key="rate"
        )

    def get_n_events_all_stimuli(self, cid, condition=None):
        return self.get_events_all_stimuli(
            cid=cid, condition=condition, relative=False, key="n_events"
        )

    def plot_all_stimuli(
        self,
        cid,
        condition=None,
        relative=True,
        key="events",
        fig=None,
        color=None,
        n_bins=None,
    ):
        if fig is None:
            fig = plt.figure(facecolor="w", figsize=(15, 3))

        if condition is None:
            stimuli = self.stimuli
        else:
            stimuli = self.get_stimuli_in_condition(condition)

        stimulus_template = self.get_stimulus_template()

        all_events = self.get_events_all_stimuli(
            cid=cid, condition=condition, relative=relative, key=key
        )

        fig.add_subplot(211)
        plt.eventplot(all_events, colors=color, label=condition)
        fig.axes[0].set_yticks([])

        fig.add_subplot(212)
        self.plot_histogram(
            all_events,
            duration_in_samples=stimulus_template.end,
            label="",
            color=color,
            n_bins=n_bins,
        )
        stimulus_template.plot_sub_stimuli(relative=False)
        self.neaten_plots(fig.axes)
        self.neaten_plots(fig.axes[0:1], bottom=True, left=True)

        for ax in fig.axes:
            plt.axes(ax)
            plt.xlim(
                [0, self.stimuli[0].duration_in_samples]
            )  # FIXME: hardcode to first stimulus

    def plot_all_sub_stimuli(
        self,
        cid,
        condition=None,
        relative=True,
        fig=None,
        pyplot_override=False,
        n_bins=None,
    ):
        if fig is None:
            fig = plt.figure(facecolor="w", figsize=(30, 3))

        if condition is None:
            stimuli = self.stimuli

        else:
            stimuli = self.get_stimuli_in_condition(condition)

        event_lists, labels = self.get_event_data_all_sub_stimuli(
            cid=cid, stimuli=stimuli, relative=relative
        )
        histogram_axes = []
        raster_axes = []

        for i, (event_list, label) in enumerate(zip(event_lists, labels)):
            current_sub_stimulus = self.get_sub_stimulus(label)

            ax = fig.add_subplot(2, len(event_lists), i + 1)
            self.sp.plot_raster(event_list, label=label)

            plt.xlim(
                [
                    0 - PLOT_SPACE,
                    current_sub_stimulus.duration_in_samples + PLOT_SPACE,
                ]
            )
            plt.ylim([-5, len(event_list) + 5])
            # current_sub_stimulus.plot(shift_factor=len(event_list)/2)
            raster_axes.append(ax)

            ax = fig.add_subplot(2, len(event_lists), i + 1 + len(event_lists))
            self.plot_histogram(
                event_list,
                duration_in_samples=current_sub_stimulus.duration_in_samples,
                label=label,
                pyplot_override=pyplot_override,
                n_bins=n_bins,
            )
            plt.xlim(
                [
                    0 - PLOT_SPACE,
                    current_sub_stimulus.duration_in_samples + PLOT_SPACE,
                ]
            )
            histogram_axes.append(ax)
            stimulus_template = self.get_stimulus_template()
            if label == "stimulus":
                stimulus_template.plot_sub_stimuli(relative=True)

        self.normalise_axes(histogram_axes, space=5)
        self.neaten_plots(fig.axes)
        self.neaten_plots(raster_axes, bottom=True)

    def get_sub_stimulus(self, label):
        stimulus_template = self.get_stimulus_template()
        for sub in stimulus_template.sub_stimuli:
            if label == sub.stripped_label:
                return sub

    @staticmethod
    def plot_raster(
        events, label=None
    ):  # TODO: extract for use in many modules
        plt.eventplot(events)
        if label is not None:
            plt.title(label)

    def plot_histogram(
        self,
        events,
        duration_in_samples,
        label=None,
        bin_duration_s=0.25,
        color=None,
        ax=None,
        scale_factor=1,
        pyplot_override=False,
        n_bins=None,
    ):
        hist_events = np.array(generic_functions.flatten_list(events))
        if n_bins is None:
            n_bins = int(duration_in_samples / 30000 / bin_duration_s)
        bins = np.linspace(0, duration_in_samples, n_bins)
        hist, bin_edges = np.histogram(hist_events, bins=bins)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.0

        if ax is None:
            # plt.step(bin_centers, hist/scale_factor, color=color)
            plt.hist(hist_events, bins=bins, histtype="step")
        else:
            if pyplot_override:
                ax.hist(hist_events, bins=bins, histtype="step", color=color)
            else:
                ax.step(bin_centers, hist / scale_factor, color=color)
        if label is not None:
            plt.title(label)

    @staticmethod
    def normalise_axes(axes, space=0):
        lower = min([ax.get_ylim()[0] for ax in axes])
        upper = max([ax.get_ylim()[1] for ax in axes])
        for ax in axes:
            ax.set_ylim([lower, upper + space])

    @staticmethod
    def neaten_plots(axes, top=True, right=True, left=False, bottom=False):
        for ax in axes:
            sns.despine(ax=ax, top=top, right=right, left=left, bottom=bottom)

    def get_stimuli_in_condition(self, condition):
        return [stim for stim in self.stimuli if stim.condition == condition]

    def get_events_all_stimuli_cluster_groups(self, cids, condition=None):
        from probez.util import generic_functions

        all_events = []
        for cid in cids:
            events = self.get_events_all_stimuli(cid, condition=condition)
            all_events.extend(generic_functions.flatten_list(events))
        return all_events

    def plot_data(
        self,
        cid,
        ax,
        plot_type="raster",
        condition=None,
        relative=True,
        key="events",
        color=None,
        scale_factor=1,
        n_bins=None,
        bin_duration_s=0.25,
    ):
        if condition is None:
            stimuli = self.stimuli
        else:
            stimuli = self.get_stimuli_in_condition(condition)

        stimulus_template = self.get_stimulus_template()
        all_events = self.get_events_all_stimuli(
            cid=cid, condition=condition, relative=relative, key=key
        )

        if plot_type == "raster":
            ax.eventplot(all_events, colors=color, label=condition)
            ax.set_yticks([])
            sns.despine(ax=ax, top=True, right=True, left=True, bottom=True)

        elif plot_type == "histogram":
            self.plot_histogram(
                all_events,
                duration_in_samples=stimulus_template.end,
                label="",
                color=color,
                ax=ax,
                scale_factor=scale_factor,
                pyplot_override=True,
                n_bins=n_bins,
                bin_duration_s=bin_duration_s,
            )
            sns.despine(ax=ax, top=True, right=True)

    @staticmethod
    def calculate_stimuli_scale_ratio(stim_struct, condition, speed):
        """

        :return normalising_factor: normalising factor for different number of stimuli in light and dark for plotting
        """
        other = "dark {}" if condition == "light {}" else "light {}"

        stimuli_a = stim_struct.get_stimuli_in_condition(
            condition.format(speed)
        )
        stimuli_b = stim_struct.get_stimuli_in_condition(other.format(speed))
        arg = np.argmax([len(stimuli_a), len(stimuli_b)])
        if arg == 1:
            n_most_stimuli = max(len(stimuli_a), len(stimuli_b))
            n_fewest_stimuli = min(len(stimuli_a), len(stimuli_b))
            ratio = n_most_stimuli / n_fewest_stimuli
        else:
            ratio = 1

        return ratio

    def get_histogram_data(
        self,
        cid,
        bin_duration_s=0.25,
        scale_factor=1,
        n_bins=None,
        condition=None,
        relative=True,
        key="events",
    ):
        if condition is None:
            stimuli = self.stimuli
        else:
            stimuli = self.get_stimuli_in_condition(condition)

        stimulus_template = self.get_stimulus_template()

        all_events = self.get_events_all_stimuli(
            cid=cid, condition=condition, relative=relative, key=key
        )
        hist_events = np.array(generic_functions.flatten_list(all_events))
        if n_bins is None:
            n_bins = int(
                stimulus_template.duration_in_samples / 30000 / bin_duration_s
            )
        bins = np.linspace(0, stimulus_template.duration_in_samples, n_bins)
        hist, bin_edges = np.histogram(hist_events, bins=bins)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.0
        normalised_hist = hist / scale_factor
        return normalised_hist, bin_centers
