
import csv
import os.path

TO_APPEND = "-sceneRect"

WAV_EXTENSIONS = [".wav", ".WAV"]


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


def save_csv(file, folder, labels, columns, to_append=TO_APPEND):
    filename = create_label_filename(
        file, folder, to_append=to_append, ext='.csv')

    if not os.path.exists(folder):
        os.makedirs(folder)

    with open(filename, "w") as f:
        writer = csv.DictWriter(f=f, fieldnames=columns, dialect='excel')
        writer.writeheader()
        for label in labels:
            writer.writerow(label)


def load_csv(file, folder, to_append=TO_APPEND):
    filename = create_label_filename(
        file, folder, to_append=to_append, ext='.csv')

    if os.path.exists(filename):
        res = []
        with open(filename, "r") as f:
            reader = csv.DictReader(f, dialect='excel')
            for line in reader:
                res.append(line)

    return res
