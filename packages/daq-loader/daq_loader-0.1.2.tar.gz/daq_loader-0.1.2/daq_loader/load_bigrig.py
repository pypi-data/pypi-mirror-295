import pandas as pd
import numpy as np
import pathlib
import matplotlib.pyplot as plt
import skvideo.io


def load_analog_bin(bonsai_directory):
    """
    Acquisition software stores a binary file called analog.bin.
    This file contains 5 channels, recorded on the same clock and should
    therefore consist of 5 channels of equal length.

    This function loads the data and separates it into its different channels

    :param bonsai_directory: the directory path that contains the data
    :return data_dictionary: a dictionary containing channel names and
    their corresponding data
    """

    if isinstance(bonsai_directory, str):
        bonsai_directory=pathlib.Path(bonsai_directory)

    bonsai_binary_filepath = bonsai_directory / "analog.bin"
    derivatives_directory = pathlib.Path(str(bonsai_directory).replace('rawdata', 'derivatives'))

    data_dictionary = {}
    data_dictionary_downsampled={}
    channel_labels = ['camera_sync_pulse', 'auditory_stimulus', 'photodiode',
                      'probe_sync', 'microphone']

    filepaths = [derivatives_directory / f'{x}.npy' for x in channel_labels]

    if all(fpath.exists() for fpath in filepaths):
        for fpath in filepaths:
            data_dictionary_downsampled.setdefault(fpath.stem, np.load(fpath))

    else:
        derivatives_directory.mkdir(parents=True, exist_ok=True)
        data = np.fromfile(bonsai_binary_filepath)
        n_channels = len(channel_labels)
        channel_length = data.shape[0] / n_channels
        assert(channel_length.is_integer())
        channels = data.reshape(int(channel_length), n_channels)

        for key, channel in zip(channel_labels, channels.T):
            data_dictionary.setdefault(key, channel)

        camera_sync_idx = get_camera_frame_idx(data_dictionary['camera_sync_pulse'])

        for key, channel in zip(channel_labels, channels.T):
            data_dictionary_downsampled.setdefault(key, channel[camera_sync_idx])
            if key in ['camera_sync_pulse', 'probe_sync']:
                np.save(derivatives_directory / key, channel)
            else:
                np.save(derivatives_directory / key, channel[camera_sync_idx])
    return data_dictionary_downsampled, data_dictionary


def get_camera_frame_idx(camera_sync_pulse):
    """
    One of the data streams we load is a TTL pulse - voltage changing from 0 to 5
    volts periodically in a square wave at 40hz. This is used to trigger the
    camera so each time the voltage changes from 0 to 5 a camera frame should
    be acquired.

    :param camera_sync_pulse: TTL pulse of 0 to 5 volts
    :return: the indices of the transitions from 0 to 5
    """

    #TODO: test this
    ttl_on = camera_sync_pulse > 2
    ttl_on_off_transitions = np.diff(ttl_on)
    on_idx = np.where(ttl_on_off_transitions)[0]
    return on_idx[::2]


def load_camera_metadata(bonsai_directory):
    """
    When the camera actually acquires a frame, it saves a timestamp which can be used
    to verify that requested frames were well received. Here we load the metadata file
    that should contain timestamp information.

    :param bonsai_directory:
    :return:
    """
    if isinstance(bonsai_directory, str):
        bonsai_directory=pathlib.Path(bonsai_directory)
    df = pd.read_csv(bonsai_directory / "cam_metadata.csv")
    return df


def number_of_dropped_frames(bonsai_directory):
    """
    By comparing the number of transitions from 0 to 5 with the number of timestamps
    recorded we can identify how many frames were dropped in the recording.
    :param bonsai_directory:
    :return:
    """

    data, data_raw = load_analog_bin(bonsai_directory)
    number_of_requested_frames = get_camera_frame_idx(data['camera_sync_pulse'])
    df = load_camera_metadata(bonsai_directory)
    number_of_received_frames=len(df['Item3'].values)

    return number_of_requested_frames - number_of_received_frames


def visual_stimulus_onsets(data):
    """
    Stimuli are visual Using the photodiode trace
    :param derivatives_folder:
    :return:
    """

    photodiode = data['photodiode']
    baseline = np.median(photodiode[:200])
    std=np.std(photodiode[:200])
    stimulus_on = photodiode < (baseline-(std*10))
    stimulus_transitions = np.diff(stimulus_on)
    stimulus_idx = np.where(stimulus_transitions)[0][::2]
    plt.figure()
    plt.plot(photodiode)
    plt.plot(stimulus_idx, np.ones_like(stimulus_idx)*5, 'o')
    plt.show()
    return stimulus_idx


def video_length(bonsai_directory):
    #bonsai_directory = pathlib.Path(str(bonsai_directory).replace('derivatives', 'rawdata'))
    video_paths = list(bonsai_directory.glob('cam.avi'))
    if len(video_paths) > 0:
        video_path = video_paths[0]
        vid_reader = skvideo.io.FFmpegReader(str(video_path))
        (numframe, _, _, _) = vid_reader.getShape()
    else:
        numframe=None
    return numframe

