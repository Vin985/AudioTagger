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
        self.speed = 1

    def __del__(self):
        self.terminate()

    def open_stream(self):
        self.stream = self.pa.open(format=self.pa.get_format_from_width(self.wave_file.getsampwidth()),
                                   channels=self.nchannels,
                                   rate=int(self.sr * self.speed),
                                   output=True,
                                   start=False,
                                   stream_callback=self.read_frames)

    def load(self, file_path):
        self.close_file()
        try:
            self.wave_file = wave.open(file_path, 'rb')
            self.nchannels = self.wave_file.getnchannels()
            self.sr = self.wave_file.getframerate()
            self.open_stream()
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

    def close_file(self):
        if self.wave_file:
            self.wave_file.close()
        if self.stream:
            self.stream.close()

    def terminate(self):
        self.close_file()
        if self.pa:
            self.pa.terminate()

    def seek(self, pos):
        pos_frame = int(pos * self.sr)
        self.wave_file.setpos(pos_frame)

    def change_speed(self, speed):
        self.speed = speed
        self.stream.close()
        self.open_stream()
