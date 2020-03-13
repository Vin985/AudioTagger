import os
import shutil
from pathlib import Path

import pandas as pd

import AudioTagger.db_utils as db_utils
from pysoundplayer import audio


def create_subsample(audio_file, interval, labels, new_file, dest_dir, labels_dest_dir, overwrite):

    start = interval[0]
    end = interval[1]

    dest_file = str(dest_dir.joinpath(new_file))
    if not os.path.exists(dest_file) or overwrite:
        print("Creating new file: " + new_file)
        audio_file.write(
            file_path=dest_file, start=start, end=end)

    # If the file has labels
    if labels is not None:
        # Get the labels associated to the extract
        start_s = audio_file.frames_to_seconds(start)
        end_s = audio_file.frames_to_seconds(end)
        current_labels = labels.loc[(labels.LabelStartTime_Seconds.between(start_s, end_s)) |
                                    (labels.LabelEndTime_Seconds.between(start_s, end_s))]
        # If the extract has labels, change their time
        if not current_labels.empty:
            current_labels = current_labels.copy()
            current_labels.LabelStartTime_Seconds -= start_s
            current_labels.LabelEndTime_Seconds -= start_s

            # Make sure the labels now fit in the sample
            current_labels.loc[current_labels.LabelStartTime_Seconds <
                               0, "LabelStartTime_Seconds"] = 0
            current_labels.loc[current_labels.LabelEndTime_Seconds >
                               end_s, "LabelStartTime_Seconds"] = end_s

            label_file_name = db_utils.create_label_filename(
                new_file, str(labels_dest_dir))
            label_dest_file = str(
                labels_dest_dir.joinpath(label_file_name))
            if not os.path.exists(label_dest_file) or overwrite:
                print("saving labels in:" + label_dest_file)
                current_labels.to_csv(label_dest_file)


def split_file(file_path, dest_dir, label_folder, labels_dest_dir,
               top_db=80, min_duration=0.75, overwrite=False):
    labels = None
    # Load file
    audio_file = audio.Audio(file_path)

    # Get intervals without silences
    sound_intervals = audio_file.get_sound_intervals(
        top_db=top_db, min_sound_duration=min_duration)

    label_file = db_utils.create_label_filename(
        os.path.basename(file_path), label_folder)

    # If the file needs to be splitted
    if len(sound_intervals) > 1:
        print("Splitting file: " + file_path)
        cpt = 1
        # Load label files if it exits
        if os.path.exists(label_file):
            labels = pd.read_csv(label_file)

        # Iterate on intervals
        for interval in sound_intervals:
            # Create new file name
            new_file = os.path.basename(
                file_path)[:-4] + "_" + str(cpt) + ".wav"
            create_subsample(audio_file, interval, labels,
                             new_file, dest_dir, labels_dest_dir, overwrite)
            cpt += 1
    else:
        shutil.copy(file_path, dest_dir)
        if os.path.exists(label_file):
            shutil.copy(label_file, labels_dest_dir)
        # break
    audio_file = None


def split_files(filelist, label_folder, dest_dir, **kwargs):
    # Path(self.base_folder).joinpath("new")
    dest_dir = Path("/home/vin/Desktop/test_split2")
    labels_dest_dir = dest_dir.joinpath("labels")

    if not labels_dest_dir.exists():
        labels_dest_dir.mkdir(parents=True, exist_ok=True)

    if filelist:
        for file_path in filelist:
            split_file(file_path, dest_dir, label_folder,
                       labels_dest_dir, **kwargs)

            # break
    print("Splitting done")
