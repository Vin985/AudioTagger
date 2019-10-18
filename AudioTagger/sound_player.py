import wave

import pyaudio


class SoundPlayer():
    def __init__(self):
        # init pyaudio
        self.pa = pyaudio.PyAudio()
        self.file_path = ""
        self.wave_file = None
        self.stream = None
        self.nchannels = 0
        self.sr = 0
        self.playing = False

    def __del__(self):
        self.terminate()

    def load(self, file_path):
        try:
            self.wave_file = wave.open(file_path, 'rb')
            self.nchannels = self.wave_file.getnchannels()
            self.sr = self.wave_file.getframerate()
            self.stream = self.pa.open(format=self.pa.get_format_from_width(self.wave_file.getsampwidth()),
                                       channels=self.nchannels,
                                       rate=self.sr,
                                       output=True,
                                       start=False,
                                       stream_callback=self.read_frames)
        except Exception as e:
            print("Error, could not load file: " + file_path)

    def play(self):
        print("playing")
        self.playing = True
        self.stream.start_stream()

    def read_frames(self, input_data, frame_count, time_info, status):
        data = self.wave_file.readframes(frame_count)
        return (data, pyaudio.paContinue)

    def pause(self):
        print("pausing")
        if self.stream.is_active():
            self.stream.stop_stream()
            self.playing = False

    def stop(self):
        print("stopping")
        if self.stream and self.stream.is_active() and self.wave_file:
            self.playing = False
            self.stream.stop_stream()
            self.wave_file.rewind()

    def terminate(self):
        if self.stream:
            self.stream.close()
        if self.pa:
            self.pa.terminate()

    def seek(self, pos):
        self.wave_file.setpos(int(pos * self.sr))
