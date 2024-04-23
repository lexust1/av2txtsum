# Import built-in libraries.
import os

# Import third-party libraries.
from pydub import AudioSegment
from pydub.silence import split_on_silence, detect_silence, detect_nonsilent


def split_audio(input_path: str,
                output_path: str,
                segment_length: float,
                min_silence_len: int,
                silence_thresh: int):
    """Splits an audio file into segments.

    Splits an audio file into segments based on silence detection.

    Args:
        input_path (str): Path to the input audio file.
        output_path (str): Path to the output directory where segments
            will be saved.
        segment_length (float): Target length of each segment in
            seconds.
        min_silence_len (int): Minimum length of silence that will be
            considered for splitting.
        silence_thresh (int): Threshold value for silence detection.

    Returns:
        None
    """
    # Load the audio file
    audio = AudioSegment.from_file(input_path, format="wav")
    # Detect silent frames.
    silences = detect_silence(
        audio,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh,
    )
    # print(silences, len(silences))
    # Determine the times to split the file based on silences
    k = 1
    times = [0]
    for start_time, end_time in silences:
        if start_time >= k * segment_length:
            times.append(start_time)
            k += 1
    times.append(len(audio))
    # print(times, len(times))
    # Split the file into segments
    for i in range(len(times) - 1):
        start_time, end_time = times[i], times[i + 1]
        segment = audio[start_time : end_time]
        file_name = f"{output_path}/segment_{i + 1:06d}_{round(segment.duration_seconds, 1)}.wav"
        segment.export(
            file_name,
            format="wav"
        )
        print(f"{file_name} has been created.")
        # print(round(audio.duration_seconds, 3), audio.channels, audio.frame_rate, audio.frame_width * 8)


def main():
    """Entry point."""
    module_dir = os.path.dirname(os.path.realpath(__file__))
    input_path = os.path.join(
        module_dir,
        "../data/audio.wav"
    )
    output_path = os.path.join(module_dir, "../data/audio_segments")
    split_audio(input_path, output_path, 10000, 100, -30)


if __name__ == "__main__":
    main()
