"""This module extracts audio from video.

This module extracts audio from an input video file and saves it to
the output file.

Functions:
- main: Entry point.
- extract_audio: Extracts audio from video.

Usage:
The module can be used by importing it and calling the extract_audio
function.
"""
# Import built-in libraries.
import os

# Import third-party libraries.
from pydub import AudioSegment


def extract_audio(input_path: str, output_path: str) -> dict:
    """Extracts audio from video.

    Extracts audio from an input file and saves it to the output file.

    Args:
        input_path: Path to the input file.
        output_path: Path to save the output file.

    Returns:
        audio_info: A dict with file_name, duration (sec), channels.
    """
    # Load the audio from the input file.
    audio = AudioSegment.from_file(input_path, format="mp4")
    # Export the audio to the output file:
    # the sample rate: 16kHz;
    # the bit depth: 16-bit, by default;
    # channels: mono.
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(output_path, format="wav")
    audio_info = {
        "file_name": output_path,
        "duration": f"{round(audio.duration_seconds, 3)} s",
        "channels": audio.channels,
        "frame_rate": f"{audio.frame_rate} Hz",
        "bit_depth": f"{audio.frame_width * 8} bit"
    }
    return audio_info


def main() -> None:
    """Entry point."""
    module_dir = os.path.dirname(os.path.realpath(__file__))
    input_path = os.path.join(
        module_dir,
        "../data/Generative AI for business.mp4"
    )
    output_path = os.path.join(module_dir, "../data/audio.mp3")
    extract_audio(input_path, output_path)


if __name__ == "__main__":
    main()
