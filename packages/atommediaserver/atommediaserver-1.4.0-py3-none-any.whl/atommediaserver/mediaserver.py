from ffmpeg import FFmpeg, Progress
import ctypes
import subprocess
import os
import sys
import numpy as np
import time
import threading
from multiprocessing import Event, shared_memory, Lock

if hasattr(sys, '_MEIPASS'):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

def run_server():
    dll_path = os.path.join(base_path, 'atommedia.dll')
    dll = ctypes.CDLL(dll_path)
    yml_path = os.path.join(base_path, 'atomconfig.yml')

    result = dll.RunMediaServer(yml_path.encode('utf-8'))

class RTSPStreamer:
    def __init__(self, width, height, output_postfix, quality, stop_event, shm_name, frame_shape, lock):
        self.width = width
        self.height = height
        self.output_postfix = output_postfix
        self.shm_name = shm_name
        self.frame_shape = frame_shape
        self.stop_event = stop_event
        self.frame_interval = 1 / 25
        self.lock = lock

        current_path = os.path.dirname(os.path.abspath(__file__))
        self.path_to_ffmpeg = os.path.join(current_path, 'decoder.exe')

        self.ffmpeg_command = [
            self.path_to_ffmpeg,
            '-y',
            '-f', 'rawvideo',
            '-fflags', 'nobuffer',
            '-flags', 'low_delay',
            '-probesize', '32',
            '-analyzeduration', '0',
            '-pix_fmt', 'bgra',
            '-s', f'{self.width}x{self.height}',
            '-i', 'pipe:0',
            '-c:v', 'mpeg4',
            '-qscale:v', f'{quality}',
            '-b:v', '20M',
            '-maxrate', '20M',
            '-bufsize', '40M',
            '-g', '1',
            '-f', 'rtsp',
            f'rtsp://localhost:8554/{self.output_postfix}'
        ]

        self.dark_frame = np.zeros((
                self.width,
                self.height,
                3
            ), dtype=np.uint8)

        self.process = None

    def start(self, conn, _):
        self.process = subprocess.Popen(self.ffmpeg_command, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        next_frame_time = time.time()

        existing_shm = shared_memory.SharedMemory(name=self.shm_name)

        frame = np.ndarray(self.frame_shape, dtype=np.uint8, buffer=existing_shm.buf)

        while not self.stop_event.is_set():
            try:
                current_time = time.time()

                if current_time >= next_frame_time:
                    with self.lock:
                        self.send_frame_to_ffmpeg(frame)
                    next_frame_time = current_time + self.frame_interval

                time.sleep(0.005)

            except EOFError:
                break
            except BrokenPipeError:
                break
            except Exception as e:
                continue

        existing_shm.close()

    def stop(self):
        self.running = False
        self.process.stdin.close()
        self.process.wait()

    def send_frame_to_ffmpeg(self, frame):
        self.process.stdin.write(frame.tobytes())
    