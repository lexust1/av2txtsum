"""This module converts subtitle data from a txt-file into a srt-file.

This module convert subtitle data from a txt-file into a well-formatted
srt-file. The txt-file contains timestamps and subtitle text in a
specific format, and the module processes this data to generate a
corresponding srt-file.

Input Format of txt-file:
The txt-file should have timestamp and subtitle text entries.
Each timestamp is followed by the associated subtitle text.
The timestamp and text should be separated by a newline character.

Example:
0:09
>> Welcome to IBM THINK 2023!
0:17
>> AI generated art, AI generated songs.
0:23
AI, what is that? It sure is a lot of fun. But when foundation ...
0:31
you need to think bigger. Because AI and business needs to be held ...
0:36
Built to be trusted, secured, and adaptable. This isn't simple ...

Output Format of srt-file:
The module converts the input txt-file into a srt-file. Each subtitle
entry in the srt-file consists of an index number, the time range
during which the subtitle is displayed, and the subtitle text.

Example:
1
00:00:09,000 --> 00:00:17,000
>> Welcome to IBM THINK 2023!

2
00:00:17,000 --> 00:00:23,000
>> AI generated art, AI generated songs.

3
00:00:23,000 --> 00:00:31,000
AI, what is that? It sure is a lot of fun. But when foundation ...

4
00:00:31,000 --> 00:00:36,000
you need to think bigger. Because AI and business needs to be held ...

5
00:00:36,000 --> 00:00:42,000
Built to be trusted, secured, and adaptable. This isn't simple ...

Functions:
- main: Entry point.
- txt_to_srt: Converts a txt-file to a srt-file.
- _format_time: Formats a time string.
- _format_last_time: Formats a time string for the last time.
- _save_as_srt: Saves the given SRT content to the output path.

Usage:
The module can be used by importing it and calling the txt_to_srt
function.

TODO: add format check with files.
TODO: more flexible way to add date to the file_name
TODO: think about logging.
"""
# Import libraries.
from datetime import datetime, timedelta
import os


def _format_time(time_str: str) -> str:
    """Formats a time string.

    Formats a time string in the format "M:S" to "HH:MM:SS,000".

    Args:
        time_str: The time string to be formatted.

    Returns:
        time_formatted: The formatted time string.
    """
    time_obj = datetime.strptime(time_str, "%M:%S")
    time_formatted = time_obj.strftime("%H:%M:%S,000")
    return time_formatted


def _format_last_time(time_str: str) -> str:
    """Formats a time string for the last time in the subtitles.

    Formats a time in the format "M:S" to "HH:MM:SS,000" and 5 for
    the last time in the subtitles.

    Args:
        time_str: The time string in the format "%M:%S".

    Returns:
        time_formatted: The formatted time string in the format
        "%H:%M:%S,000".
    """
    time_obj = datetime.strptime(time_str, "%M:%S") + timedelta(seconds=5)
    time_formatted = time_obj.strftime("%H:%M:%S,000")
    return time_formatted


def _save_as_srt(srt: str, output_path: str) -> None:
    """Saves the given SRT content to the specified output path.

    Saves the given SRT content to the specified output path as a
    srt-file.

    Args:
        srt: The SRT content to be saved.
        output_path: The path to save the SRT file
            ("data/transcript.srt").

    Returns:
        None
    """
    with open(output_path, "w") as srt_file:
        srt_file.write(srt)


def txt_to_srt(input_path: str, output_path: str) -> str:
    """Converts a txt-file to a srt-file.

    Converts a text file to the SubRip Subtitle format (.srt).
    The formats of input and output files see in the module
    description.

    Args:
        input_path: The path to the input text file
            ("data/transcripts.txt").
        output_path: The path to save the output srt-file
            ("data/transcripts.txt").
    Returns:
        srt: The generated srt-file.
    """
    # Read the lines from the input text file.
    with open(input_path, "r") as txt_file:
        lines = txt_file.readlines()
        seqs = []
        # Convert each pair of lines into a srt-sequence.
        for num in range(0, len(lines), 2):
            # A numeric counter indicating the number of the subtitle.
            cnt = int(num / 2) + 1
            # Start and end time.
            start_time = _format_time(lines[num].strip())
            # Format the time.
            if num + 2 < len(lines):
                end_time = _format_time(lines[num + 2].strip())
            else:  # the last time in the txt-file.
                end_time = _format_last_time(lines[num].strip())
            # Subtitle text in one line.
            text = lines[num + 1].strip()
            # Create a sequence and add a blank line indicating the
            # end of the subtitle.
            seq = f"{cnt}\n{start_time} --> {end_time}\n{text}\n"
            # A list of all subtitles blocks.
            seqs.append(seq)
        # Join all subtitles block in one string and saves as
        # a srt-file.
        srt = "\n".join(seqs)
        _save_as_srt(srt, output_path)
    return srt


def main() -> None:
    """ Entry point."""
    module_dir = os.path.dirname(os.path.realpath(__file__))
    input_path = os.path.join(module_dir, "../data/transcript.txt")
    output_path = os.path.join(module_dir, "../data/transcript.srt")
    txt_to_srt(input_path, output_path)


if __name__ == "__main__":
    main()
