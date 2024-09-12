"""This module contains utility methods to test a video readers output the expected frames"""

import logging
import signal
import subprocess

import ffmpeg  # type: ignore
import numpy as np  # type: ignore
import tqdm

logger = logging.getLogger(__name__)


def create_video(data: list, final_filename: str, size: int = 10, red_shift: int = 11, green_shift: int = 17):
    """Create a CFR or VFR video file whose frame index can be identified by the frame color
    Args:
        data (list): a list of tuple in the following format: [(filename, framerate, frame_count), ...]
        final_filename (str):  the name of the final video file (unused if len(data) == 1)
        size (int): width and height of the video
        red_shift (int): the amount of red that is added to each frame (loop at 256)
        green_shift (int): the amount of green that is added to each frame  (loop at 256)
    """
    total_frame_count = sum([frame_count for _, _, frame_count in data])
    # Create the frames
    frame_array: np.typing.NDArray = np.ndarray(shape=(total_frame_count, size, size, 3), dtype=np.uint8)
    for frame_idx in range(total_frame_count):
        frame_array[frame_idx, :, :, :] = np.full(
            (size, size, 3),
            (np.uint8((frame_idx * red_shift) % 256), np.uint8((frame_idx * green_shift) % 256), np.uint8(0)),
        )

    used_frames = 0
    for filename, framerate, frame_count in data:
        # Create the video file for the framerate section:
        process = (
            ffmpeg.input('pipe:', format='rawvideo', r=framerate, pix_fmt='rgb24', s=f'{size}x{size}')
            .output(filename, pix_fmt='yuv420p', vcodec='libx264', r=framerate)
            .overwrite_output()
            .run_async(pipe_stdin=True)
        )
        for frame in frame_array[used_frames : used_frames + frame_count]:
            process.stdin.write(frame.astype(np.uint8).tobytes())
        process.stdin.close()
        process.wait()
        used_frames += frame_count

    if len(data) > 1:
        ffmpeg.concat(*[ffmpeg.input(filename, r=framerate) for filename, framerate, _ in data]).output(
            final_filename, vsync='vfr'
        ).overwrite_output().run()


def expected_frame_color(frame_index: int, red_shift: int = 11, green_shift: int = 17):
    """Return the expected frame color for the given frame index of a video created by the create_video method
    Args:
        frame_index (int): the frame index
        red_shift (int): the amount of red that is added to each frame (loop at 256)
        green_shift (int): the amount of green that is added to each frame  (loop at 256)
    Returns:
        tuple: the expected frame color (red, green, blue)
    """
    return np.uint8((frame_index * red_shift) % 256), np.uint8((frame_index * green_shift) % 256), np.uint8(0)


def is_almost_same_color(color1: np.uint8, color2: np.uint8):
    """This method normalize color comparisons of a frame encoded using the create_video method
    It account for the fact that encoding will slightly degrade colors
    Args:
        color1 (np.uint8): the color to compare
        color2 (np.uint8): the expected color
    Returns:
        bool: True if the color is close enough to the expected color
    """
    return abs(int(color1) - int(color2)) < 4


class Timeout:
    """
    This class is used to run a block of code with a timeout.
    It is meant to be used as a context manager, for example:
    ```
        with Timeout(5):
            do_something()
    ```
    """

    class TimeoutException(Exception):
        pass

    def __init__(self, timeout: float):
        """Create a Timeout object
        Args:
            timeout (float): the timeout in seconds
        """
        self.timeout = timeout

    @staticmethod
    def handler(signum, frame):
        raise Timeout.TimeoutException()

    def __enter__(self):
        signal.signal(signal.SIGALRM, Timeout.handler)
        signal.setitimer(signal.ITIMER_REAL, self.timeout)

    def __exit__(self, exc_type, value, traceback):
        if exc_type == Timeout.TimeoutException:
            return True


def decode_all_frames(
    file_path: str,
    framerate: int = 10,
    use_gpu: bool = True,
    log_progress: bool = False,
    ignore_edit_list: bool = True,
) -> dict:
    """Extract all frames' PTS from a video file and mark which frame is kept or dropped for a given framerate
    Args:
        file_path (str): the path to the video file, can be a url
        framerate (int): the framerate to use to decide which frame to keep or drop
        use_gpu (bool): if True, the process is accelerated using the GPU
        log_progress (bool): if True, display the current frame index and decoding speed
    Returns:
        dict: a dictionary mapping frames' PTS to a boolean indicating if the frame is kept or dropped
    """
    all_frame = {}
    kept_frame = {}
    if log_progress:
        pbar = tqdm.tqdm(total=-1, ascii=False, unit=' frames')
        pbar.set_description(f'Reading log {"*ignore edit list active*" if ignore_edit_list else ""}')
    process = subprocess.Popen(
        [
            f'ffmpeg {"-hwaccel cuda" if use_gpu else ""} {"-ignore_editlist true" if ignore_edit_list else ""} \
    -i "{file_path}" -filter_complex [0]fps=fps={framerate}[s0] -map [s0] -an -f null - -v debug 2>&1 | grep Parsed_fps'
        ],
        stdout=subprocess.PIPE,
        universal_newlines=True,
        shell=True,
    )

    for line in iter(process.stdout.readline, ''):
        if 'Read frame with in pts ' in line:
            read_line = line.split('Read frame with in pts ')[1].split(', out pts ')
            read_in = float(read_line[0])
            read_out = float(read_line[1])
            all_frame[read_in] = False
            if read_out not in kept_frame:
                kept_frame[read_out] = []
            kept_frame[read_out].append(read_in)
            if log_progress:
                pbar.update()
        elif 'Dropping frame with pts ' in line:
            drop = float(line.split('Dropping frame with pts ')[1])
            if drop in kept_frame:
                kept_frame[drop] = kept_frame[drop][1:]
            else:
                logger.warning('No frame to drop ******************')
    process.stdout.close()
    return_code = process.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, process.args)

    for read_out, read_ins in kept_frame.items():
        if len(read_ins) > 1:
            logger.warning('out frame %s has more than one in frame', read_out)
        elif len(read_ins) == 0:
            logger.warning('out frame %s has no in frame', read_out)
        else:
            all_frame[read_ins[0]] = True

    if log_progress:
        pbar.close()
    return all_frame
