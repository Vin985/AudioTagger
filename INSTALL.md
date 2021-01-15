python -m venv audiotagger

source audiotagger/bin/activate


pip install -U https://github.com/vin985/qimage2ndarray/archive/master.zip

pip install -U https://github.com/vin985/pysoundplayer/archive/master.zip

pip install -U https://github.com/vin985/pyqtextra/archive/master.zip


git clone https://github.com/Vin985/AudioTagger

cd AudioTagger

pip install -r requirements.txt


python run.py
