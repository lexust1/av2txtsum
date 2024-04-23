"""
This module cleans text in an input file and saves the cleaned text to
 an output file.

Functions:
- main: Entry point.
- clean_text: Clean the text in the input file and save the cleaned
text to the output file.

Usage:
The module can be used by importing it and calling the clean_text
function.
"""
# Import libraries.
import os
import re

# Import the third-party libraries.
from jiwer import cer, mer, wer, wil, wip


def clean_original_transcript(input_path: str, output_path: str) -> str:
    """Cleans the original transcript for error rate calculations

    Cleans the text in the input file and save the cleaned text to
    the output file.

    Args:
        input_path (str): The path to the input file.
        output_path (str): The path to the output file.

    Returns:
        cleaned_text(str): The cleaned transcript.
    """
    # Read the input file and get the text content.
    with open(input_path, "r") as file:
        text = file.read()
    # print(text)
    # Define the patterns to exclude from the text.
    patterns = [
        r"\n",  # Remove newline characters
        r">>",  # Excludes ">>" pattern
        r"\d+:\d{2}",  # Excludes time format like "0:09"
        r"\(.*?\)",  # Excludes like "(MUSIC) "
        r" \(.*?\)",  # Excludes like " (Applause) "
        r"DARIO GIL:",  # Excludes "DARIO GIL:" pattern
        r"CLEM DELANGUE:",  # Excludes "CLEM DELANGUE:" pattern
    ]
    # Remove the patterns from the text
    text = re.sub("|".join(patterns), " ", text)
    cleaned_text = re.sub(r"\s{2,}", " ", text).strip()
    # Write the cleaned text to the output file.
    with open(output_path, "w") as file:
        file.write(cleaned_text)
    return cleaned_text


def clean_whisper_transcript(input_path: str, output_path: str) -> str:
    """Cleans the whisper transcript for error rate calculations.

    Cleans the text in the input file and save the cleaned text to
    the output file.

    Args:
        input_path (str): The path to the input file.
        output_path (str): The path to the output file.

    Returns:
        cleaned_text(str): The cleaned transcript.
    """
    # Read the input file and get the text content.
    with open(input_path, "r") as file:
        text = file.read()
    # Define the patterns to exclude from the text.
    patterns = [
        r"\n",  # Remove newline characters
        r"♪\s*",  # Remove musical notes and trailing whitespace
    ]
    # Remove the patterns from the text
    cleaned_text = re.sub("|".join(patterns), "", text).strip()
    # Write the cleaned text to the output file.
    with open(output_path, "w") as file:
        file.write(cleaned_text)
    return cleaned_text


def clean_sm4t_transcript(input_path: str, output_path: str):
    """Cleans the seamlessm4t transcript for error rate calculations.

    Cleans the text in the input file and save the cleaned text to
    the output file.

    Args:
        input_path (str): The path to the input file.
        output_path (str): The path to the output file.

    Returns:
        cleaned_text(str): The cleaned transcript.
    """
    # Read the input file and get the text content.
    with open(input_path, "r") as file:
        text = file.read()


def calculate_error_rates(reference: str, hypothesis: str) -> dict:
    """Calculates different error rate metrics.

    Calculates different error rates between a reference and a hypothesis.

    Args:
        reference: The reference string.
        hypothesis: The hypothesis string.

    Returns:
        metrics: A dictionary containing different error rates.
    """
    metrics = {
        "WER": wer(reference, hypothesis),  # Word Error Rate
        "CER": cer(reference, hypothesis),  # Character Error Rate
        "MER": mer(reference, hypothesis),  # Match Error Rate
        "WIL": wil(reference, hypothesis),  # Word Information Lost
        "WIP": wip(reference, hypothesis)   # Word Information Preserved
    }
    return metrics


def main() -> None:
    """Entry point."""
    module_dir = os.path.dirname(os.path.realpath(__file__))
    input_path = os.path.join(module_dir, "../data/transcript.txt")
    output_path = os.path.join(module_dir, "../data/cleaned_original_transcript.txt")
    clean_original_transcript(input_path, output_path)

    input_path = os.path.join(module_dir, "../data/whisper_output/audio.txt")
    output_path = os.path.join(module_dir, "../data/cleaned_whisper_transcript.txt")
    clean_whisper_transcript(input_path, output_path)


if __name__ == "__main__":
    main()
