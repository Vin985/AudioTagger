
import csv
import os.path

from bidict import bidict

TO_APPEND = "-sceneRect2"

WAV_EXTENSIONS = [".wav", ".WAV"]

COLUMNS = bidict({"id": "id",
                  "file": "Filename",
                  "label": "Label",
                  "timestamp": "LabelTimeStamp",
                  "nstep": "Spec_NStep",
                  "nwin": "Spec_NWin",
                  # "x1": "Spec_x1",
                  # "y1": "Spec_y1",
                  # "x2": "Spec_x2",
                  # "y2": "Spec_y2",
                  "start": "LabelStartTime_Seconds",
                  "end": "LabelEndTime_Seconds",
                  "min_freq": "MinimumFreq_Hz",
                  "max_freq": "MaximumFreq_Hz",
                  "max_amp": "MaxAmp",
                  "min_amp": "MinAmp",
                  "mean_amp": "MeanAmp",
                  "amp_sd": "AmpSD",
                  "area_datapoints": "LabelArea_DataPoints",
                  "overlap": "overlap",
                  "related": "Related"})


def create_label_filename(file, folder, to_append=TO_APPEND, ext='.csv'):
    file_ext = file[-4:]
    if file_ext in WAV_EXTENSIONS:
        # Everything other than last 4 characters, i.e. .wav
        filename = file[:-4]
    else:
        raise RuntimeError("Program only works for wav files")
    filename += to_append + ext
    filename = os.path.join(folder, filename)

    return filename


def save_csv(file, folder, labels, columns=COLUMNS, to_append=TO_APPEND):
    filename = create_label_filename(
        file, folder, to_append=to_append, ext='.csv')

    if not os.path.exists(folder):
        os.makedirs(folder)

    with open(filename, "w") as f:
        dest_columns = list(COLUMNS.values())
        writer = csv.DictWriter(f=f, fieldnames=dest_columns, dialect='excel')
        writer.writeheader()
        for label in labels:
            lbl = {columns[key]: value for key,
                   value in label.items() if key in columns}
            writer.writerow(lbl)


def load_csv(file, folder, columns=COLUMNS, to_append=TO_APPEND):
    filename = create_label_filename(
        file, folder, to_append=to_append, ext='.csv')

    if os.path.exists(filename):
        res = []
        with open(filename, "r") as f:
            reader = csv.DictReader(f, dialect='excel')
            for line in reader:
                lbl = {columns.inverse[key]: value for key,
                       value in line.items() if key in columns.values()}
                res.append(lbl)

    return res
