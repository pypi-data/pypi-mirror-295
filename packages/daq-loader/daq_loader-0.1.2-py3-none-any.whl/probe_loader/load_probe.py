import warnings
import numpy as np
from xpmtd.sorting_metadata import contains_ephys
import pathlib
import matplotlib.pyplot as plt


def load_probe_data_memmap(traces_path, n_chan=385):
    traces_path = pathlib.Path(traces_path)
    if not traces_path.exists():
        raise FileNotFoundError("file: {} does not exist".format(traces_path))
    data = np.memmap(str(traces_path), dtype=np.int16)
    if data.shape[0] % n_chan != 0:
        raise IncorrectNchanTracesStructError(data.shape[0], n_chan)
    shape = (int(data.shape[0] / n_chan), n_chan)
    shaped_data = np.memmap(str(traces_path), shape=shape, dtype=np.int16)
    return shaped_data, shape


def fix_sync_baseline_shift_issue(trigger):
    """
    Sometimes the entire sync channel shifts by some fixed amount
    i.e. low val 0 -> high val 64 becomes low val 8 -> high val 72.
    This should correct the trigger such that there are only two unique values.

    :return:
    """
    if len(np.unique(trigger)) == 2:
        print(f"Trigger contains only two values -> returning trigger unmodified")
        return trigger
    elif len(np.unique(trigger)) == 4:
        trigger[trigger]


def get_frame_onsets_probe(session_name, mtd):
    s = mtd.get_session(session_name)
    if contains_ephys(s):
        trigger = load_clean_trigger(
            mtd.get_session(session_name).trigger_path
        )
        frame_onsets = np.where(np.diff((trigger > trigger.mean())))[0][::2]
        return frame_onsets


def get_session_stimulus_onset_times_ephys(session_trial_times_behav, mtd, sync_type='frames'):
    """
    This function accepts the stimulus onsets in camera time and converts them to probe time based
    on the assumption that the camera trigger is sent to the sync.
    :param session_trial_times_behav:
    :param mtd:
    :return:
    """
    session_trial_times_ephys = {}
    for session_name, trial_start_list in session_trial_times_behav.items():
        s = mtd.get_session(session_name)
        if s is None:
            continue
        if contains_ephys(s):
            trigger = load_clean_trigger(
                mtd.get_session(session_name).trigger_path
            )
            if sync_type == 'frames':
                frame_onsets = np.where(np.diff((trigger > trigger.mean())))[0][::2]
                trial_starts_on_probe_clock = [
                    frame_onsets[t_start] for t_start in trial_start_list[0]
                ]  # each camera sample is a TTL on the probe
                session_trial_times_ephys.setdefault(
                    session_name, trial_starts_on_probe_clock
                )
            elif sync_type == '1hz':
                print("stimulus time conversion not implemented for 1hz pulse yet")
                pass
            else:
                raise NotImplementedError()

    return session_trial_times_ephys


class IncorrectNchanTracesStructError(Exception):
    def __init__(self, n_datapoints, n_chan):
        super().__init__()
        self.n_dp = n_datapoints
        self.n_chan = n_chan

    def __str__(self):
        return (
            "n_chan incorrect, try again n_samples: {} divided "
            "by n_chan: {} not integer".format(self.n_dp, self.n_chan)
        )


def extract_trigger(session_mtd):

    if not session_mtd.trigger_path.exists():
        print(
            f"saving trigger from {session_mtd.raw_traces_path}\n to {session_mtd.trigger_path}"
        )
        traces_memmap = load_probe_data_memmap(
            str(session_mtd.raw_traces_path), n_chan=385
        )
        trigger = traces_memmap[:, -1]
        print(f"loaded trigger from {session_mtd.raw_traces_path}")
        np.save(session_mtd.trigger_path, trigger)
        print(f"saved trigger to {session_mtd.trigger_path}")


def load_clean_trigger(trigger_path, overwrite=False):
    """
    Sometimes the sync channel is contaminated with shot noise. This needs to be removed for subsequent TTL frame
    detection etc.

    :param trigger_path:
    :return:
    """
    clean_trigger_path = pathlib.Path(
        str(trigger_path).replace("trigger", "cleaned_trigger")
    )
    if overwrite or not clean_trigger_path.exists():
        trigger = np.load(str(trigger_path))

        if trigger[0] > 0:
            first_lowest = np.where(trigger == np.min(trigger))[0][0] # would be 0 but not always 0 for some reason
            trigger[:first_lowest] = 0

        if len(np.unique(trigger)) > 2:
            print(
                "more than 2 values detected in sync channel, correcting trigger..."
            )
            trigger[trigger > 75] = trigger[
                np.roll(trigger > 75, -1)
            ]  # cleans most of the shot noise
            mean_val = trigger.mean()
            trigger[trigger > mean_val] = np.max(trigger)
            trigger[trigger < mean_val] = np.min(trigger)

        np.save(str(clean_trigger_path), trigger)
    else:
        print("loading saved cleaned trigger")
        trigger = np.load(str(clean_trigger_path))
    assert len(np.unique(trigger)) == 2
    return trigger


def extract_all_sync_channels(mtd):
    for session in mtd.sessions:
        if not session.trigger_path:
            warnings.warn(f"Print session: {session.session_path_derivatives} does not have a trigger path, "
                          f"which might mean there is no ephys for this session")
            continue
        extract_trigger(session)
        scale_factor = sanity_check(session)
        print(f"scale factor: {scale_factor}")


def extract_and_concatenate_trigger(subject_path):

    path = pathlib.Path(subject_path)
    plot = True
    recording_order = [
        "1118406_botrow150_hstripe_pretest_g0",
        "1118406_botrow150_hstripe_LSE1_posttest1_g0",
    ]
    triggers = []
    pos = 0
    for fname in recording_order:
        recording_path = list(path.rglob(f"{fname}*.ap.bin"))[0]
        trigger = load_clean_trigger(recording_path)

        if plot:
            plt.plot(np.arange(len(trigger)) + pos, trigger, zorder=10)
            pos += len(trigger)

        triggers.append(trigger)
    concatenated_trigger = np.concatenate(triggers)
    np.save(str(path / "trigger_pre_lse_post.npy"), concatenated_trigger)
    if plot:
        plt.plot(concatenated_trigger)

    plt.show()
    print("done")


def sanity_check(session_mtd, sync_type="frames"):
    photodiode = np.load(list(session_mtd.behav_derivatives.rglob("photodiode.npy"))[0])
    trigger = load_clean_trigger(session_mtd.trigger_path, overwrite=False)
    camera_frame_times_detected_on_probe = np.where(np.diff(trigger > 40))[0][
        ::2
    ]
    print(session_mtd.behav_derivatives)
    n_clock_ticks_behav = len(photodiode)
    print(n_clock_ticks_behav, len(camera_frame_times_detected_on_probe))
    if sync_type == "frames":
        assert len(photodiode) == len(camera_frame_times_detected_on_probe)
    elif sync_type == "1hz":
        ttl_on_probe = camera_frame_times_detected_on_probe
        probe_sync_nidaq = np.load(list(session_mtd.behav_derivatives.rglob("probe_sync.npy"))[0])
        ttl_on_nidaq = np.where(np.diff(probe_sync_nidaq > 2))[0][::2]

        assert len(ttl_on_nidaq) == len(ttl_on_probe)

